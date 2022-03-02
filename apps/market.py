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
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../assets/data").resolve()

df = pd.read_pickle(DATA_PATH.joinpath("pickle-file.pkl"))
df1 = pd.read_csv(DATA_PATH.joinpath("coutriesdf.csv"))
df2 = pd.read_csv(DATA_PATH.joinpath("coutriesdf2.csv"))
df3 = pd.read_csv(DATA_PATH.joinpath("winerydf.csv"))

# df = pd.read_pickle(r'C:\Users\yacin\Desktop\dash_wine_jedha\assets\data\pickle-file.pkl').head(1000)
# df1 = pd.read_csv(r"C:\Users\yacin\PycharmProjects\wine_project_checkpoint22072021\assets\data\coutriesdf.csv")
# df2 = pd.read_csv(r"C:\Users\yacin\PycharmProjects\wine_project_checkpoint22072021\assets\data\coutriesdf2.csv")
# df3=pd.read_csv(r"C:\Users\yacin\PycharmProjects\wine_project_checkpoint22072021\assets\data\winerydf.csv")
# df=pd.read_csv(r"C:\Users\yacin\PycharmProjects\wine_project_checkpoint22072021\assets\data\winerydf.csv")

list_var=df3['variety'].unique()
list_var2=np.append(list_var,'00.All')


layout = html.Div([html.H2('Le marché mondial du vin :'),
    
    html.Div([
            html.Div([html.Div([dcc.Dropdown(id='dropdown1', options=[
                                                                        {'label': 'Nombre de référence', 'value': 'title_grade'},
                                                                        {'label': 'Prix moyen des vins', 'value': 'price_grade'},
                                                                        {'label': 'Note moyenne des vins', 'value': 'points_grade'},
                                                                        {'label': 'Nombre de cépages', 'value': 'Variety_grade'}
                                                                        ],value='title_grade')],className='dropdown_style'),
                      ],className='row'),

        
            html.Div([dcc.Graph(id='graph1', figure={},style={'height':"700px"})])
        
        ],className='first_map'),

    html.Div([html.H2('Benchmark par cépage :'),
        html.Div([
            html.Div([dcc.Dropdown(id='dropdown2',
                               options=[{'label': i, 'value': i} for i in list_var2],
                               value='Bordeaux-style Red Blend')],className='dropdown_style'),
            html.Div([dcc.Dropdown(id='dropdown3',
                               options=[
                                   {'label': 'Nombre de référence', 'value': 'title_grade'},
                                   {'label': 'Prix moyen des vins', 'value': 'price_grade'},
                                   {'label': 'Note moyenne des vins', 'value': 'points_grade'}
                               ],
                               value='title_grade')],className='dropdown_style'),
            ],className='row'),

        html.Div([dcc.Graph(id='graph2', figure={}, style={'height':"700px"})])
],className='second_map'),

    html.Div([html.H2('Benchmark des producteurs de vins :'),
        html.Div([html.Div([dcc.Dropdown(id='dropdown4', options=[{'label': i, 'value': i} for i in list_var2],   value='Bordeaux-style Red Blend')
                            ],className='dropdown_style'),
        html.Div([dcc.Dropdown(id='dropdown5',options=[{'label': 'Nombre de référence', 'value': 'title'},
                                                        {'label': 'Prix moyen des vins', 'value': 'price'},
                                                        {'label': 'Note moyenne des vins', 'value': 'points'}],value='title')
                  ],className='dropdown_style'),
        ],className='row'),
        
        html.Div([dcc.Graph(id='graph3', figure={}, style={'height':"700px"})])
],className='second_map')


],className='div-main')

@app.callback(
            Output("graph1", "figure"),
            [Input("dropdown1", "value")])
def update_graph1(val):
    fig1 = px.choropleth(df1, locations="iso_alpha",
                    color=val,
                    hover_name="country",
                    hover_data=["title","price","points","variety"],
                    color_continuous_scale="Viridis",
                    title="Carte benchmark mondial")
    fig1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return fig1

@app.callback(
            Output("graph2", "figure"),
            [Input("dropdown2", "value"),
             Input("dropdown3", "value"),])
def update_graph2(val1,val2):
    fig2 = px.choropleth(df2[df2['variety']==val1], locations="iso_alpha",
                    color=val2,
                    hover_name="country",
                    hover_data=["title","price","points"],
                    color_continuous_scale="Viridis",
                    title="Carte stats selon cépage")
    fig2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return fig2

@app.callback(
            Output("graph3", "figure"),
            [Input("dropdown4", "value"),
             Input("dropdown5", "value")])
def update_graph3(val1,val2):
    test = df3.sort_values(ascending=False, by=[val2])
    if val1=='00.All':
        dfwinery=test
    else:
        dfwinery = test[test['variety']==val1]

    fig3 = px.bar(dfwinery.head(50), x="winery", y=val2,hover_data=["title","price","points"],title="Stats sur winery")
    fig3.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
    return fig3


