import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import multiprocess

def adjust_var_grid(ds_ammoniaca, ds_temperature, var):
    """
    Adjust grid of input variable layer
    adjust_var_grid("../datasets/CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_nh3_v4.2_monthly_lombardia.nc", "../datasets/temperature.nc", "t2m")
    """
    ds_ammoniaca = xr.load_dataset(ds_ammoniaca) # Copernicus (0.1°x0.1°)
    lat_bounds = slice(44.74, 46.56)
    lon_bounds = slice(8.5, 11.25)

    ammoniaca = ds_ammoniaca.agl.sel(
        lat=lat_bounds, lon=lon_bounds
    )

    ds_temperature = xr.load_dataset(ds_temperature) # Copernicus (0.1°x0.1°)
    lat_bounds = slice(46.66, 44.64)  # Invertiti
    lon_bounds = slice(8.5, 11.35)

    var = ds_temperature.t2m.sel(latitude=lat_bounds, longitude=lon_bounds)
    lai_hv = ds_temperature.lai_hv.sel(latitude=lat_bounds, longitude=lon_bounds)
    lai_lv = ds_temperature.lai_lv.sel(latitude=lat_bounds, longitude=lon_bounds)

    var = var.transpose("time", "latitude", "longitude")
    var = var.sortby("latitude", ascending=True)  # Riordina

    lats = var.latitude
    lons = var.longitude
    ammoniaca_lats = ammoniaca.lat
    ammoniaca_lons = ammoniaca.lon

    coords = [(lat, lon) for lat in lats.to_series() for lon in lons.to_series().tolist()]
    ammoniaca_coords = [(lat, lon) for lat in ammoniaca_lats.to_series() for lon in ammoniaca_lons.to_series().tolist()]

    lats = [coord[0] for coord in coords]
    lons = [coord[1] for coord in coords]

    # plt.scatter(lons, lats, c="r")
    # plt.scatter(ammoniaca_lons, ammoniaca_lats, c="y")

    times = var.time.to_series().tolist()

    t2m_adjusted_data = np.ones((len(times), len(ammoniaca.lat), len(ammoniaca.lon)))
    t2m_adjusted_data.fill(np.nan)

    for t in range(len(times)):
        print("Adjusting time: " + str(t))
        for lt in range(1, len(ammoniaca.lat) - 1):
            for ln in range(1, len(ammoniaca.lon) - 1):
                val = (
                    var[t][lt - 1][ln - 1]
                    + var[t][lt - 1][ln + 1]
                    + var[t][lt + 1][ln - 1]
                    + var[t][lt + 1][ln + 1]
                )
                t2m_adjusted_data[t][lt][ln] = val / 4

    t2m_adjusted = xr.DataArray(
        t2m_adjusted_data,
        coords=[times, ammoniaca.lat, ammoniaca.lon],
        dims=["time", "lat", "lon"],
    )
    # print(t2m_adjusted)

    print ("Adjusted!")

    # plt.scatter(ammoniaca_lons, ammoniaca_lats, c="y")
    # plt.scatter(t2m_adjusted.lon, t2m_adjusted.lat, c="b")
    # plt.show()

    return t2m_adjusted