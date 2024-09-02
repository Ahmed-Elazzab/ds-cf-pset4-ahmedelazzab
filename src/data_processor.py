import logging
import numpy
from sklearn.preprocessing import StandardScaler
from great_expectations import expectations as ge
import pandas as pd
# from dnalib.custom_expectations import NumericPandasExpectations

logger = logging.getLogger(__name__)



class DataProcessor:
    """A class for performing data processing operations on a DataFrame."""

    def __init__(self, config):
        """
        Initialize the DataProcessor class.

        Args:
            config (dict): The configuration settings.
        """
        # initialize required variables...
        self.y_col = config["data_params"]["target"]
        self.num_cols = None
        self.cat_cols = None
        self.X_scaler = None
        self.y_scaler = None

    def fit(self, dataframe):
        # Implement the training logic here
        # For example, calculate mean and std for normalization
        self.means = dataframe.mean()
        self.stds = dataframe.std()
        self.trained = True

    def preprocess(self, dataframe):
        """
        Execute the data processing operations.

        Args:
            data (DataFrame): The DataFrame to process.
        """
        if dataframe is None:
            raise ValueError("Input data is None.")
        
        # 1. Filter out the numerical columns from the dataframe.
        self.num_cols = dataframe.select_dtypes(include=numpy.number).columns.tolist()
        # 2. Filter out the categorical columns from the dataframe.
        self.cat_cols = dataframe.select_dtypes(exclude=numpy.number).columns.tolist()
        # 3. Call remove null function on your data
        dataframe = self.remove_nulls(dataframe)
        # 4. Call remove duplicate function on your data
        dataframe = self.remove_duplicates(dataframe)
        # 5. Call remove standard Scale function on your data
        dataframe = self.standard_scale(dataframe)
        return dataframe

    def post_process(self, dataframe):
        """
        Execute the post-processing operations.

        Inverse the scaling operations the target column.
        The goal of this function is to make the output "human-readable".

        Args:
        data (DataFrame): The DataFrame to process.

        Steps:
          1. Implement the logic to inverse the standard scaling
             to generate output in "human-readable" format.
          2. return updated dataframe
        """
        # implementation for the logic inverse the standard scaling
        dataframe[self.y_col] = self.y_scaler.inverse_transform(dataframe[self.y_col].values.reshape(-1, 1))
        return dataframe

    def remove_nulls(self, dataframe):
        """
        Remove null values from specified columns in the DataFrame.

        Args:
            data (DataFrame): The DataFrame to process.

        Raises:
            KeyError: If the specified columns are not found in the DataFrame.
        """
        # the logic to remove null values
        null_less_data = dataframe.dropna()

        return null_less_data

    def remove_duplicates(self, dataframe):
        """
        Remove duplicate rows from the DataFrame.

        Args:
            data (pandas.DataFrame): The DataFrame to save.

        Raises:
            KeyError: If the specified columns are not found in the DataFrame.
        """
        # write logic to remove duplicate rows from all columns and return updated dataframe
        no_duplicates = dataframe.drop_duplicates()
        return no_duplicates

    def standard_scale(self, dataframe):
        """
        Scale the data using StandardScaler.

        Args:
            data (DataFrame): The DataFrame to scale.
        """
        # 1. Implement the logic to scale the features and target column to standard Scale.
        # 2. Keep in mind that you have to apply the same scale on prediction data
        # 3. return updated data

        # Initialize the scaler if not already initialized
        if self.X_scaler is None:
            self.X_scaler = StandardScaler()
            self.X_scaler.fit(dataframe[self.num_cols])

        # Apply standard scaling to the numerical columns
        dataframe[self.num_cols] = self.X_scaler.transform(dataframe[self.num_cols])

        # Initialize the scaler for the target column if not already initialized
        if self.y_scaler is None:
            self.y_scaler = StandardScaler()
            self.y_scaler.fit(dataframe[self.y_col])

        # Apply standard scaling to the target column
        dataframe[self.y_col] = self.y_scaler.transform(dataframe[self.y_col])
        return dataframe
    
    #This is just to show concept of great expectations i repeated the unittest but in reality the docuemntation has various tools
    def pre_validation(self, dataframe):
        """Validate data before applying any transformations."""
        self.num_cols = dataframe.select_dtypes(include=numpy.number).columns.tolist()
        # 2. Filter out the categorical columns from the dataframe.
        self.cat_cols = dataframe.select_dtypes(exclude=numpy.number).columns.tolist()
        for column in self.num_cols:
            ge.ExpectColumnValuesToBeOfType(column=column, type_="float")
        # Create expactations
        for column in self.cat_cols:
            ge.ExpectColumnValuesToBeOfType(column=column, type_="str")
        return dataframe



    def post_validation(self, dataframe):
        """Validate data before applying any transformations."""
        self.num_cols = dataframe.select_dtypes(include=numpy.number).columns.tolist()
        # 2. Filter out the categorical columns from the dataframe.
        self.cat_cols = dataframe.select_dtypes(exclude=numpy.number).columns.tolist()
        for column in self.num_cols:
            ge.ExpectColumnValuesToBeOfType(column=column, type_="float")
        # Create expactations
        for column in self.cat_cols:
            ge.ExpectColumnValuesToBeOfType(column=column, type_="str")
        return dataframe