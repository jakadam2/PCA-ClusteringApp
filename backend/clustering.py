import io
from enum import Enum

from numpy import ndarray
from pandas import DataFrame
from sklearn.cluster import estimate_bandwidth, MeanShift, AffinityPropagation, DBSCAN
from matplotlib import pyplot as plt


class ClusteringMethod(Enum):
    AFFINITY = "Affinity Propagation"


class Clustering:
    @staticmethod
    def affinity_propagation(data: DataFrame) -> ndarray:
        return AffinityPropagation(preference=-50, random_state=0).fit_predict(data)

    @staticmethod
    def mean_shift(data: DataFrame) -> ndarray:
        bandwidth = estimate_bandwidth(data, quantile=0.2, n_samples=min(500, len(data)))
        return MeanShift(bandwidth=bandwidth, bin_seeding=True).fit_predict(data)

    @staticmethod
    def dbscan(data: DataFrame) -> ndarray:
        return DBSCAN(eps=0.3, min_samples=10).fit_predict(data)

    methods = {'Affinity Propagation': affinity_propagation, 'Mean-shift': mean_shift, 'dbscan': dbscan}

    @staticmethod
    def perform_clustering(data: DataFrame, method='Mean-shift'):
        if method not in Clustering.methods:
            raise ValueError(f"Clustering method {method} not recognized.")

        clusters = Clustering.methods[method](data)
        Clustering.visualize_clustering(data, clusters)

    @staticmethod
    def visualize_clustering(data: DataFrame, clusters: ndarray) -> io.BytesIO:
        ...
        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        return bytes_image

    @staticmethod
    def get_clustering_methods():
        return list(Clustering.methods.keys())
