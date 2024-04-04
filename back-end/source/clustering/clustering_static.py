import io

import seaborn as sns

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from numpy import ndarray
from pandas import DataFrame

from .clustering import Clustering


class ClusteringStatic(Clustering):

    @staticmethod
    def visualize_clustering(data: DataFrame, clusters: ndarray) -> plt.Figure:
        """Produces plot of based on given data and it's labels representing clusters."""
        reduced_data = Clustering.reduce_dimensionality(data)

        fig, axes = plt.subplots(4, 2, figsize=(8, 9),
                                 gridspec_kw={'hspace': 0,
                                              'wspace': 0,
                                              'width_ratios': [5, 1],
                                              'height_ratios': [1, 5, 1, 2]
                                              }
                                 )

        for ax in axes.flatten():
            ax.axis('off')

        axes[1, 0].axis("on")
        axes[3, 0].axis("on")

        fig.delaxes(axes[0, 1])
        fig.delaxes(axes[2, 0])
        fig.delaxes(axes[2, 1])
        fig.delaxes(axes[3, 1])

        ClusteringStatic.cluster_plot(reduced_data, clusters, axes[1, 0], axes[1, 1], axes[0, 0])
        ClusteringStatic.histogram(clusters, axes[3, 0])

        fig.tight_layout()
        return fig

    @staticmethod
    def cluster_plot(points: DataFrame, clusters: ndarray, ax_main: Axes, ax_side: Axes, ax_top: Axes) -> None:
        x, y = points.iloc[:, 0], points.iloc[:, 1]

        sns.scatterplot(x=x, y=y, hue=clusters, ax=ax_main, legend=False)

        ax_main.set_xticks([])
        ax_main.set_yticks([])

        sns.kdeplot(x=x, hue=clusters, fill=True, ax=ax_top, legend=False)

        ax_top.set_xticks([])
        ax_top.set_yticks([])
        ax_top.spines['left'].set_visible(False)

        sns.kdeplot(y=y, hue=clusters, fill=True, ax=ax_side, legend=False)

        ax_side.set_xticks([])
        ax_side.set_yticks([])

        return None

    @staticmethod
    def histogram(clusters: ndarray, ax: plt.Axes) -> None:
        sns.histplot(
            x=clusters, stat='count', hue=clusters,
            ax=ax, discrete=True, legend=False,
        )

        ax.set_xticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_title('Cluster Distribution')

    @staticmethod
    def save_plot(fig: plt.Figure) -> bytes:
        """Saves a plot to png and returns its bytes."""
        bytes_image = io.BytesIO()
        fig.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        return bytes_image.getvalue()
