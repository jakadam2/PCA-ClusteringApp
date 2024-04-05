import numpy as np
import pandas as pd
from pandas import DataFrame, Series

from source.data_type import DataType
from source.normalization import NumNormType, CatNormType


class DataTransformer:

    @staticmethod
    def change_types(dataset: DataFrame, mapping: dict[str, DataType]) -> DataFrame:
        """Change types of columns according to the given mapping of column names to new Datatypes."""
        dataset = dataset.copy()

        for column_name, new_type in mapping.items():
            match new_type:
                case DataType.NUMERICAL:
                    dataset[column_name] = DataTransformer._to_numeric(dataset[column_name])
                case DataType.CATEGORICAL:
                    dataset[column_name] = DataTransformer._to_categorical(dataset[column_name])
                case DataType.DATETIME:
                    dataset[column_name] = DataTransformer._to_datetime_unix(dataset[column_name])

        return dataset

    @staticmethod
    def _to_numeric(column: Series):
        if column.dtype == bool:
            return column.astype(int)
        else:
            return pd.to_numeric(column, errors="coerce")

    @staticmethod
    def _to_categorical(column: Series):
        return pd.Categorical(column)

    @staticmethod
    def _to_datetime_unix(column: Series):
        if column.dtype == object:
            return pd.to_datetime(column).map(pd.Timestamp.timestamp)

    @staticmethod
    def rename(dataset: DataFrame, mapping: dict[str, str]) -> DataFrame:
        """Renames dataset's columns according to the given mapping."""
        return dataset.rename(columns=mapping)

    @staticmethod
    def normalize(dataset: DataFrame, methods: list[NumNormType | CatNormType]) -> DataFrame:
        """Normalizes data according to the chosen methods, in the same order as in given list."""
        dataset = dataset.copy()
        for method in methods:
            match method:
                case NumNormType.STANDARDIZATION:
                    dataset = DataTransformer.standardize(dataset)
                case CatNormType.ONE_HOT:
                    dataset = DataTransformer.one_hot_encoding(dataset)

        return dataset

    @staticmethod
    def one_hot_encoding(dataset: DataFrame) -> DataFrame:
        """One hot encodes columns with categorical data."""
        return pd.get_dummies(dataset)

    @staticmethod
    def standardize(dataset: DataFrame) -> DataFrame:
        """Standardizes numerical data to have a mean of 0 and a standard deviation of 1."""
        numerical_column_names = DataTransformer.get_numerical_columns(dataset)
        numerical_columns = dataset[numerical_column_names]
        dataset[numerical_column_names] = (numerical_columns - numerical_columns.mean()) / numerical_columns.std()
        return dataset

    @staticmethod
    def get_numerical_columns(dataset: DataFrame):
        """Returns list of columns solely containing numerical data."""
        return dataset.select_dtypes(include=np.number).columns

    @staticmethod
    def get_datetime_columns(dataset: DataFrame):
        """Returns list of columns solely containing datetime data."""
        return dataset.select_dtypes(include='datetime').columns

    @staticmethod
    def get_categorical_columns(dataset: DataFrame):
        """Returns list of columns solely containing categorical(non numeric) data."""
        return dataset.columns.difference(DataTransformer.get_numerical_columns(dataset))

    @staticmethod
    def get_normalization_methods() -> list[dict]:
        """Returns list of dictionaries describing normalization methods."""
        response = []

        for method_type in CatNormType:
            response.append({"name": method_type, "compatible_types": [DataType.CATEGORICAL]})

        for method_type in NumNormType:
            response.append({"name": method_type, "compatible_types": [DataType.NUMERICAL, DataType.DATETIME]})

        return response
