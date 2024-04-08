import io

from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as ex
from plotly.subplots import make_subplots

from source.data_set import DataSet
from source.plotting import get_colour_palette_rgba,get_colour_palette
from source.preprocessing.dataprocessing import DataProcessing

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
        cls._pca.fit(StandardScaler().fit_transform(data_set.select_dtypes(include=np.number)))
        cls._columns_names = data_set.select_dtypes(include=np.number).columns
        cls._columns_size = len(cls._columns_names)

    @classmethod
    def transform(cls,data_set:pd.DataFrame,age:int = -2) -> pd.DataFrame:
        '''Fit PCA transform if needed and returns transformed data'''
        cls._fit(data_set)
        return cls._pca.transform(data_set.select_dtypes(include=np.number))

    @classmethod
    def interactive_pca_results(cls,data_set:pd.DataFrame) -> str:
        '''Make interactive plots using plotly and return json string'''
        cls._fit(data_set)
        pca_graph = make_subplots(rows=2,cols=2,subplot_titles=("Explained variance ratio", 
                                                                "Components direction", 
                                                                "Participation of basic features", 
                                                                "Participation of basic features"))
        PCA.explained_variance_graph(pca_graph)
        PCA.components_direction_graph(pca_graph)
        PCA.loadigns_graph(pca_graph)
        pca_graph.update_layout(
        legend={
            "title": "Component",
            "xref": "container",
            "yref": "container",
            "y": 0.87,

        },legend3={
            "title": "Feature",
            "xref": "container",
            "yref": "container",
            "y": 0.07,

        },plot_bgcolor='white')
        return pca_graph.to_json()
    
    @classmethod
    def explained_variance_graph(cls,fig:go.Figure) -> None:
        explained_variances = cls.explained_variance()
        colors = [color.to_str() for color in get_colour_palette_rgba(cls._columns_size)]
        fig.add_trace(go.Bar(y = explained_variances ,
                             x = [f'PCA{i + 1}' for i in range(cls._columns_size)],
                             marker_color=colors,showlegend=False),
                             row = 1,col=1)
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='white',title_text='Component',row = 1,col =1 )
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='white',title_text='Explained variance',row = 1,col =1)      

    @classmethod
    def components_direction_graph(cls,fig:go.Figure) -> None:
        explained_variances = cls.explained_variance()
        loadings = cls._pca.components_.T * np.sqrt(explained_variances)
        colors = [color.to_str() for color in get_colour_palette_rgba(cls._columns_size)]
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
                showlegend=True,
                legend='legend'
            ),row = 1,col = 2)
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='white',title_text='PCA1',row = 1,col =2)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='white',title_text='PCA2',row = 1,col =2)
    
    @classmethod
    def loadigns_graph(cls,fig:go.Figure) -> None:
        colors = [color.to_str() for color in get_colour_palette_rgba(cls._columns_size)]
        explained_variances = cls.explained_variance()
        loadings = abs(cls._pca.components_.T * np.sqrt(explained_variances))
        loading_ratio = loadings/np.sum(loadings,axis = 0)
        top_labels = cls._columns_names
        y_labels = [f'PCA{i + 1}' for i in range(cls._columns_size)]
        half_idx = cls._columns_size//2
        for i in range(cls._columns_size):
            fig.add_trace(go.Bar(
                y = y_labels[:half_idx],
                x = loading_ratio[i,:half_idx],
                name = top_labels[i],
                marker = dict(
                color=colors[i]),
                orientation='h',
                legendgroup=top_labels[i],
                legend='legend3'
            
            ),row = 2,col = 1)
        for i in range(cls._columns_size):
            fig.add_trace(go.Bar(
                y = y_labels[half_idx:],
                x = loading_ratio[i,half_idx:],
                name = top_labels[i],
                marker = dict(
                color=colors[i]),
                orientation='h',
                legendgroup=top_labels[i],
                legend='legend3',
                showlegend=False
            ),row = 2,col = 2)
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='white',title_text='Participation of basic feature',row = 2,col =2)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='white',title_text='Principal Component',row = 2,col =2)
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='white',title_text='Participation of basic feature',row = 2,col =1)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='white',title_text='Principal Component',row = 2,col =1)
        fig.update_layout(barmode='stack')
                
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