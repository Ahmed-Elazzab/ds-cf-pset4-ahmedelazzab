"""Module with tests for the data processor."""

import unittest

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from src.data_processor import DataProcessor
from src.utils import Utils


class DataProcessorTestCase(unittest.TestCase):
    """Test case for the DataPreProcessor class."""

    def setUp(self):
        """Setup Method."""
        # Load configuration from a YAML file
        self.config = Utils().get_config("config.yaml")
        # make a dataframe that has null values
        self.input_df = pd.DataFrame(
            {
                "x1": [1.0, 1.0, 3.0, 4.0, np.nan],
                "x2": [6.0, 6.0, np.nan, 9.0, 10.0],
                "y": [11.0, 11.0, 13.0, 14.0, 15.0],
            }
        )
        self.config["data_params"]["features"] = ["x1", "x2"]
        self.config["data_params"]["target"] = ["y"]
        self.data_processor = DataProcessor(self.config)
        self.data_processor.num_cols = ["x1", "x2", "y"]
        self.data_processor.cat_cols = []

    def test_remove_nulls(self):
        """Test the removal of columns with null values in the DataProcessor class."""
        expected_df = pd.DataFrame(
            {
                "x1": [1.0, 1.0, 4.0],
                "x2": [6.0, 6.0, 9.0],
                "y": [11.0, 11.0, 14.0],
            }
        )

        # Perform removal of null values in the DataFrame
        output_df = self.data_processor.remove_nulls(self.input_df.copy())
        # Assert that the DataFrame has no null values
        self.assertFalse(output_df.isnull().any().any())
        # compare the expected and output dataframes
        self.compare_dfs(expected_df, output_df)

    def test_remove_duplicates(self):
        """Test the removal of duplicate rows in specified columns using the DataProcessor class."""

        # Perform removal of duplicate rows in the DataFrame
        output_df = self.data_processor.remove_duplicates(self.input_df.copy())
        expected_df = self.data_processor.remove_duplicates(self.input_df.copy())
        # assert there are no duplicate rows
        self.assertFalse(output_df.duplicated().any())
        # compare the expected and output dataframes
        self.compare_dfs(expected_df, output_df)

    def test_standard_scale(self):
        """Test Standard Scale."""
        expected_df = pd.DataFrame(
            {
                "x1": [
                    -0.9622504486493763,
                    -0.9622504486493763,
                    0.5773502691896257,
                    1.3471506281091268,
                    np.nan,
                ],
                "x2": [
                    -0.9801960588196068,
                    -0.9801960588196068,
                    np.nan,
                    0.7001400420140048,
                    1.2602520756252087,
                ],
                "y": [
                    -1.1250000000000004,
                    -1.1250000000000004,
                    0.12499999999999956,
                    0.7499999999999996,
                    1.3749999999999996,
                ],
            }
        )
        # Perform standard scaling on the DataFrame
        output_df = self.data_processor.standard_scale(self.input_df)

        # compare the expected and output dataframes
        self.compare_dfs(expected_df, output_df)

    def compare_dfs(self, expected_df, output_df):
        """Compare df test."""
        # Reset the index of the DataFrames
        expected_df.reset_index(drop=True, inplace=True)
        output_df.reset_index(drop=True, inplace=True)
        # Assert that the DataFrame is equeal to the expected DataFrame
        # using the pandas testing function
        assert_frame_equal(expected_df, output_df)

        # Assert that the DataFrame has the expected shape
        self.assertEqual(expected_df.shape, output_df.shape)

        # Assert that the DataFrame has the expected columns
        self.assertEqual(expected_df.columns.tolist(), output_df.columns.tolist())

        # Assert that the DataFrame has the expected data types
        self.assertEqual(expected_df.dtypes.tolist(), output_df.dtypes.tolist())

    def test_preprocess_not_trained(self):
        """Test the preprocessing function when the preprocessor is not trained."""
        expected_df = pd.DataFrame(
            {
                "x1": [-1.0, 1.0],
                "x2": [-1.0, 1.0],
                "y": [-1.0, 1.0],
            }
        )
        # Call the preprocessing function
        output_df = self.data_processor.preprocess(self.input_df)
        # compare the expected and output dataframes
        self.compare_dfs(expected_df, output_df)
