#!/usr/bin/env python
# coding: utf-8

from plotly.subplots import make_subplots
from matplotlib.lines import Line2D
from termcolor import colored
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import warnings
import plotly.express as px
warnings.filterwarnings('ignore')
from plotly.offline import iplot, init_notebook_mode
import chart_studio.plotly as py
import plotly.graph_objs as go
import cufflinks as cf
cf.go_offline(connected=True)
init_notebook_mode(connected=True)



def MakePlots(data, col,col2,barmode,opacity,rend, title):
    
    data = data.groupby(by=[col, col2]).size().reset_index(name="counts")
    fig = px.bar(data_frame=data, x=col, y="counts", color=col2, barmode=barmode,opacity=opacity)
    fig.update_layout(xaxis={'categoryorder':'category ascending'},
                      height=600, width=1000, title=title)
    fig.show(renderer=rend)
    


def plot_bar_polar(data, col, col2,height,width,barmode,rend,title):
    
    data = data.groupby(by=[col, col2]).size().reset_index(name="frequency")
    fig = px.bar_polar(data, r="frequency", color=col, title=title,height=height, width=width,
        theta=col2, template="plotly_dark", barmode=barmode,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig.show(renderer=rend)


def plot_dostributions(data, cols, title,nbins,opacity,bool, barmode='group'):
    
    layout1 = cf.Layout(width=1000, height=650,title=title)
    data[cols].iplot(kind='hist', xTitle='Value',bins=nbins, theme = 'polar', layout=layout1,
                     histnorm='percent',opacity=opacity,barmode=barmode,online=bool,
                  yTitle='% count')


def use_bar(data, cols, opacity,rend,tracew,title,barmode='group'):

    pd.options.plotting.backend = "plotly"
    data = data.groupby(by=cols).size().reset_index(name="counts")
    fig = data.plot.bar(x=cols, y='counts',barmode=barmode,opacity=opacity)
    fig.update_layout(xaxis={'categoryorder':'category ascending'},
                      height=600, width=1000, title=title)
    fig.update_traces(marker_line_width=tracew)
    fig.show(renderer=rend)


def plot_heatmap(data):
    
    correlation = data.corr(method='pearson')
    df_lt = correlation.where(np.tril(np.ones(correlation.shape)).astype(np.bool))
    fig = px.imshow(df_lt, origin='upper', title='Correlation between features',
                    width=1200,height=1100, aspect='equal')
    #fig.update_layout(width=1200, height=1200, title='')
    fig.show()





