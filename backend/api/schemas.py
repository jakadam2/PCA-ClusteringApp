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
from pydantic import BaseModel, TypeAdapter

from backend.clustering import ClusteringMethod
from backend.data_type import DataType
from backend.normalization import CatNormType, NumNormType


class Column(BaseModel):
    name: str
    type: DataType
    values: list[float | int | bool | str | datetime.datetime]


# TODO add from dataframe method
class DatasetSchema(BaseModel):
    name: str
    variables: list[Column]

    @staticmethod
    def from_data_frame(data: DataFrame) -> 'DatasetSchema':
        return DatasetSchema()


DataTypeAdapter = TypeAdapter(DataType)


class NormalizationType(BaseModel):
    name: CatNormType | NumNormType
    compatible_types: list[DataType]


ClusteringAlgorithm = TypeAdapter(ClusteringMethod)


class Graph(BaseModel):
    name: str
    data: bytes = File(...)


class UpdateColumnNames(BaseModel):
    mapping: dict[str, str]


class UpdateColumnTypes(BaseModel):
    mapping: dict[str, DataType]
