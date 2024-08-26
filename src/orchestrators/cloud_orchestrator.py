""""""
import logging
import os
import pickle

import mlflow  # type: ignore
import pandas as pd
from azure.ai.ml import MLClient
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Model
from azure.identity import DefaultAzureCredential
from data_processor import DataProcessor
from dnalib.azfile import AzFile, azure_init  # type: ignore
from dotenv import load_dotenv
from orchestrators.abstract_orchestrator import OrchestratorABC
from sklearn.model_selection import train_test_split  # type: ignore
from utils import Utils

logger = logging.getLogger(__name__)
load_dotenv(".env")


class CloudOrchestrator(OrchestratorABC):
    def __init__(self):
        """Initialize the orchestrator."""

    def run(self, config, predictor):
        """Run the orchestrator."""
        # Donwload data from azure to local
        azure_init(
            azure_storage_secrets={
                "dsdev": {
                    "container_url": ...
                },  # SAS URL for a Container
            }
        )
        # implement the full download with try, except

        # Load data
        if config["train_model"]:
            # Train a new model
            ...
        else:
            # Load a trained model and predict using it
            ...

    def train(self, config, predictor, data):
        """Train the model."""
        # initiate DataProcessor
        ...
        # pre-validate data via great expectations
        ...
        # validate the data via preprocess
        ...
        # post-validate data via great expectations
        ...
        # Get the features columns
        ...
        # Get the target column
        ...
        # Split the data into train and test sets
        ...

        # Initiate MLClient Project, remember to implement def ml_client_project first
        ml_client = self.ml_client_project()
        mlflow_tracking_uri = ml_client.workspaces.get(ml_client.workspace_name).mlflow_tracking_uri
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        mlflow.set_experiment(os.getenv("AZUREML_EXPERIMENT_NAME"))
        # setup mlflow tracking & experiment
        ... 
        ...
        with mlflow.start_run() as mlfrun:
            # Train the model
            ...
            # Evaluate the model
            ...
            # Log metrics
            ...
            ...

            # ==================================================================#
            from mlflow.pyfunc import PythonModel, PythonModelContext
            class ModelWrapper(PythonModel):
                def __init__(self, model):
                    self.predictor = model['predictor']
                    self.processor = model['processor']
                def predict(self, context: PythonModelContext, data):
                    # You don't have to keep the semantic meaning of `predict`. You can use here model.recommend(), model.forecast(), etc
                    data = self.processor.preprocess(data)
                    data = self.predictor.predict(data)
                    # data = self.processor.post_process(data)
                    return data
            model = {"processor": processor, "predictor": predictor}
            mlflow.pyfunc.log_model("model", python_model=ModelWrapper(model))
            # ==================================================================#
            # Get, from the MLflow run object, the run ID
            ...
            # Now register the model
            ...

    def load_predict(self, config, data):
        # Initiate MLClient Project, remember to implement def ml_client_project first    
        ml_client = self.ml_client_project()
        mlflow_tracking_uri = ml_client.workspaces.get(ml_client.workspace_name).mlflow_tracking_uri
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        mlflow.set_experiment(os.getenv("AZUREML_EXPERIMENT_NAME"))
        prefix = os.environ.get("AZUREML_MODEL_NAME")

        # Implement model download
        model_name = f'{prefix}_{config["model_type"]}'
        
        """
        - Get the model version, if none provided in .env, get the latest version
        - Use ml_client.models.list(name=...) to get the model versions and then get the latest version from the list
        - Get the model by name and version using ml_client.models.get(name=..., version=...)
        - Download the model locally (current dir by default) using ml_client.models.download(name=..., version=..., download_path=...)
        - Load the downloaded model from the download path
        """

        # load the downloaded model
        ...
        # get the data processor and preprocess the data
        ... 
        # combine the predictions with the original data
        ... 
        # inverse transform the predictions
        ... 
        # Save the predictions to a csv file
        Utils.write_to_csv(final_df, config["predicted_result_path"])

    def ml_client_project(self):
        """Get the ml_client project."""
        ml_client = MLClient(
            ...
        )
        return ml_client
