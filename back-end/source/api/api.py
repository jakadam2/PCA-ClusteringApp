from typing import Annotated

from fastapi import APIRouter, Query, UploadFile, File, Depends
from fastapi.responses import Response, JSONResponse
from pandas import DataFrame

from source.api.dependencies import numerical_subset_dependency, clustering_id_dependency
from source.api.schemas import DatasetSchema, UpdateColumnNames, UpdateColumnTypes, NormalizationType, \
    ClusteringMethodSchema, ClusteringStatistics, Column
from source.clustering.clustering import Clustering, ClusteringMethod
from source.clustering.clustering_interactive import ClusteringInteractive
from source.data_set import DataSet
from source.preprocessing.data_transformer import DataTransformer
from source.data_type import DataType
from source.pca import PCA

router = APIRouter(prefix="/api")


@router.post("/file", summary="Upload a dataset")
async def post_dataset(file: UploadFile = File(...)):
    """
    ## Upload a dataset file in CSV format.

    Uploaded dataset becomes currently active dataset.
    The CSV file should be delimited by semicolons (;).
    """
    DataSet().load_data(file)
    return JSONResponse('Uploaded',201) if not DataSet().has_null else JSONResponse('Data cannot contain missing values',400)


@router.get("/file", summary="Retrieve the dataset", response_model=DatasetSchema)
async def get_dataset():
    """
    ## Retrieve the entire dataset schema.

    This endpoint returns the schema of the currently active dataset.
    """
    return DatasetSchema.from_data_frame(DataSet().data)


@router.get("/dataset", summary="Get dataset head", response_model=DatasetSchema)
async def get_head(rows: Annotated[int, Query(gt=1)]):
    """
    ## Get the first 'n' rows of the dataset.
    """
    head = DataSet().get_head(rows)
    return DatasetSchema.from_data_frame(head)


@router.put("/dataset/columns_names", summary="Update column names")
async def update_columns_names(input_schema: UpdateColumnNames):
    """
    ## Update the names of the dataset columns.

    Renames dataset's columns according to the given mapping of old column names to new column names.
    """
    transformed_data = DataTransformer.rename(DataSet().data, input_schema.mapping)
    DataSet().data = transformed_data


@router.put("/dataset/columns_types", summary="Update column types")
async def update_columns_types(input_schema: UpdateColumnTypes):
    """
    ## Update the data types of the dataset columns.

    Change types of columns according to the given mapping of column names to new Datatypes. This not only changes the
    displayed type of the column but slo tries to transform the data to the desired type.
    """
    transformed_data = DataTransformer.change_types(DataSet().data, input_schema.mapping)
    DataSet().data = transformed_data


@router.get("/pca/graph", summary="PCA components graph")
async def get_components_graph():
    """
    ## Retrieve a graph of PCA components.

    This endpoint returns a graph image that visualizes the Principal Component Analysis (PCA) components
    of the currently active dataset.
    """
    graph = PCA.interactive_pca_results(DataSet().data)
    return Response(graph, media_type='application/json')


@router.get('/pca/transform', summary="PCA transformation result", response_model=DatasetSchema)
async def get_pca(rows: Annotated[int, Query(gt=1)]):
    """
    ## Get the result of PCA transformation.

    This endpoint applies PCA transformation to the current active dataset and returns the transformed dataset schema.
    """
    transformed_data = PCA.transform(DataSet().data, DataSet().age)
    return DatasetSchema.from_data_frame(transformed_data.head(n = rows))


@router.put('/pca/transform', summary="Perform PCA")
async def perform_pca():
    """
    ## Perform PCA transformation on the dataset.

    This endpoint applies PCA transformation to the current active dataset,
    and sets the result as current active dataset.
    """
    transformed_data = PCA.transform(DataSet().data, DataSet().age)
    DataSet().data = transformed_data


@router.get("/normalization/methods", summary="Normalization methods", response_model=list[NormalizationType])
async def get_normalization_methods():
    """
    ## List all available normalization methods.
    """
    methods = DataTransformer.get_normalization_methods()
    return [NormalizationType.model_validate(method) for method in methods]


@router.post("/normalization", summary="Perform normalization")
async def perform_normalization(normalizations: list[NormalizationType]):
    """
    ## Apply normalization to the dataset.

    All available normalization methods can be found at `/normalization/methods`.
    """
    methods = [normalization.name for normalization in normalizations]
    DataSet().data = DataTransformer.normalize(DataSet().data, methods)


@router.get("/data_types", summary="Data types", response_model=list[DataType])
async def get_data_types():
    """
    ## Retrieve all possible data types.
    """
    return list(DataType)


@router.post("/clustering/", summary="Perform clustering", response_model=str)
async def perform_clustering(
    data_subset: Annotated[DataFrame, Depends(numerical_subset_dependency)],
    method: ClusteringMethodSchema
):
    """
    ## Performs clustering

    Applies chosen clustering method to the data, and returns id of the clustering result. Results are cached,
    for later use by other endpoints.

    Possible methods can be found at `/clustering/methods`.

    `columns` parameter should contain list of column names from the current active dataset on which clustering
    will be performed.
    """
    return ClusteringInteractive.perform_clustering(data_subset, DataSet().age, method.name, method.parameters)


@router.get("/clustering/{clustering_id}/plot", summary="Clustering plot")
async def get_clusters_plot(clustering_id: Annotated[str, Depends(clustering_id_dependency)]):
    """
    ## Generate a clustering plot.

    Returns plot of the clustering identified by the clustering id.
    """
    graph = ClusteringInteractive.visualize_clustering(clustering_id)
    return Response(graph, media_type='application/json')


@router.get("/clustering/{clustering_id}/clusters", summary="Clusters", response_model=Column)
async def get_clusters(clustering_id: Annotated[str, Depends(clustering_id_dependency)]):
    """
    ## Get clusters.

    Returns a column of clusters, identified by the clustering id.
    """
    clusters = ClusteringInteractive.clusters_cache[clustering_id]
    return Column(
        name="Clusters",
        type=DataType.CATEGORICAL,
        values=clusters
    )


@router.get(
    "/clustering/{clustering_id}/statistics",
    summary="Clustering statistics",
    response_model=ClusteringStatistics
)
async def get_clusters_statistics(clustering_id: Annotated[str, Depends(clustering_id_dependency)]):
    """
    ## Get a clustering statistics.

    Returns statistics of the clustering result identified by the clustering id.
    """
    statistics = ClusteringInteractive.evaluate_clustering(clustering_id)
    return ClusteringStatistics(statistics=statistics)


@router.post("/clustering/clustering_tendency", summary="Clustering tendency")
async def get_clustering_tendency(data_subset: Annotated[DataFrame, Depends(numerical_subset_dependency)]):
    """
    ## Return a hopkins statistic.

    Calculates a hopkins statistic for a chosen subset of the active dataset.
    `columns` parameter should contain list of column names from the current active dataset on which analysis
    will be performed.
    """
    return Clustering.hopkins_statistic(data_subset)


@router.get("/clustering/methods", summary="Clustering methods", response_model=list[ClusteringMethod])
async def get_clustering_methods():
    """
    ## List available clustering methods.
    """
    return Clustering.get_clustering_methods()
