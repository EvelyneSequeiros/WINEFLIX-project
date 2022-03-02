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
import pathlib
import boto3
import pickle


s3 = boto3.resource('s3', aws_access_key_id = 'AKIAUBEGQUNA73KA635C', aws_secret_access_key = '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')
wine_word2vec_model = pickle.loads(s3.Bucket("wine-yame-project").Object("wine_word2vec_model.model").get()['Body'].read())

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../assets/data").resolve()

df = pd.read_pickle(DATA_PATH.joinpath("pickle-file.pkl"))
descriptor_mapping = pd.read_csv(DATA_PATH.joinpath("descriptor_mapping.csv"))

jsonfile = DATA_PATH.joinpath("dict_of_tfidf_weightings.json")
# modelfile = DATA_PATH.joinpath("wine_word2vec_model.model")

# df = pd.read_pickle(r'C:\Users\yacin\Desktop\dash_wine_jedha\assets\data\pickle-file.pkl').head(1000)
# descriptor_mapping = pd.read_csv(r'C:\Users\yacin\Desktop\dash_wine_jedha\assets\data\descriptor_mapping.csv')
# df = pd.read_csv(r"C:\Users\yacin\Desktop\dash_wine_jedha\assets\data\dfrecofilter.csv").head(5000)
# df = preprocess.df
# df2=df[['title','variety','winery','country','province','years']]

wine_title = df['title'].unique().tolist()
# wine_title.append('00.Tous')
wine_title.sort()

# wine_variety = df['variety'].unique().tolist()
# wine_variety.append('00.Tous')
# wine_variety.sort()

# wine_winery = df['winery'].unique().tolist()
# wine_winery.append('00.Tous')
# wine_winery.sort()

# wine_country = df['country'].unique().tolist()
# wine_country.append('00.Tous')
# wine_country.sort()

# wine_province = df['province'].unique().tolist()
# wine_province.append('00.Tous')
# wine_province.sort()

wine_mapping = descriptor_mapping['level_3'].unique().tolist()
wine_mapping.sort()

input_vectors = list(df['review_vector'])
input_vectors_listed = [a.tolist() for a in input_vectors]
input_vectors_listed = [a[0] for a in input_vectors_listed]
knn = NearestNeighbors(n_neighbors=5, algorithm= 'brute', metric='cosine')
model_knn = knn.fit(input_vectors_listed)
name_test='Quinta dos Avidagos 2011 Avidagos Red (Douro)'
wine_test_vector = df.loc[df['title'] == name_test]['review_vector'].tolist()[0]
distance, indice = model_knn.kneighbors(wine_test_vector, n_neighbors=5)
df_id = pd.DataFrame({'id': list(indice[0])})


with open(jsonfile) as jsonFile:
    dict_of_tfidf_weightings = json.load(jsonFile)
    jsonFile.close()
    
# wine_word2vec_model = Word2Vec.load(modelfile)


# list_of_descriptors=['complex', 'high_acid', 'fresh', 'grass', 'lime']
# number_of_suggestions=5
# weighted_review_terms = []
# for term in list_of_descriptors:
#     if term not in dict_of_tfidf_weightings:
#         if term not in descriptor_mapping.index:
#             print('choose a different descriptor from', term)
#             continue
#         else:
#             term = descriptor_mapping['normalized'][term]
#         tfidf_weighting = dict_of_tfidf_weightings[term]
#         word_vector = wine_word2vec_model.wv.get_vector(term).reshape(1, 300)
#         weighted_word_vector = tfidf_weighting * word_vector
#         weighted_review_terms.append(weighted_word_vector)
#     review_vector = sum(weighted_review_terms)
    
#     distance, indice = model_knn.kneighbors(review_vector, n_neighbors=number_of_suggestions+1)
#     distance_list = distance[0].tolist()[1:]
#     indice_list = indice[0].tolist()[1:]



def generate_similar_movie(id):
    name = df[df.index.values == id]['title'].values[0]
    year = df[df.index.values == id]['years'].values[0]
    variety = df[df.index.values == id]['variety'].values[0]
    country = df[df.index.values == id]['country'].values[0]
    winery = df[df.index.values == id]['winery'].values[0]
    province = df[df.index.values == id]['province'].values[0]
    points = df[df.index.values == id]['points'].values[0]
    desc = ', '.join(df[df.index.values == id]['normalized_descriptors'].values[0])
    
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
                    html.H5(f"Arômes: {str(desc)}",
                            className="card-title"),
                    html.H6(f"Note sur 100: {str(points)}",
                            className="card-title"),
                ]
            ),
        ],className='tile',
        style={"width": "15rem"},
    )
    return card



# layout =html.Div([
#         html.H2('Quels vins recherchez-vous ?'),
#         html.Div([dcc.Dropdown(id='dropdown6',
#                                options=[{'label': i, 'value': i} for i in wine_title],value='Quinta dos Avidagos 2011 Avidagos Red (Douro)',
#                                )],className='dropdown_style'),         
#         html.Div(
#             html.Div(
#                 dbc.Row(children=[generate_similar_movie(
#             i) for i in df_id['id']], className='slides', id='movies36'),
#         ),
#         )   
# ]),

