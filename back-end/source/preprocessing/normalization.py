import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import RobustScaler, MinMaxScaler, StandardScaler, OrdinalEncoder, OneHotEncoder

from source.data_type import DataType
from source.normalization import NormalizationType
from source.preprocessing.dataprocessing import DataProcessing


class Normalization(DataProcessing):
    @classmethod
    def normalize(cls, dataset: DataFrame, method: NormalizationType):
        method_callable = getattr(cls, f"_{method.value}", None)

        if callable(method_callable):
            return method_callable(dataset, method)

        raise ValueError(f"Unsupported normalization method encountered: {method}")

    @classmethod
    def apply_scikit_transformer(cls, dataset: DataFrame, transformer, data_types: list[DataType], **kwargs):
        """Applies given transformer to the data, modifying it in place when possible."""
        column_names = []

        if DataType.NUMERICAL in data_types:
            column_names += cls.get_numerical_columns(dataset)
        if DataType.CATEGORICAL in data_types:
            column_names += cls.get_categorical_columns(dataset)
        if DataType.DATETIME in data_types:
            column_names += cls.get_datetime_columns(dataset)

        data_subset = dataset[column_names]
        dataset[column_names] = transformer.fit_transform(data_subset, dict(copy=False, **kwargs))
        return dataset

    @staticmethod
    def _one_hot_encoding(dataset: DataFrame, method: NormalizationType) -> DataFrame:
        """One hot encodes columns with categorical data."""
        return pd.get_dummies(dataset)

    @staticmethod
    def _ordinal_encoding(dataset: DataFrame, method: NormalizationType):
        """Performs ordinal encoding."""
        return Normalization.apply_scikit_transformer(dataset, OrdinalEncoder(), method.compatible_types)

    @staticmethod
    def _standardization(dataset: DataFrame, method: NormalizationType) -> DataFrame:
        """Standardizes numerical data to have a mean of 0 and a standard deviation of 1."""
        return Normalization.apply_scikit_transformer(dataset, StandardScaler(), method.compatible_types)

    @staticmethod
    def _min_max_scaling(dataset: DataFrame, method: NormalizationType) -> DataFrame:
        """Performs min max scaling."""
        return Normalization.apply_scikit_transformer(dataset, MinMaxScaler(), method.compatible_types)

    @staticmethod
    def _robust_scaling(dataset: DataFrame, method: NormalizationType) -> DataFrame:
        """Performs robust scaling."""
        return Normalization.apply_scikit_transformer(dataset, RobustScaler(), method.compatible_types)
