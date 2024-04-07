from typing import Optional

import numpy as np
import hashlib

from enum import StrEnum
from numpy import ndarray
from pandas import DataFrame
from abc import abstractmethod

from sklearn import metrics
from sklearn.cluster import estimate_bandwidth, MeanShift, AffinityPropagation, DBSCAN
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors

from source.cache import Cache
from source.preprocessing.data_transformer import DataTransformer
from source.exceptions import InvalidMethodException, InvalidMethodArguments


class ClusteringMethod(StrEnum):
    AFFINITY = "Affinity Propagation"
    MEAN_SHIFT = "Mean-shift"
    DBSCAN = "Dbscan"


class Clustering:
    clusters_cache = Cache[ndarray](10e8)  # cache size of 100MB

    # Stores a view of the datasets used for the clustering
    dataset_cache = Cache[DataFrame](10e9, parent=clusters_cache)

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
            dataset_id: int,
            method: ClusteringMethod,
            method_parameters: dict,
    ) -> str:
        """Performs chosen clustering operation and returns plot of clusters."""
        clustering_id = cls.get_clustering_id(dataset_id, data.columns.to_list(), method, method_parameters)
        if clustering_id in Clustering.clusters_cache:
            return clustering_id

        data = data[DataTransformer.get_numerical_columns(data)]

        if data.isna().values.any():
            data.dropna(axis='rows', inplace=True)  # is it a good idea to do it inplace?

        if method not in cls.clustering_methods:
            raise InvalidMethodException(method)

        try:
            clusters = cls.clustering_methods[method](data, method_parameters)
        except TypeError:
            raise InvalidMethodArguments(method)

        # caching results for later use
        Clustering.clusters_cache.put(clustering_id, clusters)
        Clustering.dataset_cache.put(clustering_id, data)

        return clustering_id

    @staticmethod
    def get_clustering_id(dataset_id: int, columns: list, method: ClusteringMethod, method_parameters: dict) -> str:
        """Creates a unique key identifying a clustering result."""
        raw_key = f"{method}{method_parameters}{dataset_id}{columns}"
        raw_key_bytes = raw_key.encode('utf-8')
        return hashlib.md5(raw_key_bytes).hexdigest()

    @classmethod
    def visualize_clustering(cls: type["Clustering"], clustering_id: str):
        clusters = cls.clusters_cache[clustering_id]
        data = cls.dataset_cache[clustering_id]
        plot = cls.create_plot(data, clusters)
        return cls.save_plot(plot)

    @classmethod
    @abstractmethod
    def create_plot(cls, data: DataFrame, clusters: ndarray) -> plt.Figure:
        """Produces plot of clusters based on given data and it's labels representing clusters."""
        ...

    @classmethod
    @abstractmethod
    def save_plot(cls, plot):
        ...

    @staticmethod
    def reduce_dimensionality(data: DataFrame) -> DataFrame:
        """Reduces data to 2 dimensions."""
        if len(data.columns) <= 2:
            return data

        size_threshold = 1e4
        _, columns = data.shape

        if data.size > size_threshold:
            n_components = columns//(data.size/size_threshold)
            n_components = max(int(n_components), 2)

            pca = PCA(n_components=n_components)
            data = DataFrame(pca.fit_transform(data), columns=['pca 0', 'pca 1'])

        if len(data.columns) > 2:
            tsne = TSNE(n_components=2, init='random', random_state=42)
            data = DataFrame(tsne.fit_transform(data), columns=['tsne0', 'tsne1'])

        return data

    @classmethod
    def get_clustering_methods(cls: type["Clustering"]) -> list[ClusteringMethod]:
        """Returns all available clustering methods."""
        return list(cls.clustering_methods.keys())

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

        w_sum = (w_distances ** dimensions).sum()
        u_sum = (u_distances ** dimensions).sum()
        return u_sum / (u_sum + w_sum)

    @classmethod
    def evaluate_clustering(cls: type["Clustering"], clustering_id: str) -> dict[str, float]:
        clusters = cls.clusters_cache[clustering_id]
        data = cls.dataset_cache[clustering_id]
        return {
            "Silhouette Coefficient": metrics.silhouette_score(data, clusters),
            "Calinski-Harabasz index": metrics.calinski_harabasz_score(data, clusters),
            "Davies-Bouldin index": metrics.davies_bouldin_score(data, clusters),
        }
