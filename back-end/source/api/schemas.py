"""File
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
from typing import List, Union, Dict, Any, Annotated

from fastapi import File
from pandas import DataFrame
from pydantic import BaseModel, Field

from source.clustering.clustering import ClusteringMethod
from source.preprocessing.data_transformer import DataTransformer
from source.data_type import DataType
from source.normalization import CatNormType, NumNormType

ColumnName = Annotated[str, Field(min_length=1, max_length=99)]


class Column(BaseModel):
    name: ColumnName = Field(description="The name of the column.")
    type: DataType = Field(description="The data type of the column.")
    values: List[Union[float, int, bool, str, datetime.datetime]] = Field(description="A list of values contained in "
                                                                                      "the column."
                                                                          )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "age",
                "type": "numerical",
                "values": [25, 30, 45, 60]
            }
        }


class DatasetSchema(BaseModel):
    name: str = Field(description="The name of the dataset.")
    variables: List[Column] = Field(description="A list of columns that make up the dataset.")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "from data_frame",
                "variables": [
                    {
                        "name": "age",
                        "type": "numerical",
                        "values": [25, 30, 45, 60]
                    },
                    {
                        "name": "gender",
                        "type": "categorical",
                        "values": ["male", "female", "female", "male"]
                    }
                ]
            }
        }

    @staticmethod
    def from_data_frame(data: DataFrame) -> 'DatasetSchema':
        categorical = DataTransformer.get_categorical_columns(data)
        numerical = DataTransformer.get_numerical_columns(data)

        variables = [Column(name=column_name,
                            type=DataType.CATEGORICAL if column_name in categorical else
                            DataType.NUMERICAL if column_name in numerical else DataType.DATETIME,
                            values=column.to_list())
                     for column_name, column in data.items()]
        return DatasetSchema(name='from data_frame', variables=variables)


class NormalizationType(BaseModel):
    name: CatNormType | NumNormType = Field(description="The name of the normalization method.")
    compatible_types: List[DataType] | None = Field(default=None,
                                                    description="A list of data types compatible with this "
                                                                "normalization method."
                                                    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "one_hot_encoding",
                "compatible_types": ["categorical"]
            }
        }


class Graph(BaseModel):
    name: str = Field(description="The name of the graph.")
    data: bytes = File(description="The binary data of the graph image.")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "pca_components",
                "data": "plot in a binary form"
            }
        }


class UpdateColumnNames(BaseModel):
    mapping: Dict[ColumnName, ColumnName] = Field(description="A mapping of old column names to new column names.")

    class Config:
        json_schema_extra = {
            "example": {
                "mapping": {
                    "old_column_name1": "new_column_name1",
                    "old_column_name2": "new_column_name2"
                }
            }
        }


class UpdateColumnTypes(BaseModel):
    mapping: Dict[ColumnName, DataType] = Field(description="A mapping of column names to their new data types.")

    class Config:
        json_schema_extra = {
            "example": {
                "mapping": {
                    "column_name1": "numerical",
                    "column_name2": "categorical"
                }
            }
        }


class ClusteringMethodSchema(BaseModel):
    name: ClusteringMethod = Field(description="Name of the clustering method.")
    parameters: dict[str, Any] = Field(description="Parameters for the chosen method.")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mean-shift",
                "parameters": {
                    "param_name1": 1.0,
                    "param_name2": 0.5
                }
            }
        }


class ClusteringStatistics(BaseModel):
    statistics: dict[str, float] = Field(description="[Statistics of the clustering.")

    class Config:
        json_schema_extra = {
            "example": {
                "Silhouette Coefficient": 0.1,
                "Calinski-Harabasz index": 0.5,
                "Davies-Bouldin index": 2.7,
            }
        }
