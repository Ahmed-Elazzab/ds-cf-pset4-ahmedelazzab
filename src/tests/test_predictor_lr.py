"""Module with tests for the SVM Model."""

import os
import sys
import unittest

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from statsmodels.stats.stattools import durbin_watson

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from predictors.lr_predictor import LinearModel  # noqa


class LinearModelTestCase(unittest.TestCase):
    """Linear model test cases."""

    def setUp(self):
        """Set up the test case by creating a linear model and setting up the data."""
        # Generate synthetic regression data
        X, y = make_regression(n_samples=500, n_features=5, random_state=42)
        X = pd.DataFrame(X)
        y = pd.DataFrame(y)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, random_state=42)
        # Create an instance of the LinearModel class
        self.predictor = LinearModel()

    def test_fit(self):
        """Test the `fit` method of the LinearModel class."""
        self.predictor.fit(self.X_train, self.y_train)
        # Assert that the model is not None
        self.assertIsNotNone(self.predictor.model)
        # Assert that the model is an instance of the sklearn LinearRegression class
        self.assertIsInstance(self.predictor.model, LinearRegression)
        # Assert that the model is not empty
        self.assertGreater(len(self.predictor.model.coef_), 0)

    def test_predict(self):
        """
        Test the `predict` method of the LinearModel class.

        The method fits the linear model using the provided data, then calls the `predict`
        method to obtain the predicted values. The method asserts that the shape of the predicted
        values matches the shape of the original target values.

        Asserts:
            - The shape of the predicted values matches the shape of the original target values.
        """
        self.predictor.fit(self.X_train, self.y_train)

        # Call the `predict` method to obtain the predicted values
        y_pred = self.predictor.predict(self.X_test)
        # Assert that the shape of the predicted values
        self.assertEqual(y_pred.shape, self.y_test.shape)
        # Assert that y_pred and y_test are similar using np.allclose
        self.assertTrue(np.all(np.allclose(y_pred, self.y_test, rtol=1e-5, atol=1e-5)))
        # assert that the y_pred is not None
        self.assertIsNotNone(y_pred)
        # assert that the y_pred doens't contain any null values
        self.assertFalse(np.isnan(y_pred).any())

    def test_score(self):
        """
        Test the `score` method of the LinearModel class.

        The method fits the linear model using the provided data, then calls the `score`
        method to obtain the coefficient of determination (R^2 score). The method asserts that the
        score is within the range of 0 to 1.

        Asserts:
            - The obtained score is greater than or equal to 0.
            - The obtained score is less than or equal to 1.
        """
        self.predictor.fit(self.X_train, self.y_train)
        # Call the `score` method to obtain the score
        score = self.predictor.score(self.X_test, self.y_test)
        # calculate the score using the sklearn.metrics.r2_score method
        y_pred = self.predictor.predict(self.X_test)
        residuals = self.y_test.values - y_pred
        expected_score = {
            "MAPE": float(metrics.mean_absolute_percentage_error(self.y_test, y_pred)),
            "R2": float(metrics.r2_score(self.y_test, y_pred)),
            "Durbin-Watson": float(durbin_watson(residuals)[0]),
        }
        print(expected_score, score)
        # Assert that the r2 score is greater than or equal to 0
        self.assertGreaterEqual(score["R2"], 0)
        self.assertGreaterEqual(score["MAPE"], 0)
        self.assertGreaterEqual(score["Durbin-Watson"], 0)
        # Assert that the r2 score is less than or equal to some value
        self.assertLessEqual(score["R2"], 1)
        self.assertLessEqual(score["Durbin-Watson"], 4)
        # Assert that the score is not None
        self.assertIsNotNone(score["MAPE"])
        self.assertIsNotNone(score["R2"])
        self.assertIsNotNone(score["Durbin-Watson"])
        # Assert that the score is a dictionary
        self.assertIsInstance(score, dict)
        # Assert that the score is similar to the expected score
        self.assertAlmostEqual(score["MAPE"], expected_score["MAPE"], places=2)
        self.assertAlmostEqual(score["R2"], expected_score["R2"], places=2)
        self.assertAlmostEqual(score["Durbin-Watson"], expected_score["Durbin-Watson"], places=2)


if __name__ == "__main__":
    unittest.main()
