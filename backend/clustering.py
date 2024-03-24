import io
from enum import StrEnum

from numpy import ndarray
from pandas import DataFrame
from sklearn.cluster import estimate_bandwidth, MeanShift, AffinityPropagation, DBSCAN
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


class ClusteringMethod(StrEnum):
    AFFINITY = "Affinity Propagation"
    MEAN_SHIFT = "Mean-shift"
    DBSCAN = "Dbscan"


class Clustering:
    @staticmethod
    def affinity_propagation(data: DataFrame) -> ndarray:
        """Performs clustering using affinity propagation algorithm."""
        return AffinityPropagation().fit_predict(data)

    @staticmethod
    def mean_shift(data: DataFrame) -> ndarray:
        """Performs clustering using mean shift algorithm."""
        bandwidth = estimate_bandwidth(data, quantile=0.2, n_samples=min(500, len(data)))
        return MeanShift(bandwidth=bandwidth, bin_seeding=True).fit_predict(data)

    @staticmethod
    def dbscan(data: DataFrame) -> ndarray:
        """Performs clustering using dbscan algorithm."""
        return DBSCAN().fit_predict(data)

    clustering_methods = {
        ClusteringMethod.AFFINITY: affinity_propagation,
        ClusteringMethod.MEAN_SHIFT: mean_shift,
        ClusteringMethod.DBSCAN: dbscan
    }

    @staticmethod
    def perform_clustering(data: DataFrame, method: ClusteringMethod = ClusteringMethod.MEAN_SHIFT) -> io.BytesIO:
        """Performs chosen clustering operation and returns plot of clusters."""
        if data.isna().values.any():
            data.dropna(axis='rows', inplace=True)

        if method not in Clustering.clustering_methods:
            raise ValueError(f"Clustering method {method} not recognized.")

        clusters = Clustering.clustering_methods[method](data)
        return Clustering.visualize_clustering(data, clusters)

    @staticmethod
    def visualize_clustering(data: DataFrame, clusters: ndarray) -> io.BytesIO:
        """Produces plot of based on given data and it's labels representing clusters."""
        reduced_data = Clustering.reduce_dimensionality(data)

        plt.scatter(reduced_data.iloc[:, 0], reduced_data.iloc[:, 1], c=clusters, cmap='viridis')

        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        return bytes_image

    @staticmethod
    def reduce_dimensionality(data: DataFrame) -> DataFrame:
        """Reduces data two 2 dimensions."""
        if len(data.columns) > 50:  # somewhat arbitrary number, taken from scikit-learn guide on t-SNE
            pca = PCA(n_components=50)
            data = pca.fit_transform(data)

        tsne = TSNE(n_components=2)
        return tsne.fit_transform(data)

    @staticmethod
    def get_clustering_methods() -> list[ClusteringMethod]:
        """Returns all available clustering methods."""
        return list(Clustering.clustering_methods.keys())
