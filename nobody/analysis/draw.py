# -*- coding: utf-8 -*-

import itertools
from StringIO import StringIO

import matplotlib.pyplot as plt
import numpy as np


def plot_decision_boundary(predict_func, data):
    # Set min and max values and give it some padding
    x_min, x_max = data[:, 0].min() - .5, data[:, 0].max() + .5
    y_min, y_max = data[:, 1].min() - .5, data[:, 1].max() + .5
    h = 0.01
    # Generate a grid of points with distance h between them
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    # Predict the function value for the whole gid
    Z = predict_func(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    # Plot the contour and training examples
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)


def plot_2d(predict_func, data, labels, title, features):
    n_data = np.array(data)
    _types = list(set(labels))
    _buffer = StringIO()

    colors = itertools.cycle('bgrcmybgrcmybgrcmybgrcmy')
    plot_decision_boundary(predict_func, n_data)

    for t, col in zip(_types, colors):
        m = np.array([_[0] for _ in zip(data, labels) if _[1] == t])
        x, y = m[:, 0], m[:, 1]
        plt.scatter(x, y, marker='o', c=col, cmap=plt.cm.Spectral)

    plt.xlabel(features[0])
    plt.ylabel(features[1])
    plt.title(title)

    plt.savefig(_buffer, format='PNG')
    plt.close()

    _buffer.seek(0)
    return _buffer
