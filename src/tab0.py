import dash_html_components as html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import altair as alt
import sys
import os
import plotly.express as px
import json

import pycountry_convert as pc


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def country_to_continent(country_name):
    country_name = country_name.title()
    try:
        # get country code
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        # get continent code
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        # transfer continent code into continent name
        continent_name = pc.convert_continent_code_to_continent_name(
            continent_code)
        return continent_name
    except:
        # NaN

        return pd.NA


def country_to_ISO(country_name):
    country_name = country_name.title()
    try:
        # get country code
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        # get continent code
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        return continent_code
    except:
        # NaN
        return pd.NA


def create_continent_map(column_name):

    with open('data/World_Continents.geojson', 'r') as f:
        geojson_data = json.load(f)

    # Create the choropleth map
        fig = px.choropleth(
            df_by_continent,  # DataFrame containing the data
            geojson=geojson_data,  # The loaded GeoJSON file
            # Path to the field to match with locations
            featureidkey='properties.CONTINENT',
            # Index of DataFrame that matches GeoJSON 'CONTINENT'
            locations=df_by_continent.index,
            color=column_name,  # DataFrame column whose values will be used to color the map
            projection="equirectangular"  # Map projection to be used
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            # Set the title of the map
            title_text=f'Average {column_name} Rate by Continent',
            title_x=0.5,  # Center the title
        )
        fig.update_geos(fitbounds="locations", projection_scale=1,  # Increase this value to zoom in
                        center=dict(lat=0, lon=0))
    return fig


def create_layout(app):
    layout = html.Div([
        html.Div([
            html.Div([
                html.Img(src='../assets/malnutrtion_logo1.png', style={
                    'height': 'auto',
                    'width': 'auto',
                    'max-width': '300px',
                    'max-height': '300px'
                })
            ], style={'flex': '1'}),  # This div is for the image
            html.Div([
                html.Blockquote([
                    introduction_text,
                    html.Cite("CDC", style=cite_style)
                ], style=blockquote_style)
            ], style={'flex': '3'})  # This div is for the text
        ], style={'display': 'flex', 'alignItems': 'center'}),

        html.H2("Continent Comparison", style={
                'margin-top': '20px', 'margin-left': '20px'}),
        html.Label([
            # get indicator selected
            html.Label([
                dcc.Dropdown(
                    id='column-dropdown-overview',
                    options=[{'label': i, 'value': i} for i in columns_1],
                    value='Overweight',  # Set 'Overweight' as the default option
                    placeholder="Select indicator",
                    style={'width': '50%'}
                ),
            ]),
            html.Div([
                html.H5("Indicator explanation:",
                        style={'margin-bottom': '5px'}),
                html.Div(id='indicator_explain_overview', style={
                         'font-size': 'small', 'width': '50%'}),
            ], style={'margin-bottom': '20px'}),  # Add margin between the H5 and the Div
        ]),


        # bar chart and map
        html.Div([
            # Container for the bar chart
            html.Div([
                html.Iframe(id="continent_bar", style={
                    'width': '100%', 'height': '400px'})
            ], style={'display': 'inline-block', 'width': '40%'}),

            # Container for the globe map
            html.Div([
                dcc.Graph(id='world_map_overview')
            ], style={'display': 'inline-block', 'width': '60%'})
        ]),

        # Important notes part
        html.Div([
            html.H3('Points Worth Mentioning:', style={
                    'color': '#333', 'margin-bottom': '10px'}),
            html.Ul([
                html.Li('Africa has the highest average rate of severe wasting, exceeding 2.5%.',
                        style={'margin-top': '10px'}),
                html.Li('Europe has a significantly higher average rate of overweight children, surpassing 12%.',
                        style={'margin-top': '10px'}),
                html.Li('Lack of data from Antarctica, due to less of population.',
                        style={'margin-top': '10px'})
            ], style={'list-style-type': 'none', 'padding-left': '0'}),
        ], style={'border': '1px solid #ddd', 'padding': '15px', 'border-radius': '8px'})


        # Fun fact
    ], style={'backgroundColor': '#FAF5F4'}
    )

    @app.callback(
        [Output('world_map_overview', 'figure'),
         Output('indicator_explain_overview', 'children')],
        [Input('column-dropdown-overview', 'value')]
    )
    def update_continent_map(column_name):
        if column_name is None:  # If no option is chosen, default to 'Overweight'
            column_name = 'Overweight'
        explain = growth_indicators_dict[column_name]

        # also return indicator explantion
        return create_continent_map(column_name), explain

    @app.callback(
        [Output('continent_bar', 'srcDoc')],
        [Input('column-dropdown-overview', 'value')]
    )
    def update_continent_bar(column_name):
        df_avg = pd.read_csv("data/country-wise-average.csv")
        df_avg["Continent"] = df_avg["Country"].apply(country_to_continent)
        df_by_continent = df_avg.groupby("Continent").mean(numeric_only=True)
        df_by_continent.drop("Income Classification", inplace=True, axis=1)

        df_by_continent = df_by_continent.reset_index()
        chart = alt.Chart(df_by_continent,
                          title=alt.TitleParams(
                              text=f'Average {column_name} by Continent Bar Chart',
                          )
                          ).mark_bar().encode(
            # Set label angle to 0 degrees for horizontal labels
            x=alt.X('Continent:N', axis=alt.Axis(labelAngle=0)),
            y=column_name,
            tooltip=[
                # Custom tooltip for Year
                alt.Tooltip("Continent", title="Continent"),
                alt.Tooltip(column_name, title=column_name, format='.2f')]
        ).properties(
            width='container',
            background='transparent'
        ).configure_view(
            strokeWidth=0,
            fill='transparent'
        )
        chart_html = chart.to_html()

        return (chart_html,)
    return layout


