# -*- coding: utf-8 -*-

# from sklearn import datasets, cluster
#
# iris = datasets.load_iris()
# k_means = cluster.KMeans(3)
#
# k_means.fit(iris.data)
#
# print k_means.labels_[::10]
# print iris.target[::10]

from sklearn import datasets
from matplotlib import pyplot as plt
import numpy as np

iris = datasets.load_iris()

for t, m, col in zip(xrange(3), '>ox', 'rgb'):
    plt.scatter(iris.data[iris.target == t, 0],
                iris.data[iris.target == t, 1],
                marker=m, c=col)
plt.xlabel(iris.feature_names[0])
plt.ylabel(iris.feature_names[1])

plt.savefig('test.png', dpi=72)

import collections

from sklearn.cluster import KMeans
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt

# 测试性数据的导入和设置
iris = datasets.load_iris()

train_data = iris.data
target_data = iris.target

X = np.array(train_data)

kmeans = KMeans(n_clusters=3)
kmeans.fit(train_data)
labels = kmeans.labels_

# mapping = {}
#
# for _i, (s, e) in enumerate([(0, 50), (50, 100), (100, 150)]):
#     d = collections.defaultdict(list)
#     for i, _ in enumerate(labels[s:e]):
#         d[_].append(i)
#
#     t = sorted(d.items(), key=lambda x: len(x[1]))
#     mapping[_i] = t[-1][0]
#
# labels = [mapping[_] for _ in labels]

for t, m, col in zip(xrange(3), '>ox', 'bgr'):
    plt.scatter(train_data[target_data == t, 0],
                train_data[target_data == t, 1],
                marker=m, c=col)
    # plt.scatter(train_data[labels == t, 0],
    #             train_data[labels == t, 1],
    #             s=80, marker=m, c=col)

plt.xlabel(iris.feature_names[0])
plt.ylabel(iris.feature_names[1])

plt.title('Plot of picture')
plt.savefig('test.png', dpi=72)
