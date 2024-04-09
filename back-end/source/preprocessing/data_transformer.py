import itertools

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

from source.data_type import DataType
from source.exceptions import ColumnConversionError
from source.normalization import NumNormType, CatNormType
from source.preprocessing.dataprocessing import DataProcessing
from source.preprocessing.normalization import Normalization


class DataTransformer(DataProcessing):

    @staticmethod
    def change_types(dataset: DataFrame, mapping: dict[str, DataType]) -> DataFrame:
        """Change types of columns according to the given mapping of column names to new Datatypes."""
        dataset = dataset.copy()

        for column_name, new_type in mapping.items():
            try:
                match new_type:
                    case DataType.NUMERICAL:
                        dataset[column_name] = DataTransformer._to_numeric(dataset[column_name])
                    case DataType.CATEGORICAL:
                        dataset[column_name] = DataTransformer._to_categorical(dataset[column_name])
                    case DataType.DATETIME:
                        dataset[column_name] = DataTransformer._to_datetime(dataset[column_name])
            except ValueError as ve:
                raise ColumnConversionError(column_name, new_type, str(ve))
        return dataset

    @staticmethod
    def _to_numeric(column: Series):
        if column.dtype == bool:
            return column.astype(int)
        elif column.dtype == np.datetime64:
            return column.map(pd.Timestamp.timestamp)
        else:
            return pd.to_numeric(column, errors="raise")

    @staticmethod
    def _to_categorical(column: Series):
        return pd.Categorical(column)

    @staticmethod
    def _to_datetime(column: Series):
        """Should work both on posix format and OSI like formats."""
        return pd.to_datetime(column, dayfirst=True).map(np.datetime64)

    @staticmethod
    def rename(dataset: DataFrame, mapping: dict[str, str]) -> DataFrame:
        """Renames dataset's columns according to the given mapping."""
        return dataset.rename(columns=mapping)

    @staticmethod
    def normalize(dataset: DataFrame, methods: list[NumNormType | CatNormType]) -> DataFrame:
        """Normalizes data according to the chosen methods, in the same order as in given list."""
        dataset = dataset.copy()

        for method in methods:
            dataset = Normalization.normalize(dataset, method)

        return dataset

    @staticmethod
    def get_normalization_methods() -> list[dict]:
        """Returns list of dictionaries describing normalization methods."""
        return [{"name": method_type, "compatible_types": method_type.compatible_types}
                for method_type in itertools.chain(CatNormType, NumNormType)]
