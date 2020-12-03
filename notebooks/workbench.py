import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

ds_ammoniaca = xr.load_dataset("./datasets/ammoniaca.nc")
lat_bounds = slice(44.74, 46.56)
lon_bounds = slice(8.5, 11.25)

ammoniaca = ds_ammoniaca.__xarray_dataarray_variable__.sel(
    lat=lat_bounds, lon=lon_bounds
)

# Copernicus (0.1°x0.1°)
ds_temperature = xr.load_dataset("./datasets/temperature.nc")
lat_bounds = slice(46.66, 44.64)  # Invertiti
lon_bounds = slice(8.5, 11.35)

t2m = ds_temperature.t2m.sel(latitude=lat_bounds, longitude=lon_bounds)
lai_hv = ds_temperature.lai_hv.sel(latitude=lat_bounds, longitude=lon_bounds)
lai_lv = ds_temperature.lai_lv.sel(latitude=lat_bounds, longitude=lon_bounds)

t2m = t2m.transpose("time", "latitude", "longitude")
t2m = t2m.sortby("latitude", ascending=True)  # Riordina

lats = t2m.latitude
lons = t2m.longitude
ammoniaca_lats = ammoniaca.lat
ammoniaca_lons = ammoniaca.lon

coords = [(lat, lon) for lat in lats.to_series() for lon in lons.to_series().tolist()]
ammoniaca_coords = [
    (lat, lon)
    for lat in ammoniaca_lats.to_series().tolist()
    for lon in ammoniaca_lons.to_series().tolist()
]

lats = [coord[0] for coord in coords]
lons = [coord[1] for coord in coords]

ammoniaca_lats = [coord[0] for coord in ammoniaca_coords]
ammoniaca_lons = [coord[1] for coord in ammoniaca_coords]

plt.scatter(lons, lats, c="r")
plt.scatter(ammoniaca_lons, ammoniaca_lats, c="y")

times = t2m.time.to_series().tolist()

t2m_adjusted_data = np.ones((len(times), len(ammoniaca_lats), len(ammoniaca_lons)))
t2m_adjusted_data.fill(np.nan)
# for t in range(len(times)):
for t in range(1):
    for lt in range(1, len(ammoniaca.lat) - 1):
        for ln in range(1, len(ammoniaca.lon) - 1):
            val = (
                t2m[t][lt - 1][ln - 1]
                + t2m[t][lt - 1][ln + 1]
                + t2m[t][lt + 1][ln - 1]
                + t2m[t][lt + 1][ln + 1]
            )
            t2m_adjusted_data[t][lt][ln] = val / 4
            print(t)

t2m_adjusted = xr.DataArray(
    t2m_adjusted_data,
    coords=[times, ammoniaca_lats, ammoniaca_lons],
    dims=["time", "lat", "lon"],
)
print(t2m_adjusted)

plt.scatter(t2m_adjusted.lon, t2m_adjusted.lat, c="b")
plt.show()