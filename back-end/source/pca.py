from sklearn.decomposition import PCA as SklearnPCA
import sklearn
from matplotlib import pyplot as plt
from source.data_set import DataSet
import io
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


class PCA:
    '''Class performs all PCA operations using PCA class from sklearn and caching'''
    sklearn.set_config(transform_output="pandas")
    current_age:int = -1
    _pca = SklearnPCA()
    
    @classmethod
    def _fit(cls,data_set:pd.DataFrame) -> None:
        if cls.current_age == -1:
            cls.current_age += 1
            cls._pca.fit(StandardScaler().fit_transform(data_set.select_dtypes(include=np.number).dropna()))
            print(data_set.head())

    @classmethod
    def transform(cls,data_set:pd.DataFrame,age:int = -2) -> pd.DataFrame:
        '''Fit PCA transform if needed and returns transformed data'''
        cls._fit(data_set)
        return cls._pca.transform(data_set.select_dtypes(include=np.number).notnull())

    @classmethod
    def components_graph(cls,data_set:pd.DataFrame,age:int = -2,format = 'jpg') -> io.BytesIO:
        '''Fit PCA transform if needed and returns components graph'''
        cls._fit(data_set)
        explained_variance = cls._pca.explained_variance_ratio_
        fig = plt.figure()
        plt.title('Percentage explained variance by each PCA component')
        plt.bar([f'PCA{i + 1}' for i in range(len(explained_variance))],explained_variance)
        plt.xlabel('Component')
        plt.ylabel('Percentage explained variance')
        buffer = io.BytesIO()
        plt.savefig(buffer,format = format)
        buffer.seek(0)
        plt.close(fig)
        return buffer
    

    @classmethod
    def explained_variance(cls) -> pd.Series:
        return cls._pca.explained_variance_ratio_
        
