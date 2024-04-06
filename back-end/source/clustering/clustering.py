import numpy as np

from enum import StrEnum
from numpy import ndarray
from pandas import DataFrame
from abc import abstractmethod
from sklearn.cluster import estimate_bandwidth, MeanShift, AffinityPropagation, DBSCAN
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors

from source.preprocessing.data_transformer import DataTransformer
from source.exceptions import InvalidMethodException


class ClusteringMethod(StrEnum):
    AFFINITY = "Affinity Propagation"
    MEAN_SHIFT = "Mean-shift"
    DBSCAN = "Dbscan"


class Clustering:
    @staticmethod
    def affinity_propagation(data: DataFrame, params: dict) -> ndarray:
        """Performs clustering using affinity propagation algorithm."""
        return AffinityPropagation(**params).fit_predict(data)

    @staticmethod
    def mean_shift(data: DataFrame, params: dict) -> ndarray:
        """Performs clustering using mean shift algorithm."""
        bandwidth = estimate_bandwidth(data, quantile=0.2, n_samples=min(500, len(data)))
        return MeanShift(bandwidth=bandwidth, **params).fit_predict(data)

    @staticmethod
    def dbscan(data: DataFrame, params: dict) -> ndarray:
        """Performs clustering using dbscan algorithm."""
        return DBSCAN(**params).fit_predict(data)

    clustering_methods = {
        ClusteringMethod.AFFINITY: affinity_propagation,
        ClusteringMethod.MEAN_SHIFT: mean_shift,
        ClusteringMethod.DBSCAN: dbscan
    }

    @classmethod
    def perform_clustering(
            cls: type["Clustering"],
            data: DataFrame,
            method: ClusteringMethod,
            method_parameters: dict,
    ):
        """Performs chosen clustering operation and returns plot of clusters."""
        data = data[DataTransformer.get_numerical_columns(data)]

        if data.isna().values.any():
            data.dropna(axis='rows', inplace=True)

        if method not in cls.clustering_methods:
            raise InvalidMethodException(method)

        clusters = cls.clustering_methods[method](data, method_parameters)
        plot = cls.visualize_clustering(data, clusters)

        return cls.save_plot(plot)

    @staticmethod
    @abstractmethod
    def visualize_clustering(data: DataFrame, clusters: ndarray) -> plt.Figure:
        """Produces plot of clusters based on given data and it's labels representing clusters."""
        ...

    @staticmethod
    @abstractmethod
    def save_plot(plot):
        ...

    @staticmethod
    def reduce_dimensionality(data: DataFrame) -> DataFrame:
        """Reduces data to 2 dimensions."""
        if len(data.columns) <= 2:
            return data

        if len(data.columns) > 50:  # somewhat arbitrary number, taken from scikit-learn guide on t-SNE
            pca = PCA(n_components=50)
            data = pca.fit_transform(data)

        tsne = TSNE(n_components=2)
        result = tsne.fit_transform(data)

        if isinstance(result, np.ndarray):
            result = DataFrame.from_records(result, columns=['tsne0', 'tsne1'])

        return result

    @staticmethod
    def get_clustering_methods() -> list[ClusteringMethod]:
        """Returns all available clustering methods."""
        return list(Clustering.clustering_methods.keys())

    @staticmethod
    def hopkins_statistic(data: DataFrame, sample_size=0.1, seed=42) -> float:
        """
        Calculates hopkins statistic.

        https://en.wikipedia.org/wiki/Hopkins_statistic
        """
        data = data.dropna()
        rows, dimensions = data.shape
        m = int(sample_size * rows)
        m = m if m > 0 else rows

        np.random.seed(seed)

        neighbours = NearestNeighbors(n_neighbors=2).fit(data.to_numpy())

        data_sample = data.sample(n=m, replace=False).to_numpy()
        y_sample = np.random.uniform(data.min(axis=0), data.max(axis=0), size=(m, dimensions))

        w_distances, _ = neighbours.kneighbors(data_sample, return_distance=True)
        w_distances = w_distances[:, 1]

        u_distances, _ = neighbours.kneighbors(y_sample, n_neighbors=1, return_distance=True)

        w_sum = (w_distances**dimensions).sum()
        u_sum = (u_distances**dimensions).sum()
        return u_sum/(u_sum + w_sum)
