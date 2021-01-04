import matplotlib.pyplot as plt


def plot_shapefile(shapefile, epsg=4326, title="", xlabel="", ylabel=""):
    """
    Plot shapefile
    """
    shapefile.to_crs(epsg=epsg, inplace=True)
    fig, ax = plt.subplots(1)
    ax = shapefile.plot(axes=ax)
    ax.set_xlabel(xlabel, labelpad=10)
    ax.set_ylabel(ylabel, labelpad=10)
    ax.set_title(title, fontsize=15)


import numpy as np
from scipy.stats import norm


def plot_distributions(ts, title='', xlabel='',):
    """
    Plot distributions
    """
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    fig.suptitle(title, fontsize=15)

    fig.subplots_adjust(wspace = 0.5)

    result = axs[0].hist(ts, bins=20)

    mean = np.mean(ts)
    sigma = np.sqrt(np.var(ts))
    x = np.linspace(min(ts), max(ts), 100)
    dx = result[1][1] - result[1][0]
    scale = len(ts) * dx

    axs[0].plot(x, norm.pdf(x, mean, sigma) * scale)
    axs[0].set_xlabel(xlabel[0], labelpad=10)
    axs[0].set_ylabel('Frequency', labelpad=10)

    axs[1] = ts.plot(kind="kde")
    axs[1].set_xlabel(xlabel[1], labelpad=10)
    axs[1].set_ylabel('Density', labelpad=10)

    plt.show()