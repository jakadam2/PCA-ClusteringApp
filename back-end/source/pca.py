import io

from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as ex
from plotly.subplots import make_subplots

from source.data_set import DataSet
from source.plotting import get_colour_palette_rgba,get_colour_palette

import pandas as pd
import numpy as np

import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA as SklearnPCA

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
            cls._columns_names = data_set.select_dtypes(include=np.number).columns

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
    def interactive_pca_results(cls,data_set:pd.DataFrame) -> str:
        cls._fit(data_set)
        explained_variance = cls._pca.explained_variance_ratio_
        pca_graph = make_subplots(rows=1,cols=2)
        explained_variance_graph = PCA.explained_variance_graph(explained_variance)
        components_direction_graph = PCA.components_direction_graph(pca_graph)
        pca_graph.add_trace(explained_variance_graph,row=1,col=1)
        return components_direction_graph.to_html(config = PCA.get_configs())
    
    @staticmethod
    def explained_variance_graph(explained_variance) -> go.Bar:
        colors = [color.to_str() for color in get_colour_palette_rgba(len(explained_variance))]
        fig = go.Bar(y = explained_variance ,x = [f'PCA{i + 1}' for i in range(len(explained_variance))],marker_color=colors)
        return fig

    @classmethod
    def components_direction_graph(cls,fig) -> go.Figure:
        explained_variances = cls._pca.explained_variance_ratio_
        loadings = cls._pca.components_.T * np.sqrt(explained_variances)
        colors = [color.to_str() for color in get_colour_palette_rgba(len(explained_variances))]
        for i, feature in enumerate(cls._columns_names):
            fig.add_trace(go.Scatter(
                x=[0, loadings[i, 0]/2],
                y=[0, loadings[i, 1]/2],
                mode='lines+markers',
                name=feature,
                line=dict(color=colors[i], width=2),
                marker=dict(color=colors[i], size=10,symbol= "arrow-bar-up", angleref="previous"),
                text=[feature],
                hoverinfo='text',
                showlegend=True
            ),row = 1,col = 2)

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='white',title_text='Principal Component 1',row = 1,col =2)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='white',title_text='Principal Component 2',row = 1,col =2)
        return fig

    @classmethod
    def explained_variance(cls) -> pd.Series:
        return cls._pca.explained_variance_ratio_
        
    @staticmethod
    def get_configs():
        """Returns configs for displaying plotly figure."""
        config = {
            'displaylogo': False,
            'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        }
        return config