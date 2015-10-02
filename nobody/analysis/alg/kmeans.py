# -*- coding: utf-8 -*-

from sklearn.cluster import KMeans


def k_means(train_data, n):

    if not train_data:
        return []

    _k_means = KMeans(n_clusters=n)
    _k_means.fit(train_data)
    labels = _k_means.labels_

    return labels, _k_means.predict
