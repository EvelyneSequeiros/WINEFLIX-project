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
import dash_table
from sklearn.neighbors import NearestNeighbors
import json
from gensim.models import word2vec
from gensim.models import Word2Vec
import random
import pickle
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../assets/data").resolve()

df = pd.read_pickle(DATA_PATH.joinpath("selima_famd.pkl")).head(1000)

# df = pd.read_pickle(r'C:\Users\yacin\Desktop\dash_wine_jedha\assets\data\selima_famd.pkl').head(1000)

col_list=df.columns.tolist()
col_list.sort()
col_list=col_list[4:]

wine_title = df['title'].unique().tolist()
wine_title.append('00.Tous')
wine_title.sort()

wine_variety = df['variety'].unique().tolist()
wine_variety.append('00.Tous')
wine_variety.sort()

wine_winery = df['winery'].unique().tolist()
wine_winery.append('00.Tous')
wine_winery.sort()

wine_country = df['country'].unique().tolist()
wine_country.append('00.Tous')
wine_country.sort()

wine_province = df['province'].unique().tolist()
wine_province.append('00.Tous')
wine_province.sort()

# wine_title = df['title'].unique().tolist()
# wine_title.sort()


def generate_similar_movie(id):
    name = df[df.index.values == id]['title'].values[0]
    year = df[df.index.values == id]['years'].values[0]
    variety = df[df.index.values == id]['variety'].values[0]
    country = df[df.index.values == id]['country'].values[0]
    winery = df[df.index.values == id]['winery'].values[0]
    province = df[df.index.values == id]['province'].values[0]
    points = df[df.index.values == id]['points'].values[0]
    # desc = ', '.join(df[df.index.values == id]['normalized_descriptors'].values[0])
    
    card = dbc.Card(
        [
            dbc.CardImg(
                src="https://raw.githubusercontent.com/yacine-yame/datasets/main/winebottle.jpg", top=True),
            dbc.CardBody(
                [
                    html.H4(f"{name}", className="card-title"),
                    html.H5(f"Cépage: {str(variety)}",
                            className="card-title"),
                    html.H5(f"Année: {int(year)}",
                            className="card-title"),
                    html.H5(f"Producteur: {str(winery)}",
                            className="card-title"),
                    html.H5(f"Pays: {str(country)}",
                            className="card-title"),
                    html.H5(f"province: {str(province)}",
                            className="card-title"),
                    # html.H5(f"Arômes: {str(desc)}",
                    #         className="card-title"),
                    html.H6(f"Note sur 100: {str(points)}",
                            className="card-title"),
                ]
            ),
        ],className='tile',
        style={"width": "15rem"},
    )
    return card



layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2('Visulisation des clusters/gammes'),className='row')
    ]),
    
    dbc.Row([
            dbc.Col([
            html.Div([
                        html.Div([html.P('Nom du vin :'),
                        dcc.Dropdown(id='dropdown100', options=[{'label': i, 'value': i} for i in wine_title],value='00.Tous',clearable=False),
                        html.P('Cépage :'),
                        dcc.Dropdown(id='dropdown101', options=[{'label': i, 'value': i} for i in wine_variety],value='00.Tous',clearable=False),
                        html.P('Producteur :'),
                        dcc.Dropdown(id='dropdown102', options=[{'label': i, 'value': i} for i in wine_winery],value='00.Tous',clearable=False),
                        html.P('Pays :'),
                        dcc.Dropdown(id='dropdown103', options=[{'label': i, 'value': i} for i in wine_country],value='00.Tous',clearable=False),
                        html.P('Province :'),
                        dcc.Dropdown(id='dropdown104', options=[{'label': i, 'value': i} for i in wine_province],value='00.Tous',clearable=False),]
            ,className='dropdown_style2'),
                    ],className='row'),],width=4),

                dbc.Col([
                dcc.Graph(id='graph100', figure={},style={'height':"700px"}),
                        ],width=8)
    ]),
    
    dbc.Row([
        dbc.Col(html.H2('Visulisation des clusters/gammes'),className='row2')
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div([html.P('Choisir un vin :'),
                    dcc.Dropdown(id='dropdown105', options=[{'label': i, 'value': i} for i in wine_title],value='Quinta dos Avidagos 2011 Avidagos Red (Douro)', clearable=False)
                    ],className='dropdown_style'
                     ),
            
            html.Div(
                dbc.Row(children=[generate_similar_movie(i) for i in df.index.values], id='movies100'),className="row")
        ])              
    ])
])


