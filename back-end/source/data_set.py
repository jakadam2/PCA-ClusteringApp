import pandas as pd
from source.api.schemas import DatasetSchema
from source.data_type import DataType


def get_key(dataset_id: int, columns: list[str] | None):
    return f"{dataset_id}|{'-'.join(sorted(columns))}"


class DataSetImplementation:
    '''Implements all of functionalities of DataSet but it is not singleton'''
    def __init__(self) -> None:
        self._data_set: pd.DataFrame|None = None 
        self._previous_data_set : pd.DataFrame|None = None 
        self._name: str|None = None
        self.age:int = 0

    def load_data(self,data_schema:DatasetSchema) -> None:
        '''Loads DataFrame from DatasetSchema object'''
        self._data_set = pd.DataFrame({column.name: pd.Series(column.values,dtype = float if column.type == DataType.NUMERICAL else str) for column in data_schema.variables})

    @property
    def data(self) -> pd.DataFrame:
        '''Property to get DataFrame with going back mechanism'''
        return self._data_set
    
    @data.setter
    def data(self,new_data:pd.DataFrame) -> None:
        self.age += 1
        self._previous_data_set = self._data_set
        self._data_set = new_data

    def get_types(self) -> pd.Series:
        '''Returns types of each column'''
        return self._data_set.dtypes
    
    def get_info(self) -> pd.Series:
        '''Returns short summary of data'''
        return self._data_set.describe(include='all')
    
    def get_head(self,rows:int = 10) -> pd.DataFrame:
        '''Returns first "rows" rows of data '''
        return self._data_set.head(n = rows)
    

class DataSet:
    '''Singleton version of DataSetImplementation'''
    _impl:DataSetImplementation = None

    def __new__(cls,*args,**kwargs) -> DataSetImplementation:
        if cls._impl is None:
            cls._impl = DataSetImplementation(*args,**kwargs)
        return cls._impl
    
    
