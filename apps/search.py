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
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../assets/data").resolve()

df = pd.read_pickle(DATA_PATH.joinpath("pickle-file.pkl"))

# df = pd.read_pickle(r'C:\Users\yacin\Desktop\dash_wine_jedha\assets\data\pickle-file.pkl').head(1000)
# df2=df[['title','variety','winery','country','province','years']]

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


def generate_similar_movie(id):
    name = df[df.index.values == id]['title'].values[0]
    year = df[df.index.values == id]['years'].values[0]
    variety = df[df.index.values == id]['variety'].values[0]
    country = df[df.index.values == id]['country'].values[0]
    winery = df[df.index.values == id]['winery'].values[0]
    province = df[df.index.values == id]['province'].values[0]
    points = df[df.index.values == id]['points'].values[0]
    
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
                    html.H6(f"Note sur 100: {str(points)}",
                            className="card-title"),
                ]
            ),
        ],className='tile',
        style={"width": "15rem"},
    )
    return card


PAGE_SIZE = 5


layout =html.Div([
        html.H2('Quels vins recherchez-vous ?'),
        html.Div([
         html.Div([html.P('Nom du vin :'),dcc.Dropdown(id='dropdown1',
                               options=[{'label': i, 'value': i} for i in wine_title],value='00.Tous',
                               )],className='dropdown_style'),
        html.Div([html.P('Cépage :'),dcc.Dropdown(id='dropdown2',
                               options=[{'label': i, 'value': i} for i in wine_variety],value='Pinot Gris',
                              )],className='dropdown_style'),
        html.Div([html.P('Producteur :'),dcc.Dropdown(id='dropdown3',
                               options=[{'label': i, 'value': i} for i in wine_winery],value='00.Tous',
                               )],className='dropdown_style'),
        html.Div([html.P('Pays :'),dcc.Dropdown(id='dropdown4',
                               options=[{'label': i, 'value': i} for i in wine_country],value='France',
                               )],className='dropdown_style'),
        html.Div([html.P('Province :'),dcc.Dropdown(id='dropdown5',
                               options=[{'label': i, 'value': i} for i in wine_province],value='Alsace',
                               )],className='dropdown_style'),
        ],className='row'),
        
        html.Div([html.P('Années:'),dcc.RangeSlider(id='my-range-slider1',
                                                        min=1990,
                                                        max=2021,
                                                        step=1,
                                                        value=[1990, 2021],tooltip = { 'always_visible': True }
                                ),]),
         
        html.Div(
            html.Div(
                dbc.Row(children=[generate_similar_movie(
            i) for i in df.index.values], className='slides', id='movies'),
        ),
        )   
])

@app.callback(Output(component_id='movies', component_property='children'),
              [Input('dropdown1', 'value'),
                Input('dropdown2', 'value'),
                Input('dropdown3', 'value'),
                Input('dropdown4', 'value'),
                Input('dropdown5', 'value'),
                Input('my-range-slider1', 'value'),])
def update_movies(value1,value2,value3,value4,value5,value6):
        if value1!='00.Tous':
                dfx=df[df['title']==value1]
        else:
                dfx=df
        if value2!='00.Tous':
                dfx=dfx[dfx['variety']==value2]
        else:
                dfx=dfx
        if value3!='00.Tous':
                dfx=dfx[dfx['winery']==value3]
        else:
                dfx=dfx
        if value4!='00.Tous':
                dfx=dfx[dfx['country']==value4]
        else:
                dfx=dfx
        if value5!='00.Tous':
                dfx=dfx[dfx['province']==value5]
        else:
                dfx=dfx
        if value6!='00.Tous':
                dfx=dfx[(dfx['years']>value6[0])&(dfx['years']<value6[1])]
        else:
                dfx=dfx
        list_index=dfx.index.values        
        return html.Div(html.Div(dbc.Row(children=[generate_similar_movie(i) for i in list_index], className='slides'))),
