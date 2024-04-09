from pathlib import Path

import pandas as pd
from pandas import DataFrame
from pandas.errors import ParserError, EmptyDataError

from fastapi import UploadFile

from source.exceptions import NoActiveDataset, InvalidFileExtension, EmptyFileException, NaNValuesException


class DataSetImplementation:
    """Implements all of functionalities of DataSet but it is not singleton"""

    def __init__(self) -> None:
        self._data_set: pd.DataFrame | None = None
        self._previous_data_set: pd.DataFrame | None = None
        self._name: str | None = None
        self.age: int = 0

    def load_data(self, file: UploadFile) -> None:
        """Loads DataFrame from DatasetSchema object"""
        dataset = self.safe_read(file)

        for column in dataset.columns[dataset.dtypes == 'object']:
            try:
                dataset[column] = pd.to_datetime(dataset[column])
            except (ParserError, ValueError):
                pass

        self._data_set = dataset

    def safe_read(self, file: UploadFile, expected_extension: str = ".csv") -> DataFrame:
        """Validates and reads given file, raising HTTP errors in case of invalid file, returns loaded file"""
        file_extension = Path(file.filename).suffix
        if file_extension != expected_extension:
            raise InvalidFileExtension(expected_extension, file_extension)

        try:
            data = pd.read_csv(file.file, sep=";", decimal=",")
        except EmptyDataError:
            raise EmptyFileException(file.filename)

        if data.isnull().any(axis=None):
            raise NaNValuesException()

        return data

    @property
    def data(self) -> pd.DataFrame:
        """Property to get DataFrame with going back mechanism"""
        if self._data_set is None:
            raise NoActiveDataset()
        return self._data_set

    @data.setter
    def data(self, new_data: pd.DataFrame) -> None:
        self.age += 1
        self._previous_data_set = self._data_set
        self._data_set = new_data

    @property
    def has_null(self) -> bool:
        """Returns true if DataSet contains at least one missing value"""
        return self._data_set.isnull().any(axis=None)

    def get_types(self) -> pd.Series:
        """Returns types of each column"""
        return self._data_set.dtypes

    def get_info(self) -> pd.Series:
        """Returns short summary of data"""
        return self._data_set.describe(include='all')

    def get_head(self, rows: int = 10) -> pd.DataFrame:
        """Returns first "rows" rows of data """
        return self._data_set.head(n=rows)


class DataSet:
    """Singleton version of DataSetImplementation"""
    _impl: DataSetImplementation = None

    def __new__(cls, *args, **kwargs) -> DataSetImplementation:
        if cls._impl is None:
            cls._impl = DataSetImplementation(*args, **kwargs)
        return cls._impl
