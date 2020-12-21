import pandas as pd
import numpy as np
import sklearn.linear_model as skl_lm
import matplotlib.pyplot as plt
import statsmodels as sm
import matplotlib.pyplot as plt
from utils import utils




def cross_validation(data, k, p, d, q, plot=False):
    """
    Cross validation
    """
    n = len(data)
    rmse = []
    aics = []
    bics = []

    for i in range(k - 1):
        start = ((n * (i + 1)) / k )

        # Divide data into two dataset: training and validation
        train_set = data[0:int(start)].to_period('M')
        validation_set = data[int(start):int(start+int(n/k))].to_period('M')

        # Model fitting
        model = sm.tsa.arima.model.ARIMA(train_set, order=(p,d,q))
        model_fit = model.fit()

        predictions = []
        errors = []

        # Predictions
        for i in range(int(n/k)):
            prediction = model_fit.forecast()
            model_fit = model_fit.append([prediction.values[0]])
            predictions.append(prediction.values[0])
            errors.append(validation_set.values[i] - prediction.values[0])

        if plot is True:
            plt.figure()
            predictions = pd.Series(predictions, index=validation_set.index)
            predictions.plot()
            validation_set.plot()
            plt.show()

        rmse.append(sum(np.array(errors)**2))

    return np.mean(rmse)