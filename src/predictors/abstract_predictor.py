"""Base class for all the predictors.

The parameters (attributes) are initialized by the child model class.
"""

import logging
from abc import ABC, abstractmethod

import numpy as np
from sklearn.metrics import r2_score
from statsmodels.stats.stattools import durbin_watson

logger = logging.getLogger(__name__)


class PredictorABC(ABC):
    """Abstract class for all Predictor types."""

    def __init__(self):
        """Initialize the predictor."""
        self.model = None

    @abstractmethod
    def fit(self, X_train, y_train):
        """Fit predictor.

        X:{ndarray, sparse matrix} of shape (n_samples, n_features)
        The input samples.
        y:ndarray of shape (n_samples,)
        The input target value.

        self : object
        Fitted estimator.
        """
        raise NotImplementedError()

    @abstractmethod
    def predict(self, X):
        """Applies the model to predict price for given X."""
        raise NotImplementedError()

    def score(self, X_test, y_test):
        """
        X:{ndarray, sparse matrix} of shape (n_samples, n_features)
        Test samples.
        y:ndarray of shape (n_samples,)
        True values for X.

        score:float
        """

        # 1. Implement a method that returns the MAPE, R2, and Durbin-Watson of the model. It should be a dictionary.
        # Calculate the predictions using the model's predict method
        y_pred = self.predict(X_test)

        # Calculate MAPE (Mean Absolute Percentage Error)
        mape = float(np.mean(np.abs((y_test - y_pred) / y_test)) * 100)

        # Calculate R2 score
        r2 = float(r2_score(y_test, y_pred))

        # Calculate Durbin-Watson score
        dw = float(durbin_watson(y_test - y_pred))

        # Create a dictionary to store the scores
        scores = {"MAPE": mape, "R2": r2, "Durbin-Watson": dw}

        return scores
