""""""
import pandas as pd
import logging
from utils import Utils
from orchestrators.abstract_orchestrator import OrchestratorABC
from data_processor import DataProcessor
from sklearn.model_selection import train_test_split


logger = logging.getLogger(__name__)


class LocalOrchestrator(OrchestratorABC):
    def __init__(self):
        """Initialize the orchestrator."""

    def run(self, config, predictor):
        """Run the orchestrator."""
        if self.config["train_model"]:
            # Load data
            ...
            # Train a new model
            ...
        else:
            # Load data
            ...
            # Load a trained model and predict using it
            ...

    def train(self, config, predictor, data):
        """Trains a new model."""
        # initialize the data processor and run it on the data
        ...
        # pre-validate data via great expectation
        ...
        # validate the data via preprocess
        ...
        # post-validate data via great expectation
        ...
        # Get the features columns
        ...
        # Get the target column
        ...
        # Split the data into train and test sets
        ...
        # Train the model
        ...
        # Evaluate the model
        ...
        # generate a model path
        model_path = Utils.generate_model_path(config, self.TIME_STAMP)        
        # Save the model to the model path
        model = {"processor": processor, "predictor": predictor}
        Utils.save_pkl(model, model_path)

    def load_predict(self, config, data):
        # Load the model from the model path you can use Utils.load_pkl method    
        ...
        # get the trained processor and run it on the data
        ...
        # get the trained predictor and predict using it
        ...
        # combine the predictions with the original data
        ...
        # inverse transform the predictions
        ...
        # Save the predictions to a csv fileupda
        Utils.write_to_csv(final_df, config["predicted_result_path"])
        