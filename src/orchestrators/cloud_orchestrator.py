import logging
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
from azureml.core import Workspace


load_dotenv(".env")


container_url = os.getenv("SECRET_AZURE_INPUT_SAS_URL")
# import pdb; pdb.set_trace()
working_dir = os.getenv("DSDEV_WORK_DIR")
train_data = os.getenv("AZFILE_TRAIN_INPUT_DATA")


logger = logging.getLogger(__name__)



class CloudOrchestrator(OrchestratorABC):
    def __init__(self):
        """Initialize the orchestrator."""
        self.default_credential = DefaultAzureCredential()

    def run(self, config, predictor):
        """Run the orchestrator."""
        # Download data from Azure to local
        azure_init(
            azure_storage_secrets={
                "dsdev": {
                    "container_url": container_url
                },  # SAS URL for a Container
            }
        )
        # Implement the full download with try, except
        local_file_path = os.path.join(working_dir, "kc_house_data.csv")

        azf = AzFile.from_string(train_data)
        azf.download(local_dest=local_file_path)
        # Load data
        if config["train_model"]:
            self.train(config, predictor)  # Train a new model
        else:
            self.load_predict(config)  # Load a trained model and predict using it
        # Return the model registry and predictions if available
    


    def train(self, config, predictor):
        """Train the model."""
        # Initiate DataProcessor
        dataframe = pd.read_csv(config["input_data"])
        processor = DataProcessor(config)
        dataframe = processor.preprocess(dataframe)

        # Pre-validate data via great expectations
        processor.pre_validation(dataframe)
        # # Validate the data via preprocess
        processor.preprocess(dataframe)
        # # Post-validate data via great expectations
        processor.post_validation(dataframe)
        # Get the features columns
        X = dataframe[config["data_params"]["features"]]
        # Get the target column
        Y = dataframe[config["data_params"]["target"]]
        # Split the data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=config["test_size"], random_state=42)

        # Initiate MLClient Project
        def ml_client_project():
            """Get the ml_client project."""
            # Provide the necessary parameters and configurations for your MLClient initialization
            subscription_id = os.getenv("AZUREML_SUBSCRIPTION_ID")
            resource_group = os.getenv("AZUREML_RESOURCE_GROUP")
            workspace_name = os.getenv("AZUREML_NAME")

            # Create an instance of DefaultAzureCredential for authentication
            credential = DefaultAzureCredential()
            

            # Initialize the MLClient object
            ml_client = MLClient(credential, subscription_id, resource_group, workspace_name)
            return ml_client
        
        ml_client = ml_client_project()
        mlflow_tracking_uri = ml_client.workspaces.get(ml_client.workspace_name).mlflow_tracking_uri
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        mlflow.set_experiment(os.getenv("AZUREML_EXPERIMENT_NAME"))

        with mlflow.start_run() as mlfrun:
            # Train the model
            predictor.fit(X_train, y_train)
            # Evaluate the model
            score = predictor.score(X_test, y_test)
            if isinstance(score, dict):
                for key, value in score.items():
                    mlflow.log_metric(key, value)
            else:
                mlflow.log_metric("score", score)

            model = {"processor": processor, "predictor": predictor}
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
            run_id = mlfrun.info.run_id
            # Now register the model
            model_name = f'{config["model_type"]}_{run_id}'

            # Register the model with Azure ML
            registered_model = Model(
                path=f"runs:/{run_id}/model",
                name=model_name,
                description="Model registered from MLflow run.",
                tags={"run_id": run_id},
                type=AssetTypes.MLFLOW_MODEL,
            )
            ml_client.models.create_or_update(registered_model)


    def load_predict(self, config):
        """Load a trained model and predict using it."""
        # Initiate MLClient Project
        ml_client = self.ml_client_project()
        mlflow_tracking_uri = ml_client.workspaces.get(ml_client.workspace_name).mlflow_tracking_uri
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        mlflow.set_experiment(os.getenv("AZUREML_EXPERIMENT_NAME"))
        prefix = os.environ.get("AZUREML_MODEL_NAME")

        # Implement model download
        model_name = f'{prefix}_{config["model_type"]}'

        # Get the model version, if none provided in .env, get the latest version
        model_versions = ml_client.models.list(name=model_name)
        latest_version = max([int(model.version) for model in model_versions])
        model = ml_client.models.get(name=model_name, version=latest_version)

        # Download the model locally (current dir by default)
        download_path = os.path.join(working_dir, model_name)
        ml_client.models.download(name=model_name, version=latest_version, download_path=download_path)

        # Load the downloaded model
        with open(os.path.join(download_path, "model.pkl"), "rb") as f:
            model = pickle.load(f)

        # Get the data processor and preprocess the data
        processor = model["processor"]
        dataframe = pd.read_csv(config["input_data"])
        data = processor.preprocess(dataframe)

        # Get the trained predictor and make predictions
        predictor = model["predictor"]
        y_pred = predictor.predict(data[config["data_params"]["features"]])

        # Combine the predictions with the original data
        final_df = pd.concat([dataframe, pd.DataFrame(data=y_pred, index=dataframe.index, columns=[config["data_params"]["target"]])], axis=1)

        # Post-process the predictions
        final_df = processor.post_process(final_df)

        # Save the predictions to a CSV file
        Utils.write_to_csv(final_df, config["predicted_result_path"])

    def ml_client_project(self):
        """Get the ml_client project."""
        ml_client = MLClient(
            workspace_name=os.getenv("AZUREML_NAME"),
            subscription_id=os.getenv("AZUREML_SUBSCRIPTION_ID"),
            resource_group_name=os.getenv("AZUREML_RESOURCE_GROUP"),
            credential=self.default_credential,
        )
        return ml_client