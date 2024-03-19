import pandas as pd
import numpy as np


class DataSetImplementation:
    """
    Implements all of functionalities of DataSet but it isn not singleton
    """

    def __init__(self) -> None:
        self._data_set: pd.DataFrame | None = None

    def load_data(self, data_path: str, separator: str = ';') -> None:
        self._data_set = pd.read_csv(data_path, sep=separator)

    def save_data(self, data_path: str, separator: str = ';') -> None:
        self._data_set.to_csv(data_path, sep=separator)

    def get_types(self) -> pd.Series:
        return self._data_set.dtypes

    def get_info(self) -> pd.Series:
        return self._data_set.describe(include='all')

    def get_head(self, rows: int = 10) -> pd.DataFrame:
        return self._data_set.head(n=rows)


class DataSet:
    _impl = None

    def __new__(cls, *args, **kwargs) -> DataSetImplementation:
        if cls._impl is None:
            cls._impl = DataSetImplementation(*args, **kwargs)
        return cls._impl
