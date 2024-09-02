import logging
import os
import pickle

import yaml

logger = logging.getLogger(__name__)


class Utils:
    """A class for util methods."""

    @staticmethod
    def get_config(config_file):
        """
        Load the configuration from the YAML file.

        Args:
            config_file (str): Path to the config file.

        Returns:
            dict: The loaded configuration as a dictionary.

        Raises:
            Exception: If the config file is not found.
        """
        """Instruction """

        logger.info("Load config.yaml and loading setup")
        # 1. Implement the logic to load the configuration from the YAML file.
        # 2. Return the configuration nested dictionary
        # 3. If the config file is not found, raise an Exception with an appropriate message.
        try:
            with open(config_file, "r") as file:
                config = yaml.safe_load(file)
            logger.info("Configuration loaded successfully.")
            return config
        except FileNotFoundError:
            logger.error("Config file not found.")
            raise Exception("Config file not found.")

    @staticmethod
    def write_to_csv(dataframe, path):
        """
        Save the DataFrame to a CSV file.

        Args:
            dataframe (pandas.DataFrame): The DataFrame to save.
            path (str): Path to the output CSV file.

        Raises:
            IOError: If there is an error while saving the DataFrame to CSV.
        """
        """Instruction """
        # 1. Implement the logic to save the dataframe to CSV File Format.
        # 2. If there's any Error in saving to csv file please raise IO Exception
        try:
            dataframe.to_csv(path, index=False)
            logger.info("Dataframe successfully saved to CSV.")
        except IOError as e:
            logger.error(f"An error occurred while saving the dataframe to CSV: {str(e)}")

    @staticmethod
    def generate_model_path(config, time_stamp):
        """
        Generate the path for saving the model.

        Args:
            config (dict): Configuration dictionary containing model information.
            time_stamp (str): Timestamp to append to the model name.

        Returns:
            str: The path for saving the model.

        Raises:
            KeyError: If the required keys are not found in the config dictionary.
        """
        # Use model_type, model_dir from config and current timestamp to create model path.
        # It should be like output/model_registry/svm.pk
        try:
            model_dir = config["model_dir"]
            model_type = config["model_type"]
            return os.path.join(model_dir, f"model_{model_type}_{time_stamp}.pkl")
        except KeyError as e:
            logger.error(f"Required keys not found in the config dictionary: {str(e)}")
            raise KeyError("Required keys not found in the config dictionary.")

    @staticmethod
    def save_pkl(predictor_ins, path):
        """Save the model to the specified path as a pickle file.

        Args:
            predictor_ins: The predictor instance or object to be saved.
            path (str): The file path where the model will be saved.

        Raises:
            IOError: If an input/output error occurs while saving the model.
            Exception: If any other unexpected error occurs.
        """
        """Instruction """
        # 1.  Use the pickle library to prediction class instance to .pkl file.
        # 2. If there's any Error in saving file please raise IO Exception
        try:
            with open(path, "wb") as file:
                pickle.dump(predictor_ins, file)
            logger.info("Model successfully saved as pickle.")
        except IOError as e:
            logger.error(f"An error occurred while saving the model: {str(e)}")
        except Exception as e:
            logger.error(f"An error occurred while saving the model: {str(e)}")

    @staticmethod
    def load_pkl(path):
        """Load the model from the specified path as a pickle file.

        Args:
            path (str): The file path from which to load the model.

        Returns:
            The loaded model object.

        Raises:
            FileNotFoundError: If the specified file path does not exist.
            IOError: If an input/output error occurs while loading the model.
            pickle.UnpicklingError: If an error occurs during the unpickling process.
            Exception: If any other unexpected error occurs.
        """
        """Instruction """
        # 1. Implement the logic to lead the pickle file from the path and return the class object.
        # 2. If there's any Error in loading file please raise FileNotFoundError, IO and Exceptions
        try:
            with open(path, "rb") as file:
                model = pickle.load(file)
            return model
        except FileNotFoundError as e:
            logger.error(f"File not found error occurred while loading the model: {str(e)}")
        except IOError as e:
            logger.error(f"An error occurred while loading the model: {str(e)}")
        except pickle.UnpicklingError as e:
            logger.error(f"Error occurred while unpickling the model: {str(e)}")
        except Exception as e:
            logger.error(f"An error occurred while loading the model: {str(e)}")
