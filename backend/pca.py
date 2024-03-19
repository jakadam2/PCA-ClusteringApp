from sklearn.decomposition import PCA as SklearnPCA
from matplotlib import pyplot as plt
from data_set import DataSet

class PCA:

    current_age:int = -1
    _pca = SklearnPCA()

    @classmethod
    def _fit(cls,data_set:DataSet) -> None:
        cls._pca.fit(data_set.data)

    @classmethod
    def transform(cls,data_set:DataSet) -> None:
        if data_set.age != cls.current_age:
            cls._fit(data_set)
        data_set.data = cls._pca.transform(data_set.data)

    @classmethod
    def components_graph(cls,data_set:DataSet):
        if data_set.age != cls.current_age:
            cls._fit(data_set)
        explained_variance = cls._pca.explained_variance_ratio_
        plt.bar([i + 1 for i in range(len(explained_variance))],explained_variance)

    @property
    @classmethod
    def explained_variance(cls):
        return cls._pca.explained_variance_ratio_


        


        
