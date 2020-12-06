import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# TODO: invertire assi temperatura prima di passarla come argomento
    # ds = ds.transpose("time", "latitude", "longitude")
    # ds = ds.sortby("latitude", ascending=True)  # Riordina
def adjust_var_grid(ds, target_lats, target_lons, dims=["time", "lat", "lon"], shift=0.051, plot=False):
    """
    Adjust grid of input variable layer
    """
    lat_bounds = slice(min(target_lats) - shift, max(target_lats) + shift) 
    lon_bounds = slice(min(target_lons) - shift, max(target_lons) + shift)

    ds = ds.sel(latitude=lat_bounds, longitude=lon_bounds)

    lats = ds.latitude
    lons = ds.longitude

    times = ds.time.to_series().tolist()

    ds_adjusted_data = np.ones((len(times), len(target_lats), len(target_lons)))
    ds_adjusted_data.fill(np.nan)

    for lat in range(1, len(lats)):
        for lon in range(1, len(lons)):
            mean = (
                ds[:, lat - 1, lon - 1] * 0.25
                + ds[:, lat - 1, lon] * 0.25
                + ds[:, lat, lon - 1] * 0.25
                + ds[:, lat, lon] * 0.25
            )
            ds_adjusted_data[:, lat - 1, lon - 1] = mean

    ds_adjusted = xr.DataArray(
        ds_adjusted_data,
        coords=[times, target_lats, target_lons],
        dims=dims,
    )

    if plot:
        ds_adjusted.mean(dim='time').plot()
        plt.show()

    return ds_adjusted

# ds_nh3 = xr.load_dataset('./datasets/CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_nh3_v4.2_monthly_lombardia.nc')
# ds = xr.load_dataset('./datasets/temperature.nc')
# ds = ds.t2m
# ds = ds.transpose("time", "latitude", "longitude")
# ds = ds.sortby("latitude", ascending=True)  # Riordina
# res = adjust_var_grid(ds, ds_nh3.lat, ds_nh3.lon, plot=True)