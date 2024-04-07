import numpy as np
from pandas import DataFrame


class DataProcessing:

    @classmethod
    def get_numerical_columns(cls, dataset: DataFrame) -> list[str]:
        """Returns list of columns solely containing numerical data."""
        return dataset.select_dtypes(include=np.number).columns.to_list()

    @classmethod
    def get_datetime_columns(cls, dataset: DataFrame) -> list[str]:
        """Returns list of columns solely containing datetime data."""
        return dataset.select_dtypes(include=['datetime', 'timedelta']).columns.to_list()

    @classmethod
    def get_categorical_columns(cls, dataset: DataFrame) -> list[str]:
        """Returns list of columns solely containing categorical(non numeric) data."""
        return dataset.select_dtypes(include='object', exclude=['datetime', 'timedelta']).columns.to_list()

