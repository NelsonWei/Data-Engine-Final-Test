# -*- coding:utf-8 -*-
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from efficient_apriori import apriori as e_apriori


def processByMl(df):
    # one-hot 编码
    df_hot_encoded = df.drop("产品名称",1).join(df["产品名称"].str.get_dummies())
    # print(df_hot_encoded)

    # 设置index
    df_hot_encoded.set_index(["订单日期","客户ID"],inplace=True)

    # 挖掘频繁项集 和 关联规则

    itemsets = apriori(df_hot_encoded, use_colnames=True, min_support=5)
    rules = association_rules(itemsets, metric='lift', min_threshold=2)



def processByEf(df):
    # 以 订单日期 和 客户ID 分组
    grouped = df.groupby(["订单日期", "客户ID"])

    # 生成 transactions
    transactions_product = []
    for key, value in grouped:
        transactions_product.append(set(value["产品名称"]))

    # 训练模型
    itermsets,rules = e_apriori(transactions_product,min_support=0.02,min_confidence=0.2)
    k_iter = len(itermsets[1])+len(itermsets[2])

    # 输出结果
    print("EF-Apriori关联分析".center(50,'*'))
    print("共找到{}个频繁项集，{}种关联规则".format(k_iter,len(rules)))
    print("频繁项集：")
    print(itermsets)
    print("关联规则：")
    print(rules)


def main():
    # 读取数据
    order_df = pd.read_csv('订单表.csv', encoding='GBK')
    # print(order_df)

    # 数据分组
    order_main = order_df[["订单日期", "客户ID", "产品名称"]]
    # order_grouped = order_main.groupby(["订单日期", "客户ID"])

    # 分别使用两种方法进行关联分析
    processByEf(order_df)
    # processByMl(order_df) 经计算无法得到rules


if __name__ == '__main__':
    main()