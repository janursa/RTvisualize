import  sys, time, os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import numpy as np
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from time import sleep
from flask import request
file = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_scatter_data.csv"

x = [1, 2, 3, 2]
types = ["id1","id2","id2"]
trace=go.Scatter(
    x=x,
    y=x,
    mode='markers',
    showlegend = False,
    text = types,
    marker=dict(symbol = [100,200,300])
)

layout = go.Layout(
    # xaxis = dict(title = "X position", zeroline = False,range =[
    #             min(self.df[name]["data"]["x"]) - 15,
    #             max(self.df[name]["data"]["x"]) +15
    #         ]),
    # yaxis = dict(title = "Y position", zeroline = False,
    #         range =[
    #             min(self.df[name]["data"]["y"]) - 15,
    #             max(self.df[name]["data"]["y"]) +15
    #         ]),
    # height=600,
    # width=600,
    # legend=dict(
    #     x=1,
    #     y=.95,
    #     traceorder='normal',
    #     font=dict(
    #         family='sans-serif',
    #         size=12,
    #         color='#000'
    #     ),
    #     # bgcolor='#E2E2E2',
    #     bordercolor='#FFFFFF',
    #     borderwidth=1
    # ),
    annotations=[
        dict(
            x=1.16,
            y=1,
            xref='paper',
            yref='paper',
            text='<I> Cell types: </I>',
            showarrow=False
        )
    ]

)
fig = go.Figure(data=trace)

fig.show()