df_avg = pd.read_csv("data/country-wise-average.csv")

df_avg["Continent"] = df_avg["Country"].apply(country_to_continent)
df_by_continent = df_avg.groupby("Continent").agg('mean')
df_by_continent.drop("Income Classification", inplace=True, axis=1)


growth_indicators_dict = {
    "Income Classification": "The income classification of a country typically refers to the categorization of countries based on their gross national income (GNI) per capita. Common classifications include low-income, middle-income, and high-income countries, as defined by organizations like the World Bank.",
    "Severe Wasting": "Percentage of children aged 0–59 months who are below minus three standard deviations from median weight-for-height of the WHO Child Growth Standards.",
    "Wasting": "Moderate and severe: Percentage of children aged 0–59 months who are below minus two standard deviations from median weight-for-height of the WHO Child Growth Standards.",
    "Overweight": "Moderate and severe: Percentage of children aged 0-59 months who are above two standard deviations from median weight-for-height of the WHO Child Growth Standards.",
    "Stunting": "Moderate and severe: Percentage of children aged 0–59 months who are below minus two standard deviations from median height-for-age of the WHO Child Growth Standards.",
    "Underweight": "Moderate and severe: Percentage of children aged 0–59 months who are below minus two standard deviations from median weight-for-age of the World Health Organization (WHO) Child Growth Standards.",
    "U5 Population ('000s)": "Population of children under the age of 5, measured in thousands (000s)."
}

columns_to_drop = ["Country", "Income Classification",
                   "U5 Population ('000s)", "Continent"]

columns_1 = df_avg.drop(columns=columns_to_drop, axis=1).columns


text_style = {
    'fontFamily': 'Times New Roman, Times, serif',  # This sets the type of font
    'fontSize': '20px',  # This sets the size of the font
    'textAlign': 'center'  # This sets the alignment of the text
}

blockquote_style = {
    'borderLeft': '2px solid #ccc',
    'padding': '10px',
    'margin': '20px',
    'fontStyle': 'italic',
    'fontSize': '23px',
    'color': '#9d7666'
}

cite_style = {
    'display': 'block',
    'textAlign': 'right',
    'marginTop': '10px'
}

introduction_text = "Global malnutrition and poverty are interconnected challenges affecting billions worldwide.   As of 2022, 2.5 billion adults were overweight, including 890 million with obesity, while 390 million were underweight.   Meanwhile, 149 million children under 5 were stunted, 45 million wasted, and 37 million overweight or obese.   Malnutrition's impacts stemming from undernutrition, micronutrient deficiencies, and overnutrition affect individuals' health, economic, and social well-being, particularly in low- and middle-income countries.   Concurrently, global poverty exacerbates malnutrition, with approximately 690 million people suffering from undernutrition.  Despite some progress in reducing hunger, achieving Zero Hunger by 2030 remains a formidable goal, necessitating comprehensive efforts to transform food systems, improve nutrition, and address the root causes of poverty and inequality"


points_worth_to_mention = '''
1. Africa has the highest average rate of severe wasting, exceeding 2.5%.\n
2. Europe has a significantly higher average rate of overweight children, surpassing 12%.
'''
