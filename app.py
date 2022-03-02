import dash
import dash_bootstrap_components as dbc
import os

external_scripts = [{"src": "https://unpkg.com/swup@latest/dist/swup.min.js"}]
external_stylesheets=[dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server
# server.secret_key = os.environ.get('secret_key', 'secret')

# app = dash.Dash(__name__, suppress_callback_exceptions=True,
#                 external_stylesheets=[dbc.themes.BOOTSTRAP],
#                 external_scripts=external_scripts,
#                 assets_ignore=".js",
#                 meta_tags=[{'name': 'viewport',
#                             'content': 'width=device-width, initial-scale=1.0'}]
#                 )

# server = app.server

# server = Flask(__name__)
# app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)
# app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# for your home PostgreSQL test table
# app.server.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:your_password@localhost/test"

# for your live Heroku PostgreSQL database
# app.server.config["SQLALCHEMY_DATABASE_URI"] = "postgres://hnvfmsfibmqcrb:65caa21039f8501ae1dbdf9a3628b20d9855871cbcc122a6189eba8e0083c30f@ec2-34-253-116-145.eu-west-1.compute.amazonaws.com:5432/d7fm23seuj26me"

# db = SQLAlchemy(app.server)
