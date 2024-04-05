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

from annotated_types import MinLen
from fastapi import File, Body
from pandas import DataFrame
from pydantic import BaseModel, Field

from source.clustering.clustering import ClusteringMethod
from source.data_transformer import DataTransformer
from source.data_type import DataType
from source.normalization import CatNormType, NumNormType


class Column(BaseModel):
    name: str = Field(..., description="The name of the column.")
    type: DataType = Field(..., description="The data type of the column.")
    values: List[Union[float, int, bool, str, datetime.datetime]] = Field(...,
                                                                          description="A list of values contained in "
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
    name: str = Field(..., description="The name of the dataset.")
    variables: List[Column] = Field(..., description="A list of columns that make up the dataset.")

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
    name: CatNormType | NumNormType = Field(..., description="The name of the normalization method.")
    compatible_types: List[DataType] = Field(...,
                                             description="A list of data types compatible with this normalization "
                                                         "method."
                                             )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "one_hot",
                "compatible_types": ["categorical"]
            }
        }


class Graph(BaseModel):
    name: str = Field(..., description="The name of the graph.")
    data: bytes = File(..., description="The binary data of the graph image.")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "pca_components",
                "data": "plot in a binary form"
            }
        }


class UpdateColumnNames(BaseModel):
    mapping: Dict[str, str] = Field(..., description="A mapping of old column names to new column names.")

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
    mapping: Dict[str, DataType] = Field(..., description="A mapping of column names to their new data types.")

    class Config:
        json_schema_extra = {
            "example": {
                "mapping": {
                    "column_name1": "numerical",
                    "column_name2": "categorical"
                }
            }
        }


Columns = Annotated[
    list[str],
    MinLen(2),
    Body(
        description="A list of names of columns of a current active dataset.",
        example=["Column A", "Column B"]
    )
]

ClusteringMethodSchema = Annotated[
    ClusteringMethod,
    Body(description="Name of the clustering method.", example="Mean-shift")
]

MethodParameters = Annotated[
    dict[str, Any],
    Body(
        description="Parameters for the chosen method.",
        example={
            "param_name1": 1.0,
            "param_name2": 0.5
        }
    ),
]
