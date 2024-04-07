import numpy as np
import pandas as pd
import plotly.graph_objs as go
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.collections import PolyCollection
from numpy import ndarray
from pandas import DataFrame
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots

from source.clustering.clustering import Clustering
from source.plotting import get_colour_palette_rgba


class ClusteringInteractive(Clustering):

    @classmethod
    def create_plot(cls, data: DataFrame, clusters: ndarray):
        """Produces plot of based on given data and it's labels representing clusters."""
        reduced_data = cls.reduce_dimensionality(data)

        fig = cls.setup_figure()
        cls.histogram(clusters, fig, 4, 1)
        cls.cluster_plot(reduced_data, clusters, fig, 2, 1)

        return go.FigureWidget(fig)

    @staticmethod
    def setup_figure() -> go.Figure:
        """Sets up the figure layout for the clustering visualization."""
        fig = make_subplots(
            rows=4, cols=2,
            column_widths=[0.8, 0.2],
            row_heights=[0.1, 0.7, 0.1, 0.3],
            specs=[
                [{'type': 'xy'}, None],
                [{'type': 'scatter'}, {'type': 'xy'}],
                [None, None],
                [{'type': 'histogram'}, None]
            ],
            horizontal_spacing=0,
            vertical_spacing=0,
        )

        fig.update_layout(
            plot_bgcolor='white',
            dragmode='pan',
        )

        return fig

    @classmethod
    def cluster_plot(cls, points: DataFrame, clusters: ndarray, fig: Figure, row: int, col: int) -> None:
        clusters_num = np.unique(clusters).size
        colors = get_colour_palette_rgba(clusters_num)
        min_y, max_y = float('inf'), -float('inf')
        min_x, max_x = float('inf'), -float('inf')

        for cluster_id in np.unique(clusters):
            cluster_id: int
            cluster_points = points[clusters == cluster_id]
            cluster_x, cluster_y = cluster_points.iloc[:, 0], cluster_points.iloc[:, 1]
            color = colors[cluster_id]

            scatter = go.Scattergl(
                x=cluster_x, y=cluster_y, marker=dict(color=str(color)), mode='markers',
                name=str(cluster_id), legendgroup=f"group{cluster_id}", showlegend=False,
                hovertemplate=f'Part of cluster {cluster_id}<extra></extra>',
            )
            fig.add_trace(scatter, row, col)

            side_density = cls.get_line_density(cluster_y)
            side_density_x, side_density_y = side_density[:, 0], side_density[:, 1]

            min_y = min(min_y, side_density_y.min())
            max_y = max(max_y, side_density_y.max())

            histogram_right = go.Scatter(
                x=side_density_x, y=side_density_y, mode='lines',
                fill='tozerox', fillcolor=color.change_alfa(0.4).to_str(), marker=dict(color=str(color)),
                showlegend=False, legendgroup=f"group{cluster_id}", name=str(cluster_id),
                hoverinfo='skip'
            )
            fig.add_trace(histogram_right, row=row, col=col + 1)

            side_density = cls.get_line_density(cluster_x)
            side_density_y, side_density_x = side_density[:, 0], side_density[:, 1]

            min_x = min(min_x, side_density_x.min())
            max_x = max(max_x, side_density_x.max())

            histogram_top = go.Scatter(
                x=side_density_x, y=side_density_y, mode='lines',
                fill='tozeroy', fillcolor=color.change_alfa(0.4).to_str(), marker=dict(color=str(color)),
                showlegend=False, legendgroup=f"group{cluster_id}", name=str(cluster_id),
                hoverinfo='skip'
            )
            fig.add_trace(histogram_top, row=row - 1, col=col)

        fig.update_xaxes(fixedrange=True, tickmode='array', tickvals=[], row=row, col=col + 1)
        fig.update_yaxes(matches='y2', tickmode='array', tickvals=[], row=row, col=col + 1)
        fig.update_xaxes(matches='x2', tickmode='array', tickvals=[], row=row - 1, col=col)
        fig.update_yaxes(fixedrange=True, tickmode='array', tickvals=[], row=row - 1, col=col)

        fig.update_xaxes(title_text=points.columns[0], tickmode='array', tickvals=[], row=row, col=col)
        fig.update_yaxes(title_text=points.columns[1], tickmode='array', tickvals=[], row=row, col=col)

        fig.update_layout(yaxis2=dict(range=[min_y, max_y]))
        fig.update_layout(xaxis2=dict(range=[min_x, max_x]))

    @staticmethod
    def get_line_density(points: pd.Series):
        plt.close()
        sample_points = points.sample(n=min(1000, len(points)), replace=False, random_state=42)
        plot: plt.Axes = sns.kdeplot(y=sample_points, fill=True)
        poly: PolyCollection = plot.collections[0]
        plt.close()
        return poly.get_paths()[0].vertices

    @staticmethod
    def histogram(clusters: ndarray, fig: Figure, row: int, col: int) -> None:
        clusters_num = np.unique(clusters).size
        colors = get_colour_palette_rgba(clusters_num)

        for cluster_id, cluster_size in zip(*np.unique(clusters, return_counts=True)):
            bar = go.Bar(
                y=[cluster_size], x=[cluster_id], marker=dict(color=colors[cluster_id].to_str()),
                name=str(cluster_id), legendgroup=f"group{cluster_id}",
                hovertemplate=f'Cluster size: {cluster_size}<br>Cluster Id: {cluster_id}<extra></extra>'
            )
            fig.add_trace(bar, row=row, col=col)

        fig.update_xaxes(title_text="Clusters", tickmode='array', tickvals=[], fixedrange=True, row=row, col=col)
        fig.update_yaxes(title_text="Count", fixedrange=True, row=row, col=col)

    @classmethod
    def save_plot(cls, fig: Figure) -> str:
        """Saves a plot to html string."""
        configs = cls.get_configs()
        return fig.to_html(config=configs)

    @staticmethod
    def get_configs():
        """Returns configs for displaying plotly figure."""
        config = {
            'displaylogo': False,
            'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        }
        return config
