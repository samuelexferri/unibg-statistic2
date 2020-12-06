import matplotlib.pyplot as plt


def plot_shapefile(shapefile, epsg=4326, title="", xlabel="", ylabel=""):
    shapefile.to_crs(epsg=epsg, inplace=True)
    fig, ax = plt.subplots(1)
    ax = shapefile.plot(axes=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)


