# -*- coding: utf-8 -*-

from sklearn import datasets
from matplotlib import pyplot as plt
import numpy as np
import sklearn.linear_model
import matplotlib


matplotlib.rcParams['figure.figsize'] = (10.0, 8.0)

np.random.seed(0)

X, y = datasets.make_moons(200, noise=0.20)

plt.scatter(X[:, 0], X[:, 1], s=40, c=y, cmap=plt.cm.Spectral)

clf = sklearn.linear_model.LogisticRegressionCV()
clf.fit(X, y)

print X[:, 0].min(), X[:, 1].max()
print clf.predict([0, 0])


def plot_decision_boundary(pred_func):
    # Set min and max values and give it some padding
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    h = 0.01
    # Generate a grid of points with distance h between them
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    # Predict the function value for the whole gid
    Z = pred_func(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    # Plot the contour and training examples
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Spectral)

plot_decision_boundary(lambda x: clf.predict(x))
plt.title("Logistic Regression")

plt.savefig('test.png', dpi=80)

# - - - - - - - - - -

# from matplotlib import pyplot as plt
# import numpy as np
#
# X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
# C, S = np.cos(X), np.sin(X)
#
# plt.figure(figsize=(8, 6), dpi=60)
#
# ax = plt.subplot(1, 1, 1)
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
# ax.xaxis.set_ticks_position('bottom')
# ax.spines['bottom'].set_position(('data', 0))
# ax.yaxis.set_ticks_position('left')
# ax.spines['left'].set_position(('data', 0))
#
# plt.plot(X, C, color='blue', linewidth=1.0, linestyle='-', label='cos')
# plt.plot(X, S, color='green', linewidth=1.0, linestyle='-', label='sin')
#
# plt.xlim(X.min()*1.1, X.max()*1.1)
# plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
#            [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
#
# plt.ylim(C.min()*1.1,C.max()*1.1)
# plt.yticks([-1, 0, +1],
#            [r'$-1$', r'$0$', r'$+1$'])
#
# t = 2 * np.pi / 3
# plt.plot([t, t], [0, np.cos(t)], color='blue', linewidth=1.5, linestyle="--")
# plt.scatter([t, ], [np.cos(t), ], 50, color='blue')
# plt.annotate(r'$\sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$',
#              xy=(t, np.sin(t)),  xycoords='data',
#              xytext=(+10, +30), textcoords='offset points', fontsize=16,
#              arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
#
# plt.plot([t, t], [0, np.sin(t)], color='red',  linewidth=1.5, linestyle="--")
# plt.scatter([t, ], [np.sin(t), ], 50, color='red')
# plt.annotate(r'$\cos(\frac{2\pi}{3})=-\frac{1}{2}$',
#              xy=(t, np.cos(t)),  xycoords='data',
#              xytext=(-90, -50), textcoords='offset points', fontsize=16,
#              arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
#
# for label in ax.get_xticklabels() + ax.get_yticklabels():
#     label.set_fontsize(16)
#     label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.65))
#
# plt.legend(loc='upper left', frameon=False)
#
# plt.savefig('test.png', dpi=80)


