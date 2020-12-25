import matplotlib.pyplot as plt


def plot_shapefile(shapefile, epsg=4326, title="", xlabel="", ylabel=""):
    """
    Plot shapefile
    """
    shapefile.to_crs(epsg=epsg, inplace=True)
    fig, ax = plt.subplots(1)
    ax = shapefile.plot(axes=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)


import numpy as np
from scipy.stats import norm


def plot_distributions(ts, title):
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    result = axs[0].hist(ts, bins=20)
    fig.suptitle(title)
    mean = np.mean(ts)
    sigma = np.sqrt(np.var(ts))
    x = np.linspace(min(ts), max(ts), 100)
    dx = result[1][1] - result[1][0]
    scale = len(ts) * dx
    axs[0].plot(x, norm.pdf(x, mean, sigma) * scale)
    axs[1] = ts.plot(kind="kde")
    plt.show()