# layout =html.Div([
#         html.H2('Quels vins recherchez-vous ?'),
#         html.Div([dcc.Dropdown(id='dropdown100',
#                                options=[{'label': i, 'value': i} for i in wine_title],value='00.Tous',
#                                )],style={'width': '15%', 'display': 'block', 'vertical-align': 'left'}),
#         html.Div([dcc.Dropdown(id='dropdown101',
#                                options=[{'label': i, 'value': i} for i in wine_variety],value='00.Tous',
#                               )],style={'width': '15%', 'display': 'block', 'vertical-align': 'left'}),
#         html.Div([dcc.Dropdown(id='dropdown102',
#                                options=[{'label': i, 'value': i} for i in wine_winery],value='00.Tous',
#                                )],style={'width': '15%', 'display': 'block', 'vertical-align': 'left'}),
#         html.Div([dcc.Dropdown(id='dropdown103',
#                                options=[{'label': i, 'value': i} for i in wine_country],value='00.Tous',
#                                )],style={'width': '15%', 'display': 'block', 'vertical-align': 'left'}),
#         html.Div([dcc.Dropdown(id='dropdown104',
#                                options=[{'label': i, 'value': i} for i in wine_province],value='00.Tous',
#                                )],style={'width': '15%', 'display': 'block', 'vertical-align': 'left'}),
         
#          html.Div([dcc.Graph(id='graph100', figure={},style={'height':"700px"})],style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'right'}),
         
#          html.Div([dcc.Dropdown(id='dropdown105',
#                                options=[{'label': i, 'value': i} for i in wine_title],value='Quinta dos Avidagos 2011 Avidagos Red (Douro)',
#                                )],className='dropdown_style'),
         
#          html.Div(
#             html.Div(
#                 dbc.Row(children=[generate_similar_movie(i) for i in df.index.values], className='slides', id='movies100'),
#         ),
#         )
# ])

@app.callback(Output('graph100', 'figure'),
              [Input('dropdown100', 'value'),
               Input('dropdown101', 'value'),
               Input('dropdown102', 'value'),
               Input('dropdown103', 'value'),
               Input('dropdown104', 'value'),]
              )
def update_graph1(val1,val2,val3,val4,val5):
    if val1!='00.Tous':
        dfx=df[df['title']==val1]
    else:
        dfx=df
    if val2!='00.Tous':
        dfx=dfx[dfx['variety']==val2]
    else:
        dfx=dfx
    if val3!='00.Tous':
        dfx=dfx[dfx['winery']==val3]
    else:
        dfx=dfx
    if val4!='00.Tous':
        dfx=dfx[dfx['country']==val4]
    else:
        dfx=dfx
    if val5!='00.Tous':
        dfx=dfx[dfx['province']==val5]
    else:
        dfx=dfx
    fig1 = px.scatter_3d(dfx,
                         x ="c1", y="c2",z="c3", color='Cluster_KMeans', hover_data=['title','variety','winery','country','province'])
    return fig1

@app.callback(Output(component_id='movies100', component_property='children'),
              [Input(component_id='dropdown105', component_property='value')])
def update_movies(value):
    n=df[df['title']==value]['Cluster_KMeans'].tolist()[0]
    list_ind=df[df['Cluster_KMeans']==n].index.tolist()
    list_of_choice=[]
    for x in range (8):
        num1 = random.randint(0, len(list_ind))
        list_of_choice.append(list_ind[num1])
    df_id = pd.DataFrame({'id': list_of_choice})
    return html.Div(
        html.Div(
            dbc.Row(children=[generate_similar_movie(
                i) for i in df_id['id']], className='slides')
        ),
    )