layout =html.Div([
        html.Div([html.H2('Choisir la méthode de recommendation :')],className="row"),
        dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
            dcc.Tab(label='Par titre de vin', value='tab-1-example-graph'),
            dcc.Tab(label='Par arômes voulus', value='tab-2-example-graph'),
        ]),
        html.Div(id='tabs-content-example-graph')
    ])

# @app.callback(Output(component_id='movies36', component_property='children'),
#               [Input('dropdown6', 'value'),
#                 ])
# def update_movies(value40):
#         name_test=value40
#         wine_test_vector = df.loc[df['title'] == name_test]['review_vector'].tolist()[0]
#         distance, indice = model_knn.kneighbors(wine_test_vector, n_neighbors=3)
#         distance_list = distance[0].tolist()[1:]
#         indice_list = indice[0].tolist()[1:]
#         return html.Div(html.Div(dbc.Row(children=[generate_similar_movie(i) for i in indice_list], className='slides'))),


@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
        html.Div([html.P('Recommandation pour le vin:'),dcc.Dropdown(id='dropdown6',
                               options=[{'label': i, 'value': i} for i in wine_title],value='Quinta dos Avidagos 2011 Avidagos Red (Douro)',
                               )],className='dropdown_style'),         
        html.Div(
            html.Div(
                dbc.Row(children=[generate_similar_movie(
            i) for i in df_id['id']], className='slides', id='movies36'),
        ),
        )])
    elif tab == 'tab-2-example-graph':
        return html.Div([
            html.Div([        
                    html.Div([html.P('Choisir arôme n°1 :'),dcc.Dropdown(id='dropdown7',
                               options=[{'label': i, 'value': i} for i in wine_mapping],value='complex',
                               )],className='dropdown_style'),
                    html.Div([html.P('Choisir arôme n°2 :'),dcc.Dropdown(id='dropdown8',
                               options=[{'label': i, 'value': i} for i in wine_mapping],value='high_acid',
                               )],className='dropdown_style'),
                    html.Div([html.P('Choisir arôme n°3 :'),dcc.Dropdown(id='dropdown9',
                               options=[{'label': i, 'value': i} for i in wine_mapping],value='fresh',
                               )],className='dropdown_style'),
                    html.Div([html.P('Choisir arôme n°4 :'),dcc.Dropdown(id='dropdown10',
                               options=[{'label': i, 'value': i} for i in wine_mapping],value='grass',
                               )],className='dropdown_style'),
                    html.Div([html.P('Choisir arôme n°5 :'),dcc.Dropdown(id='dropdown11',
                               options=[{'label': i, 'value': i} for i in wine_mapping],value='lime',
                               )],className='dropdown_style'),  
                ],className='row'),
            
        html.Div(
            html.Div(
                dbc.Row(children=[generate_similar_movie(
            i) for i in df_id['id']], className='slides', id='movies37'),
        ),
        )])

@app.callback(Output(component_id='movies36', component_property='children'),
              [Input(component_id='dropdown6', component_property='value')])
def update_movies(value):
    wine_test_vector = df.loc[df['title'] == value]['review_vector'].tolist()[0]
    distance, indice = model_knn.kneighbors(wine_test_vector, n_neighbors=5)
    df_id = pd.DataFrame({'id': list(indice[0])})
    return html.Div(
        html.Div(
            dbc.Row(children=[generate_similar_movie(
                i) for i in df_id['id']], className='slides')
        ),
    )

@app.callback(Output(component_id='movies37', component_property='children'),
              [Input(component_id='dropdown7', component_property='value'),
               Input(component_id='dropdown8', component_property='value'),
               Input(component_id='dropdown9', component_property='value'),
               Input(component_id='dropdown10', component_property='value'),
               Input(component_id='dropdown11', component_property='value'),])
def descriptors_to_best_match_wines(value1,value2,value3,value4,value5):
    list_of_descriptors=[value1,value2,value3,value4,value5]
    number_of_suggestions=6
    weighted_review_terms = []
    for term in list_of_descriptors:
        if term not in dict_of_tfidf_weightings:
            if term not in descriptor_mapping.index:
                print('choose a different descriptor from', term)
                continue
            else:
                term = descriptor_mapping['normalized'][term]
        tfidf_weighting = dict_of_tfidf_weightings[term]
        word_vector = wine_word2vec_model.wv.get_vector(term).reshape(1, 300)
        weighted_word_vector = tfidf_weighting * word_vector
        weighted_review_terms.append(weighted_word_vector)
    review_vector = sum(weighted_review_terms)
    
    distance, indice = model_knn.kneighbors(review_vector, n_neighbors=number_of_suggestions+1)
    # distance_list = distance[0].tolist()[1:]
    # indice_list = indice[0].tolist()[1:]
    df_id = pd.DataFrame({'id': list(indice[0])})
    return html.Div(
        html.Div(
            dbc.Row(children=[generate_similar_movie(
                i) for i in df_id['id']], className='slides')
        ),
    )

# def update_movies(value):
#     wine_test_vector = df.loc[df['title'] == value]['review_vector'].tolist()[0]
#     distance, indice = model_knn.kneighbors(wine_test_vector, n_neighbors=5)
#     df_id = pd.DataFrame({'id': list(indice[0])})
#     return html.Div(
#         html.Div(
#             dbc.Row(children=[generate_similar_movie(
#                 i) for i in df_id['id']], className='slides')
#         ),
#     )