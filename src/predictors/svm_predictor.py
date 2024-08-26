"""A class for SVM model that uses MLPredictor abstract class."""

from sklearn.svm import SVR

from predictors.abstract_predictor import PredictorABC


class SVMModel(PredictorABC):
    """SVM model class using abstract model class."""

    # 1. Assign the model property of Parent predictor to SVR
    def __init__(self):
        self.model = SVR()

    def fit(self, X_train, y_train):
        """Builds the ml model on train data."""

        # 2. Apply fit method to train model accordingly
        self.model.fit(X_train, y_train)

    def predict(self, X):
        """Applies the model to predict price for given X."""
        return self.model.predict(X)
