from pathlib import Path

import pandas as pd
import numpy as np
from pandas.errors import ParserError

from pandas import DataFrame
from pandas.errors import ParserError, EmptyDataError

from fastapi import UploadFile

from source.exceptions import NoActiveDataset, InvalidFileExtension, EmptyFileException, NaNValuesException


class DataSet:
    """Implements all of functionalities of DataSet but it is not singleton"""
    _data_set:pd.DataFrame|None = None
    _previous_data_set:pd.DataFrame|None = None
    age = -1

    @staticmethod
    def load_data(file: UploadFile) -> None:
        """Loads DataFrame from DatasetSchema object"""
        dataset = DataSet.safe_read(file)

        for column in dataset.columns[dataset.dtypes == 'object']:
            try:
                dataset[column] = pd.to_datetime(dataset[column])
            except (ParserError, ValueError):
                pass

        DataSet._data_set = dataset

    @staticmethod
    def safe_read(file: UploadFile, expected_extension: str = ".csv") -> DataFrame:
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
        if DataSet._data_set is None:
            raise NoActiveDataset()
        return DataSet._data_set

    @data.setter
    def data(self, new_data: pd.DataFrame) -> None:
        DataSet.age += 1
        DataSet._previous_data_set = self._data_set
        DataSet._data_set = new_data


    @property
    def has_null(self) -> bool:
        """Returns true if DataSet contains at least one missing value"""
        return DataSet._data_set.isnull().any(axis=None)

    @staticmethod
    def get_types() -> pd.Series:
        """Returns types of each column"""
        return DataSet._data_set.dtypes

    @staticmethod
    def get_info() -> pd.Series:
        """Returns short summary of data"""
        return DataSet._data_set.describe(include='all')

    @staticmethod
    def get_head( rows: int = 10) -> pd.DataFrame:
        """Returns first "rows" rows of data """
        return DataSet._data_set.head(n=rows)

