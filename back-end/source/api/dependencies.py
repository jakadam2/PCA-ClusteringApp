from typing import Annotated

from annotated_types import MinLen
from fastapi import Depends, Body
from pandas import DataFrame
from collections import Counter

from source.api.schemas import UpdateColumnNames, UpdateColumnTypes
from source.clustering.clustering import Clustering
from source.data_set import DataSet
from source.data_type import DataType
from source.exceptions import NonexistentColumnsException, NonNumericColumnsException, NonexistentClusteringID, \
    InvalidMapping
from source.preprocessing.data_transformer import DataTransformer


async def data_dependency():
    """Returns current active dataset."""
    return DataSet().data


async def subset_dependency(
        columns: Annotated[
            list[str],
            MinLen(2),
            Body(
                description="A list of names of columns of a current active dataset.",
                example=["Column A", "Column B"]
            )
        ],
        data: Annotated[DataFrame, Depends(data_dependency)]
) -> DataFrame:
    """Provides a subset of current active dataset."""
    if not set(columns).issubset(data.columns):
        raise NonexistentColumnsException()

    data_subset = data[columns]
    return data_subset


async def numerical_subset_dependency(data_subset: Annotated[DataFrame, Depends(subset_dependency)]) -> DataFrame:
    """Provides a subset of current active dataset and validates that all columns are of numeric type."""
    numerical_columns = DataTransformer.get_numerical_columns(data_subset)
    if len(data_subset.columns) != len(numerical_columns):
        raise NonNumericColumnsException()

    return data_subset


async def clustering_id_dependency(clustering_id: str) -> str:
    """Provides a clustering_id and validates that it is valid."""
    if clustering_id not in Clustering.clusters_cache:
        raise NonexistentClusteringID()

    return clustering_id


async def column_name_mapping_dependency(
        mapping_schema: UpdateColumnNames,
        data: Annotated[DataFrame, Depends(data_dependency)]
) -> dict[str, str]:
    """Provides a valid mapping of old column names to new ones."""
    mapping = mapping_schema.mapping
    old_names = set(mapping.keys())
    new_names = set(mapping.values())

    if duplicates := [column_name for column_name, count in Counter(mapping.values()).items() if count > 1]:
        raise InvalidMapping(f"Column names should be unique. Duplicate names found: {", ".join(duplicates)}")

    if missing_columns := old_names.difference(data.columns):
        raise InvalidMapping(f"Provided columns are not present in the dataset: {", ".join(missing_columns)}")

    if conflicting_names := new_names.intersection(old_names.symmetric_difference(data.columns)):
        raise InvalidMapping(
            f"New column names overlap with already existing column names. Conflicting names: "
            f"{", ".join(conflicting_names)}"
        )

    return mapping


async def column_type_mapping_dependency(
        mapping_schema: UpdateColumnTypes,
        data: Annotated[DataFrame, Depends(data_dependency)]
) -> dict[str, DataType]:
    """Provides a valid mapping of column names to types."""
    mapping = mapping_schema.mapping
    names = set(mapping.keys())

    if missing_columns := names.difference(data.columns):
        raise InvalidMapping(f"Provided columns are not present in the dataset: {missing_columns}")

    return mapping
