import logging
from datetime import datetime

from dotenv import load_dotenv

from orchestrators.cloud_orchestrator import CloudOrchestrator
from orchestrators.local_orchestrator import LocalOrchestrator
from predictors.lr_predictor import LinearModel
from predictors.svm_predictor import SVMModel
from utils import Utils

load_dotenv(".env")


"""Create a dictionary that maps the string keys to corresponding model classes. i.e LinearModel and SVM. these string should be respective of what model we have defined in the config.yml file. all '...' to be implemented"""
PREDICTORS_LOOKUP = {"linear": LinearModel, "SVM": SVMModel}

"""Create a dictionary that maps the string keys to corresponding Platform classes. i.e local and cloud. these string should be respective of what cloud platform we have defined in the config.yml file. all '...' to be implemented"""
ORCHESTRATOR_LOOKUP = {"local": LocalOrchestrator, "cloud": CloudOrchestrator}

""" Implement the configuration for logging in the project here. it should add a log file in the output/logs/abc.log Log file should contain logs of complete journey of training and predicting model. The name of the log file should be like this. log-2023-06-06_200011.log, all '...' to be filled"""
TIME_STAMP = datetime.now().strftime("%Y-%m-%d_%H%M%S")
log_filename = f"log-{TIME_STAMP}.log"
logging.basicConfig(filename=f"output/logs/{log_filename}", level=logging.INFO)
logging.info("Running Urban Planning")
logger = logging.getLogger("urbanGUIda")
logger = logging.getLogger(__name__)


def run():
    """Main method responsible running the model."""
    # Load the configuration using Configuration class

    # Get the configuration from the Utils class
    config = Utils.get_config("config.yaml")
    if config is None:
        raise ValueError("Failed to load configuration.")
    # Create a predictor instance based on the model_type
    if config["model_type"] in PREDICTORS_LOOKUP:
        predictor = PREDICTORS_LOOKUP[config["model_type"]]()
    # Create an instance of the orchestrator based on the platform
    if config["platform"] in ORCHESTRATOR_LOOKUP:
        orchestrator = ORCHESTRATOR_LOOKUP[config["platform"]]()
    # run the orchestrator
    orchestrator.run(config, predictor)


if __name__ == "__main__":
    """
    Entry point of the script. Calls the run_model function.
    """
    run()
