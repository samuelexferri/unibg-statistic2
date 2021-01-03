import pandas as pd

def xarray2pandas(dataset, lat, lon):
    """
    Dataset must be in format [time, lat, lon]

    Returns `pandas.core.series.Series` time series
    """
    return dataset[:, lat, lon].to_series()


def ts_train_test_split(ts, ratio):
    return ts[:int(len(ts)*ratio)], ts[int(len(ts)*ratio):]