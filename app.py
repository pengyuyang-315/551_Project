import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import tab2, tab1, tab0

app = dash.Dash(__name__)
server = app.server

app.title = "Malnutrition and poverty cross the globe"
print("Current working directory set to:", os.getcwd())

app.layout = html.Div([
    html.Div([
        html.Img(src='assets/logo2.jpeg', height='100vh', width='100vw', style={'display': 'inline-block', 'padding-bottom': 8}),
        dcc.Tabs(
            id='tabs',
            value='tab1',  # Set the default tab ID here
            children=[
                dcc.Tab(label='Overview', value='tab0', children=tab0.create_layout(app)),
                dcc.Tab(label='Malnutrition', value='tab1', children=tab1.create_layout(app)),
                dcc.Tab(label='Poverty', value='tab2', children=tab2.create_layout(app)),
            ]
        ),

        html.Hr(),
    ], style={'position': 'relative', 'min-height': '100vh'}),
    
])


    
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8964)