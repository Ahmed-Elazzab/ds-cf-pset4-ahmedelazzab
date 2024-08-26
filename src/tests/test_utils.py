import os
import tempfile
import unittest

import pandas as pd

from utils import Utils


class TestUtils(unittest.TestCase):
    """Test Cases for utils.py ."""

    expected_result = {
        "training_data": "input_data/kc_house_data.csv",
        "input_data": "input_data/kc_house_data.csv",
        "model_dir": "output/model_registry",
        "predicted_result_path": "output/predictions/predictions.csv",
        "train_model": True,
        "trained_model_file": "model_linear_2023-06-01_173421.pkl",
        "test_size": 0.4,
        "model_type": "linear",
        "data_params": {
            "features": [
                "bedrooms",
                "bathrooms",
                "sqft_living",
                "sqft_lot",
                "floors",
                "waterfront",
                "view",
                "condition",
                "grade",
                "sqft_above",
                "sqft_basement",
                "yr_built",
                "yr_renovated",
                "zipcode",
                "lat",
                "long",
                "sqft_living15",
                "sqft_lot15",
            ],
            "target": ["price"],
        },
    }

    def test_load_configuration_success(self):
        """
        Test the successful loading of configuration.

        This unit test ensures that the configuration is loaded correctly
        and matches the expected result.

        The configuration file path is provided, and the `get_config()` method
        is called to retrieve the configuration settings. Assertions are made
        to check the type, length, and content of the returned configuration.

        Raises:
            AssertionError: If any of the assertions fail.
        """
        # Define the configuration file path
        config_file = "config.yaml"
        # Get the configuration settings
        config = Utils.get_config(config_file)
        # Assert that the returned result is a dictionary
        self.assertIsInstance(config, dict)
        # Assert that the length of the result matches the expected length
        self.assertEqual(len(config), len(self.expected_result))
        # Assert that the result matches the expected result
        self.assertDictEqual(config, self.expected_result)

    def test_write_to_csv(self):
        """Save the predictions to a csv file."""
        # make a temporary folder
        with tempfile.TemporaryDirectory() as tempdir:
            # create a dummy dataframe
            df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
            # write the dataframe to a csv file
            path = os.path.join(tempdir, "test.csv")
            Utils.write_to_csv(df, path)
            # read the csv file
            df_read = pd.read_csv(path)
            # assert that the csv file is not empty
            self.assertGreater(os.path.getsize(path), 0)
            # assert that the csv file has the correct number of rows and columns
            self.assertEqual(df.shape, df_read.shape)
            # assert that the csv file has the correct content
            self.assertEqual(df.values.tolist(), df_read.values.tolist())

    def test_generate_model_path(self):
        """Generate a model path."""
        # make a timestamp
        timestamp = "2023-06-01_173421"
        # expected result
        expected_path = "model_dir/model_linear_2023-06-01_173421.pkl"
        # generate a model path
        config = {"model_dir": "model_dir", "model_type": "linear"}
        path = Utils.generate_model_path(config, timestamp)
        # assert that the model path is correct
        self.assertEqual(expected_path, path)

    def test_save_load_pkl(self):
        """Save a pickle file."""
        # make a temporary folder
        tempdir = tempfile.TemporaryDirectory()
        # create a dummy dataframe
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        # save the dataframe to a pickle file
        path = os.path.join(tempdir.name, "test.pkl")
        Utils.save_pkl(df, path)
        # assert that the pickle file is not empty
        self.assertGreater(os.path.getsize(path), 0)
        # load the pickle file
        loaded_df = Utils.load_pkl(path)
        # assert that the pickle file has the correct content
        self.assertEqual(df.values.tolist(), loaded_df.values.tolist())
        # remove the temporary folder
        tempdir.cleanup()
