import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import dash_bootstrap_components as dbc
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import tab2, tab1, tab0

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.title = "Malnutrition and poverty cross the globe"
print("Current working directory set to:", os.getcwd())

app.layout = html.Div([
    html.Div([
        html.Img(src='assets/logo5.png', height='100%', width='6%', style={'display': 'inline-block', 'vertical-align': 'middle'}),
        html.H2("Beyond Borders: Malnutrition & Poverty", style={'display': 'inline-block', 'vertical-align': 'middle', 'font-family':' Georgia', 'font-size': '200%', 'margin': '0 auto','color': 'white'}),
    ], style={'position': 'relative', 'height': '100%', 'width': '100%', 'background-color': '#293F54', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
    html.Div([
        dcc.Tabs(
            id='tabs',
            value='tab0',  # Set the default tab ID here
            children=[
                dcc.Tab(
                    label='General',
                    value='tab0',
                    children=tab0.create_layout(app),
                    style={
                        'font-family': 'Georgia',
                        'font-size': '120%',
                        'background-color': 'lightgrey',
                        'border-width': '0'
                    },
                    selected_style={
                        'font-family': 'Georgia',
                        'font-size': '120%',
                        'background-color': '#FAF5F4',
                        'border-width': '0'
                    }
                ),
                dcc.Tab(
                    label='Something About Malnutrition',
                    value='tab1',
                    children=tab1.create_layout(app),
                    style={
                        'font-family': 'Georgia',
                        'font-size': '120%',
                        'background-color': 'lightgrey',
                        'border-width': '0'
                    },
                    selected_style={
                        'font-family': 'Georgia',
                        'font-size': '120%',
                        'background-color': '#FAF5F4',
                        'border-width': '0'
                    }
                ),
                dcc.Tab(
                    label='Facts for Poverty',
                    value='tab2',
                    children=tab2.create_layout(app),
                    style={
                        'font-family': 'Georgia',
                        'font-size': '120%',
                        'background-color': 'lightgrey',
                        'border-width': '0'
                    },
                    selected_style={
                        'font-family': 'Georgia',
                        'font-size': '120%',
                        'background-color': '#FAF5F4',
                        'border-width': '0'
                    }
                )
            ]
        )

    ]),
])




    
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8964)
