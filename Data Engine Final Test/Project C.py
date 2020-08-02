# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

def main():
    # 读取数据
    data_ori = pd.read_csv('CarPrice_Assignment.csv')
    print(data_ori)

    # 建立ID维度表
    dimension_id = data_ori[["car_ID", "CarName"]].set_index(data_ori["car_ID"]).drop(["car_ID"],1)
    print(dimension_id)

    # 处理原数据表格，使数据规范化
    data_processed  = data_ori.drop(["CarName","symboling","carbody","enginetype","cylindernumber","fuelsystem"],1)
    data_processed["fueltype"] = data_processed.fueltype.map(lambda x: 1 if x=="gas" else 0)
    data_processed["aspiration"] = data_processed.aspiration.map(lambda x :1 if x=="turbo" else 0)
    data_processed["doornumber"] = data_processed.doornumber.map(lambda x :1 if x=="four" else 0)
    data_processed["drivewheel"] = data_processed.drivewheel.map(lambda x :1 if x=="4wd" else 0)
    data_processed["enginelocation"] = data_processed.enginelocation.map(lambda x :1 if x=="front" else 0)
    data_processed = data_processed.set_index(data_processed.car_ID).drop(["car_ID"],1)
    print(data_processed)
    # 归一化
    min_max_scaler = MinMaxScaler()
    train_x = min_max_scaler.fit_transform(data_processed)
    print(train_x)

    # 手肘法
    sse = []
    for k in range(1,80):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(train_x)
        sse.append(kmeans.inertia_)
    x = range(1,80)
    plt.xlabel("K")
    plt.ylabel("SSE")
    plt.plot(x,sse,'o-')
    plt.show()

    # 进行聚类 选取14
    kmeans = KMeans(n_clusters=14)
    kmeans.fit(train_x)
    predict_y = kmeans.predict(train_x)
    print(predict_y)

    dimension_id["class"] = predict_y
    dimension_id.to_csv('car_id_class.csv')
    print(dimension_id)





if __name__ == '__main__':
    main()