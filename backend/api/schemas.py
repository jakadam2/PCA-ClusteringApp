"""
// DTOs
variable = {
    "id":int,
    "name":string,
    "typeId":int,
    "values":[double]
    }

dataset = {
    "datasetname":string,
    "variables":[variable],
    }

dataType = {
    "id":int,
    "name":string
    }

normalizationMethod = {
    "id":int,
    "name":string
    }

clusteringAlgorithm = {
    "id":int,
    "name":string
    }

clusteringDescription = {
    "graph":image,
    "description":string
    }
"""
import datetime

from fastapi import File
from pandas import DataFrame
from pydantic import BaseModel

from backend.clustering import ClusteringMethod
from backend.data_type import DataType
from backend.normalization import CatNormType, NumNormType


class Column(BaseModel):
    name: str
    type: DataType
    values: list[float | int | bool | str | datetime.datetime]


class DatasetSchema(BaseModel):
    name: str
    variables: list[Column]

    @staticmethod
    def from_data_frame(data: DataFrame) -> 'DatasetSchema':
        variables = [Column(name = column_name,
                            type = DataType.CATEGORICAL if data[column_name].dtype == 'object' else DataType.NUMERICAL,
                            values = data[column_name].to_list()) 
                            for column_name in data.columns]
        return DatasetSchema(name='from data_frame',variables=variables)



class NormalizationType(BaseModel):
    name: CatNormType | NumNormType
    compatible_types: list[DataType]



class Graph(BaseModel):
    name: str
    data: bytes = File(...)


class UpdateColumnNames(BaseModel):
    mapping: dict[str, str]


class UpdateColumnTypes(BaseModel):
    mapping: dict[str, DataType]
