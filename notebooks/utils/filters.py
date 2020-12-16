import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point


def filter_grid_on_shapefile(lats, lons, shp, plot_grid=False, plot_filter=False):
    """
    Filter grid on shapefile
    """
    # Create the latitudes/longitudes grid
    coords = [(lat, lon) for lat in lats for lon in lons]

    lats = [coord[0] for coord in coords]
    lons = [coord[1] for coord in coords]

    if plot_grid:
        plt.figure()
        plt.title("Observations Grid")
        plt.xlabel("longitutde")
        plt.ylabel("latitude")
        plt.scatter(lons, lats, c="r")
        plt.show()

    # Consider only the points inside the shape
    grid = [
        (round(lat, 2), round(lon, 2))
        for lat, lon in zip(lats, lons)
        if shp.geometry.contains(Point(lon, lat)).bool()
    ]

    if plot_filter:
        lats = [coord[0] for coord in grid]
        lons = [coord[1] for coord in grid]
        plt.figure()
        shp.plot()
        plt.scatter(lons, lats, c="r")
        plt.title("Filtered Observations Grid")
        plt.xlabel("longitutde")
        plt.ylabel("latitude")
        plt.show()

    return grid


def filter_data_on_shapefile(data, lats, lons, shp, epsg=None, plot_grid=False, plot_filter=False):
    """
    Filter data on shapefile
    """
    if epsg is not None:
        shp.to_crs(epsg=epsg, inplace=True)

    lats = [round(lat, 2) for lat in lats.to_series().tolist()]
    lons = [round(lon, 2) for lon in lons.to_series().tolist()]

    result = np.ones((248, len(lats), len(lons))) # Times length = 248 (2000-01 to 2020-08)
    result.fill(np.nan)

    grid = filter_grid_on_shapefile(
        lats=lats, lons=lons, shp=shp, plot_grid=plot_grid, plot_filter=plot_filter
    )

    for lat_idx, lat in enumerate(lats):
        for lon_idx, lon in enumerate(lons):

            if (lat, lon) in grid:
                for time_idx in range(len(data.time.to_series().tolist())):
                    result[time_idx][lat_idx][lon_idx] = data[
                        time_idx, lat_idx, lon_idx
                    ].values
    return result