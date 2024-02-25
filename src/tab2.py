import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go


MPI_nat = pd.read_csv("data/MPI_national.csv")
columns_1 = MPI_nat.drop("Country", axis=1).columns

MPI_sub = pd.read_csv("data/MPI_subnational.csv")
#countryNames = MPI_sub["Country"].unique().tolist()
#cityNames = MPI_sub["Sub-national region"].unique().tolist()

def create_world_map():
    fig = go.Figure()

    fig.add_trace(go.Choropleth(
        locations=MPI_nat["Country"],  # Make sure this column contains country names recognized by Plotly
        z=MPI_nat['MPI Urban'],        # Make sure 'MPI Urban' is the correct column name
        locationmode='country names',
        colorscale=[[0, 'lightblue'], [1, 'darkblue']],
        colorbar=dict(title='MPI Urban Rate'),
        hoverinfo='location+z'
    ))

    fig.update_layout(
        title=dict(text='Average MPI Urban Rate', x=0.5, y=0.9),
        geo=dict(
            showcoastlines=True,
            projection_type='equirectangular',
            showocean=True, oceancolor="LightBlue",
            showland=True, landcolor="White",
            showcountries=True, countrycolor="Gray"
        ),
    )
    return fig

def create_layout():
    world_map_figure = create_world_map()  
    layout = html.Div([
        html.H1("World Map of MPI Urban"),
        dcc.Graph(
            id='world-map',
            figure=world_map_figure
        ),

        

    
    ])
    return layout