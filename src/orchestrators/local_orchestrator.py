import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import logging
from datetime import datetime
from utils import Utils
from orchestrators.abstract_orchestrator import OrchestratorABC
from data_processor import DataProcessor
from sklearn.model_selection import train_test_split
from predictors.lr_predictor import LinearModel
from predictors.svm_predictor import SVMModel


class LocalOrchestrator(OrchestratorABC):
    def __init__(self):
        """Initialize the orchestrator."""
        self.model_registry = {}

    def run(self, config, predictor):
        """Run the orchestrator."""
        if config["train_model"]:
            self.train(config, predictor)  # Train a new model
        else:
            self.load_predict(config)  # Load a trained model and predict using it

        # Return the model registry and predictions if available
        return self.model_registry

    def train(self, config, predictor):
        """Train a new model."""
        # Load data from file
        dataframe = pd.read_csv(config["input_data"])

        # Initialize the data processor and preprocess the data
        processor = DataProcessor(config)
        dataframe = processor.preprocess(dataframe)

        processor.pre_validation(dataframe)
        # # Validate the data via preprocess
        processor.preprocess(dataframe)
        # # Post-validate data via great expectations
        processor.post_validation(dataframe)

        # Get the features 
        X = dataframe[config["data_params"]["features"]]
        #Get the target column
        Y = dataframe[config["data_params"]["target"]]

        # Split the data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=config["test_size"], random_state=42)

        # Train the model
        predictor.fit(X_train, y_train)

        # Evaluate the model
        score = predictor.score(X_test, y_test)
        logging.info(f"Model score: {score}")
        TIME_STAMP = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        # Generate a model path and save the model
        model_path = Utils.generate_model_path(config, TIME_STAMP)
        model = {"processor": processor, "predictor": predictor}
        Utils.save_pkl(model, model_path)

        # Update the model registry
        self.model_registry[config["model_type"]] = model

    def load_predict(self, config):
        """Load a trained model and predict using it."""
        # Load data from file
        dataframe = pd.read_csv(config["input_data"])

        # Load the model from the specified file
        model = Utils.load_pkl(config["trained_model_file"])

        # Get the trained processor and preprocess the data
        processor = model["processor"]
        dataframe = processor.pre_process(dataframe)

        # Get the trained predictor and make predictions
        predictor = model["predictor"]
        y_pred = predictor.predict(dataframe[config["data_params"]["features"]])

        # Combine the predictions with the original data
        final_df = pd.concat([dataframe, pd.DataFrame(data=y_pred, index=dataframe.index, columns=[config["data_params"]["target"]])], axis=1)

        # Post-process the predictions
        final_df = processor.post_process(final_df)

        # Save the predictions to a CSV file
        Utils.write_to_csv(final_df, config["predicted_result_path"])

        # Update the model registry with the loaded model
        self.model_registry[config["model_type"]] = model
        return self.model_registry