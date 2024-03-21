from typing import Annotated

from fastapi import APIRouter, Query

from backend.api.schemas import DatasetSchema, UpdateColumnNames, UpdateColumnTypes, Graph, NormalizationType
from backend.data_set import DataSet
from backend.data_transformer import DataTransformer
from backend.data_type import DataType

router = APIRouter(prefix="/api")


@router.post("/file")
async def post_dataset(dataset: DatasetSchema):
    DataSet().load_data(dataset)


@router.get("/file", response_model=DatasetSchema)
async def get_dataset():
    return DatasetSchema.from_data_frame(DataSet().data)


# TODO make get_head method of dataset return dataset schema
@router.get("/dataset", response_model=DatasetSchema)
async def get_head(rows: Annotated[int, Query(gt=1)]):
    head = DataSet().get_head(rows)
    return DatasetSchema.from_data_frame(head)


@router.put("/dataset/columns_names")
async def update_columns_names(input_schema: UpdateColumnNames):
    DataTransformer.rename(DataSet().data, input_schema.mapping)


@router.put("/dataset/columns_types")
async def update_columns_types(input_schema: UpdateColumnTypes):
    DataTransformer.change_types(DataSet().data, input_schema.mapping)


@router.get("/components/graph", response_model=Graph)
async def get_components_graph():
    ...


@router.get("/normalization_methods", response_model=list[NormalizationType])
async def get_normalization_methods():
    methods = DataTransformer.get_normalization_methods()
    return [NormalizationType.model_validate(method) for method in methods]


@router.get("/data_types", response_model=list[DataType])
async def get_data_types():
    return list(DataType)


@router.post("/clustering")
async def post_clustering():
    ...


@router.get("/clustering", response_model=Graph)
async def get_clustering():
    ...
