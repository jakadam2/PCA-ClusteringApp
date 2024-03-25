from typing import Annotated
import pandas as pd

from fastapi import APIRouter, Query, UploadFile, File
from fastapi.responses import Response

from source.api.schemas import DatasetSchema, UpdateColumnNames, UpdateColumnTypes, Graph, NormalizationType
from source.clustering import Clustering, ClusteringMethod
from source.data_set import DataSet
from source.data_transformer import DataTransformer
from source.data_type import DataType
from source.pca import PCA

router = APIRouter(prefix="/api")


@router.post("/file")
async def post_dataset(file: UploadFile = File(...)):
    df = pd.read_csv(file.file, sep=';')
    DataSet()._data_set = df
    print(df.head())


@router.get("/file", response_model=DatasetSchema)
async def get_dataset():
    return DatasetSchema.from_data_frame(DataSet().data)


@router.get("/dataset", response_model=DatasetSchema)
async def get_head(rows: Annotated[int, Query(gt=1)]):
    head = DataSet().get_head(rows).fillna('')
    return DatasetSchema.from_data_frame(head)


@router.put("/dataset/columns_names")
async def update_columns_names(input_schema: UpdateColumnNames):
    transformed_data = DataTransformer.rename(DataSet().data, input_schema.mapping)
    DataSet().data = transformed_data


@router.put("/dataset/columns_types")
async def update_columns_types(input_schema: UpdateColumnTypes):
    transformed_data = DataTransformer.change_types(DataSet().data, input_schema.mapping)
    DataSet().data = transformed_data


@router.get("/pca/graph", response_model=Graph)
async def get_components_graph():
    graph = PCA.components_graph(DataSet().data, DataSet().age)
    return Response(graph.getvalue(), media_type='image/png')


@router.get('/pca/transform', response_model=DatasetSchema)
async def get_pca():
    transformed_data = PCA.transform(DataSet().data, DataSet().age)
    return DatasetSchema.from_data_frame(transformed_data)


@router.put('/pca/transform')
async def perform_pca():
    transformed_data = PCA.transform(DataSet().data, DataSet().age)
    DataSet().data = transformed_data


@router.get("/normalization/methods", response_model=list[NormalizationType])
async def get_normalization_methods():
    methods = DataTransformer.get_normalization_methods()
    return [NormalizationType.model_validate(method) for method in methods]


@router.post("/normalization")
async def perform_normalization(normalizations: list[NormalizationType]):
    methods = [normalization.name for normalization in normalizations]
    DataSet().data = DataTransformer.normalize(DataSet().data, methods)


@router.get("/data_types", response_model=list[DataType])
async def get_data_types():
    return list(DataType)


@router.get("/clustering/graph")
async def perform_clustering(method: ClusteringMethod):
    graph = Clustering.perform_clustering(DataSet().data, method)
    return Response(graph.getvalue(), media_type='image/png')


@router.get("/clustering/methods", response_model=list[ClusteringMethod])
async def get_clustering():
    return Clustering.get_clustering_methods()
