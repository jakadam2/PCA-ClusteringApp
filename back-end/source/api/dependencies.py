from typing import Annotated

from annotated_types import MinLen
from fastapi import Depends, Body
from pandas import DataFrame

from source.clustering.clustering import Clustering
from source.data_set import DataSet
from source.exceptions import NonexistentColumnsException, NonNumericColumnsException, NonexistentClusteringID
from source.preprocessing.data_transformer import DataTransformer


async def subset_dependency(
        columns: Annotated[
            list[str],
            MinLen(2),
            Body(
                description="A list of names of columns of a current active dataset.",
                example=["Column A", "Column B"]
            )
        ]
) -> DataFrame:
    """Provides a subset of current active dataset."""
    if not set(columns).issubset(DataSet().data.columns):
        raise NonexistentColumnsException()

    data_subset = DataSet().data[columns]
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
