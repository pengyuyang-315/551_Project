from src import tab2, tab1, tab0
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import flask
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = dash.Dash(__name__)
server = app.server


@server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(server.root_path, 'static'), 'favicon.ico')


app.title = "Malnutrition and poverty cross the globe"
print("Current working directory set to:", os.getcwd())

app.layout = html.Div([
    html.Div([
        dcc.Tabs(id='tabs',
                 value='tab-0',
                 children=[
                    dcc.Tab(label='Overview', value='tab-0',
                            children=tab0.create_layout(app)),
                    dcc.Tab(label='Malnutrition', value='tab-1',
                            children=tab1.create_layout(app)),
                    dcc.Tab(label='Poverty', value='tab-2',
                            children=tab2.create_layout(app)),
                 ]),
        html.Hr(),
    ], style={'position': 'relative', 'min-height': '100vh'}),

])


server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8964)
