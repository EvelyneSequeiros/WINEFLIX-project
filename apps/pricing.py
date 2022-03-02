import os
from app import app
import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Div import Div
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import numpy as np


layout = html.Div([dcc.Input(
                            id="input_{}",className='div-main')])

# @app.callback(
#             Output("graph6", "figure"),
#             [Input("dropdown6", "value"),
#              Input("dropdown7", "value"),
#              Input("dropdown8", "value"),
#              Input("dropdown9", "value")])
# def update_graph4(val1,val2,val3,val4):
#     test2 = df6.sort_values(ascending=False, by='price')
#     if val1=='00.All':
#         dfwinery1=test2
#     else:
#         dfwinery1 = test2[test2['variety']==val1]

#     if val2=='00.All':
#         dfwinery2=dfwinery1
#     else:
#         dfwinery2 = dfwinery1[dfwinery1['winery']==val2]

#     if val3=='00.All':
#         dfwinery3=dfwinery2
#     else:
#         dfwinery3 = dfwinery2[dfwinery2['country']==val3]

#     if val3=='00.All':
#         dfwinery4=dfwinery3
#     else:
#         dfwinery4 = dfwinery3[dfwinery3['province']==val4]

#     fig7 = px.bar(dfwinery4.head(50), x="winery", y="points",hover_data=["title","price"],title="Stats sur points/price/bouteille")
#     fig7.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
#     return fig7