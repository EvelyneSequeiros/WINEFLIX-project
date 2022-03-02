import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output
import pandas as pd
# Connect to main app.py file
from app import app, server
# Connect to your app pages
from apps import market,search,flavor,carac

#server = app.server
# styling the sidebar
MENU_STYLE = {
    'justify': 'center',
    'color':'red'
}
# SIDEBAR_STYLE = {
#     "position": "static",
#     "top": 0,
#     "left": 0,
#     "bottom": 0,
#     "width": "600px",
#     "padding": "2rem 1rem",
#     "font-family" : 'Work Sans',
#     "margin": "0 auto",
#     'textAlign': 'center',
#     'color':'pink'
# }

# padding for the page content
CONTENT_STYLE = {
    #"padding-top": "10px",
}



sidebar = html.Div(
    [   html.Div([
        html.Img(src="assets/logo.png",
                 style={
                     'height': '100px',
                     'marginLeft': 'auto',
                     'marginRight': 'auto',
                     "margin-bottom":"15px",
                     "margin-top":"50px",
                     'textAlign': 'center',
                 },
    )],className="row"),

        # html.Hr(),
       html.Div([
        #  dcc.Link("Mon profil", href="/market", className="linkstyle"),
        dcc.Link("Données mondiales sur le vin", href="/market", className="linkstyle"),
        dcc.Link("Recommandation par arômes", href="/flavor", className="linkstyle"),
        dcc.Link("Recommandation par gammes de vins", href="/carac", className="linkstyle"),
        dcc.Link("Recherche spécifique", href="/search", className="linkstyle"),
        ],
        className="row"),
    ],
    # style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content,
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == '/market':
        return market.layout
    elif pathname == '/':
        return market.layout
    elif pathname == '/search':
        return search.layout
    elif pathname == '/flavor':
        return flavor.layout
    elif pathname == '/carac':
        return carac.layout
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )


if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(debug=True, port=3000, dev_tools_hot_reload=False)
    