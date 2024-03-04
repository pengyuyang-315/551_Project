# import dash_html_components as html
# import dash_core_components as dcc

# def create_layout(app):
#     layout = html.Div([
#         html.Div("tab-2 content")
#     ])
#     return layout

from dash import Dash, dcc, html, Input, Output
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import datetime

MPI_nat = pd.read_csv("data/MPI_national.csv")
columns_1 = MPI_nat.drop("Country", axis=1).columns

MPI_sub = pd.read_csv("data/MPI_subnational.csv")
countryNames = MPI_sub["Country"].unique().tolist()


def create_world_map_1(column_name):
    fig = go.Figure()
    print("start plotting")
    print(column_name)
    fig.add_trace(go.Choropleth(

        locations=MPI_nat["Country"],
        z=MPI_nat[column_name],
        locationmode='country names',
        colorscale='YlOrRd',
        colorbar=dict(title=column_name + ' Rate'),
        hoverinfo='location+z'
    ))

    fig.update_layout(
        title=dict(text='Average ' + column_name + ' Rate', x=0.5, y=0.9),
        geo=dict(
            showcoastlines=True,
            projection_type='equirectangular',
            showocean=True, oceancolor="LightBlue",
            showland=True, landcolor="White",
            showcountries=True, countrycolor="Gray"
        ),
    )

    return fig


def create_layout(app):

    layout = html.Div([
        html.H2("Poverty Data Visualization", style={
                'margin-top': '20px', 'margin-left': '20px'}),
        html.Label([
            dcc.Dropdown(
                id='columns-dropdown',
                # Assuming MPI_nat.columns contains the columns you want to include in the dropdown
                options=[{'label': col, 'value': col}
                         for col in MPI_nat.columns if col != 'Country'],
                value='MPI Urban',  # Assuming 'MPI Urban' is a default option you want to set
                placeholder="Select indicator",
                style={'width': '50%'}
            ),
        ], style={'margin-bottom': '20px'}),
        dcc.Graph(id='world-map-1',
                  style={'width': '100%', 'height': '480px'}),
    ], style={'height': '420px'})

    @app.callback(
        Output('world-map-1', 'figure'),
        Input('columns-dropdown', 'value')
    )
    def update_world_map1(column_name):
        if column_name is None:
            column_name = 'MPI Urban'
        return create_world_map_1(column_name)

    return layout

# ... your Dash app initialization and server code ...
