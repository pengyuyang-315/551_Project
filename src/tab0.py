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


# def create_continent_map(column_name):

#     with open('data/World_Continents.geojson', 'r') as f:
#         geojson_data = json.load(f)

#     # Create the choropleth map
#         fig = px.choropleth(
#             df_by_continent,  # DataFrame containing the data
#             geojson=geojson_data,  # The loaded GeoJSON file
#             # Path to the field to match with locations
#             featureidkey='properties.CONTINENT',
#             # Index of DataFrame that matches GeoJSON 'CONTINENT'
#             locations=df_by_continent.index,
#             color=column_name,  # DataFrame column whose values will be used to color the map
#             projection="orthographic"  # Map projection to be used
#         )
#         fig.update_layout(
#             paper_bgcolor='rgba(0,0,0,0)',
#             # Set the title of the map
#             title_text=f'Average {column_name} Rate by Continent',
#             title_x=0.5,  # Center the title
#         )
#         fig.update_geos(fitbounds="locations", projection_scale=1,  # Increase this value to zoom in
#                         center=dict(lat=0, lon=0))
#     return fig

def create_continent_map(column_name):

    with open('data/World_Continents.geojson', 'r') as f:
        geojson_data = json.load(f)

    # Create the choropleth map
    fig = px.choropleth(
        df_by_continent,  # DataFrame containing the data
        geojson=geojson_data,  # The loaded GeoJSON file
        # Path to the field to match with locations
        featureidkey='properties.CONTINENT',
        # Column in DataFrame that matches GeoJSON 'CONTINENT'
        locations=df_by_continent.index,
        color=column_name,  # DataFrame column whose values will be used to color the map
        projection="orthographic"  # Change to a globe projection
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            showland=True,
            landcolor="lightgrey",
            showocean=True,
            oceancolor="azure",
            showlakes=True,
            lakecolor="azure",
            showrivers=True,
            rivercolor="azure",
            showcountries=False,
            showframe=False,
            projection_scale=1,  # Increase this value to zoom in
            center=dict(lat=0, lon=0),  # Center on the map
        ),
        width=800,  # Adjust these values to increase or decrease the size of the globe
        height=600
    )

    return fig

# Call the function with the column name you want to visualize
# For example: create_continent_map('Overweight').show()

    # The update_geos call is not needed since we're already setting the geo properties in update_layout.
    # If you wanted to customize aspects of the geographic layout further, you could use update_geos here.

    return fig


def create_layout(app):
    layout = html.Div([
        html.Div([
            html.Div([
                html.Iframe(
                    src="https://www.youtube.com/embed/sNozVZ_-wdA",
                    width="560",
                    height="315",
                    style={"marginLeft": "20px"}
                )
            ], style={'flex': '1'}),  # This div is for the image
            html.Div([
                html.Blockquote([
                    introduction_text,
                    html.Cite("CDC", style=cite_style)
                ], style=blockquote_style)
            ], style={'flex': '3'})  # This div is for the text
        ], style={'display': 'flex', 'alignItems': 'center'}),


        html.H2("Continent Brief Comparison", style={
                'margin-top': '20px', 'text-align': 'center'}),
        html.Div([
            # Dropdown for selecting an indicator
            html.Label([
                dcc.Dropdown(
                    id='column-dropdown-overview',
                    options=[{'label': i, 'value': i} for i in columns_1],
                    value='Stunting',  # Set 'Overweight' as the default option
                    placeholder="Select indicator",
                    # Adjusted width and added minimum width
                    style={'width': '15%', 'minWidth': '300px',
                           'text-align': 'center'}
                ),
            ], style={'display': 'flex', 'justify-content': 'center', 'width': '100%'}),  # Center the dropdown and ensure it fits in the div

            # Container for explanation text
            html.Div([
                # html.H5("Indicator explanation:",
                #         style={'margin-bottom': '5px'}),
                html.Div(id='indicator_explain_overview', style={
                    'font-size': 'small', 'width': '100%', 'text-align': 'center'}),  # Adjusted width to 100%
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'margin-top': '20px', 'margin-bottom': '20px', 'width': '50%'}),  # Adjusted width to 100%
        ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'width': '100%'}),  # Adjusted width to 100%


        # Container for the globe map
        html.Div([
            # html.Iframe(src="assets/temp.jpeg/",
            #             style={
            #                 'width': '100%',  # This will make the image take the full width of its parent
            #                 'height': 'auto',  # Adjusts the height automatically to keep the aspect ratio
            #                 'display': 'block',  # Ensures that the image doesn't inline with other elements
            #                 'object-fit': 'contain'  # Adjusts the image to fit within the container
            #             }),
            dcc.Graph(id='world_map_overview'),

        ], style={'display': 'flex',
                  'justify-content': 'center',
                  'align-items': 'center', 'width': '100%', 'height': '100%'}),

        # bar chart
        # html.H2("Comparative Brief Analysis of Child Nutritional Status Across Continents", style={
        #     'margin-top': '20px', 'text-align': 'center'}),

        html.Div([
            html.Iframe(id="continent_bar", style={
                # 'block' can also work if you want it to be the only element on the row
                'display': 'block',

                'width': '100%',  # Adjust the width as necessary
                'height': '600px'
            })
        ], style={'text-align': 'center', 'width': '100%', 'height': '100%'}),

        html.Div([
            # Container for the bar chart
        ]),


        # html.H2("Overall Global Trend"),
        # time series
        html.Div([
            html.Iframe(
                srcDoc=chart_html_time_series,
                style={'width': '100%', 'height': '400px', 'border': '0px'}
            )
        ]),
        # stunting trendline
        html.Div([
            html.Iframe(
                srcDoc=stuning_chart_html,
                style={'width': '100%', 'height': '400px', 'border': '0px'}
            )
        ]),

        html.Div([
            html.H3(
                "The situation seems to be improving, but... is it too soon to celebrate?")
        ], style={"text-align": "center"}),

        # Important notes part
        # html.Div(id="notes", style={
        #          'border': '1px solid #ddd', 'padding': '15px', 'border-radius': '8px'})

        html.Div([
            html.Div([
                html.H2("Reflecting on the Data:", style={
                    'textAlign': 'center',
                    'color': '#AEBD93',  # White color for better contrast
                    'textShadow': '2px 2px 4px #000000'  # Black shadow for readability
                }),
                html.P("Global malnutrition extends across all continents, affecting billions. In 2022, 2.5 billion adults were overweight, with a significant number also underweight, demonstrating the dual burden of malnutrition.",
                       style={'textAlign': 'justify', 'backgroundColor': 'rgba(255, 255, 255, 0.8)', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}),
                html.P("Stunting in 149 million children under 5 is more than a height issue. It signifies prolonged nutritional deficiencies with long-term impacts on physical and cognitive development.",
                       style={'textAlign': 'justify', 'backgroundColor': 'rgba(255, 255, 255, 0.8)', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}),
                html.P("A decline in infant mortality rates suggests progress, yet persistent gender disparities call for more targeted actions.",
                       style={'textAlign': 'justify', 'backgroundColor': 'rgba(255, 255, 255, 0.8)', 'padding': '20px', 'borderRadius': '10px'}),
            ], className="reflection-section", style={'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}),

            html.Div([
                html.H2("Looking Ahead:", style={
                    'textAlign': 'center',
                    # White color for better contrast
                    'color': '#7796B2',
                    'textShadow': '2px 2px 4px #000000'  # Black shadow for readability
                }),
                html.P("Achieving Zero Hunger by 2030 is an ambitious goal necessitating a transformation in our food systems to enhance nutrition and address the root causes of poverty and inequality.",
                       style={'textAlign': 'justify', 'backgroundColor': 'rgba(255, 255, 255, 0.8)', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}),
                html.P("The first 1000 days of life are crucial. Improved nutrition during this period sets a solid foundation for the future.",
                       style={'textAlign': 'justify', 'backgroundColor': 'rgba(255, 255, 255, 0.8)', 'padding': '20px', 'borderRadius': '10px'}),
            ], className="looking-ahead-section", style={'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}),

            html.Div([
                html.H2("Call to Action:", style={
                    'textAlign': 'center',
                    # White color for better contrast
                    'color': 'rgb(190,52,85)',
                    'textShadow': '2px 2px 4px #000000'  # Black shadow for readability
                }),
                html.P("Let's remember, behind these statistics are real lives. It's essential to convert data insights into tangible actions, assuring every child a healthy start in life.",
                       style={'textAlign': 'justify', 'backgroundColor': 'rgba(255, 255, 255, 0.8)', 'padding': '20px', 'borderRadius': '10px'}),
            ], className="call-to-action-section", style={'padding': '20px', 'borderRadius': '10px'}),
        ], style={
            'backgroundImage': 'url(/assets/background3.png)',
            'backgroundSize': 'cover',
            'backgroundPosition': 'center center',
            'padding': '20px'
        })





        # Fun fact
    ], style={'backgroundColor': '#FAF5F4'}
    )

    @app.callback(
        [Output('world_map_overview', 'figure'),
         Output('indicator_explain_overview', 'children')
         ],
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
        df_by_continent.drop("U5 Population ('000s)", axis=1, inplace=True)
        df_long = df_by_continent.melt(
            id_vars=['Continent'], var_name='Category', value_name='Value')
        individual_chart_width = 1200 / 6  # Adjust 800 to match your page width if needed

        base = alt.Chart(df_long).mark_bar().encode(
            x=alt.X('Category:N', title=None, axis=alt.Axis(labelAngle=-45)),
            y=alt.Y('Value:Q', title='Percentage'),
            color='Category:N',
            tooltip=['Continent', 'Category', 'Value']
        ).properties(
            width=individual_chart_width,  # Use the calculated width here
            height=400
        )

        # Create the faceted chart without specifying width in the properties
        chart = base.facet(
            column=alt.Column('Continent:N', header=alt.Header(
                title='Comparative Indicators Between Continents', labelOrient='bottom'))
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            grid=False
        ).configure_view(
            stroke=None
        ).configure(background='transparent')

        # Convert to HTML
        chart_html = chart.to_html()
        return (chart_html,)

    # change your points at here

    # @app.callback(
    #     [Output('notes', 'children')],
    #     [Input('column-dropdown-overview', 'value')]
    # )
    # def update_important_notes(column_name):
    #     if column_name == "Overweight":
    #         return (html.Div([
    #             html.H3('Points Worth Mentioning:', style={
    #                 'color': '#333', 'margin-bottom': '10px'}),
    #             html.Ul([
    #                 html.Li('Africa has the highest average rate of severe wasting, exceeding 2.5%.',
    #                     style={'margin-top': '10px'}),
    #                 html.Li('Europe has a significantly higher average rate of overweight children, surpassing 12%.',
    #                     style={'margin-top': '10px'}),
    #                 html.Li('Lack of data from Antarctica, due to less of population.',
    #                     style={'margin-top': '10px'})
    #             ], style={'list-style-type': 'none', 'padding-left': '0'})
    #         ]),)
    #     else:
    #         return (html.Div([
    #             html.H3('Points Worth Mentioning:', style={
    #                 'color': '#333', 'margin-bottom': '10px'}),
    #             html.Ul([
    #                 html.Li('America has the highest average rate of severe wasting, exceeding 2.5%.',
    #                     style={'margin-top': '10px'}),
    #                 html.Li('Europe has a significantly higher average rate of overweight children, surpassing 12%.',
    #                     style={'margin-top': '10px'}),
    #                 html.Li('Lack of data from Antarctica, due to less of population.',
    #                     style={'margin-top': '10px'})
    #             ], style={'list-style-type': 'none', 'padding-left': '0'}),
    #         ]),)
    return layout


# read country wise csv
df_avg = pd.read_csv("data/country-wise-average.csv")
df_avg["Continent"] = df_avg["Country"].apply(country_to_continent)
df_by_continent = df_avg.groupby("Continent").mean(numeric_only=True)
df_by_continent.drop("Income Classification", inplace=True, axis=1)

# read


growth_indicators_dict = {
    "Severe Wasting": "A measure of children who are much thinner than they should be for their height, indicating they're critically undernourished.",
    "Wasting": "A measure of children who weigh too little for their height, suggesting they have recently lost weight or are chronically underfed.",
    "Overweight": "A measure of children who weigh more than what is considered healthy for their height, which could lead to health problems.",
    "Stunting": "A measure of children who are shorter than they should be for their age, often because they haven't had enough nutrition over a long period.",
    "Underweight": "A measure of children who weigh less than what is considered healthy for their age, often due to inadequate nutrition."
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
    'fontSize': '18px',
    'color': '#9d7666'
}

cite_style = {
    'display': 'block',
    'textAlign': 'right',
    'marginTop': '10px'
}

introduction_text = "Global malnutrition and poverty are interconnected challenges affecting billions worldwide.   As of 2022, 2.5 billion adults were overweight, including 890 million with obesity, while 390 million were underweight.   Meanwhile, 149 million children under 5 were stunted, 45 million wasted, and 37 million overweight or obese.   Malnutrition's impacts stemming from undernutrition, micronutrient deficiencies, and overnutrition affect individuals' health, economic, and social well-being, particularly in low- and middle-income countries.   Concurrently, global poverty exacerbates malnutrition, with approximately 690 million people suffering from undernutrition.  Despite some progress in reducing hunger, achieving Zero Hunger by 2030 remains a formidable goal, necessitating comprehensive efforts to transform food systems, improve nutrition, and address the root causes of poverty and inequality."

# trend line
df_world = pd.read_csv("data/World_Malnutrition_Data.csv")
df_world.rename(columns={"TIME_PERIOD": "Year",
                "OBS_VALUE": "value"}, inplace=True)
df_world_mort = df_world[df_world["Indicator"]
                         == "Under-five mortality rate"]
df_world_stunting = df_world[df_world.Indicator ==
                             "Height-for-age <-2 SD (stunting)"]
df_world_underwt = df_world[df_world.Indicator ==
                            "Weight-for-age <-2 SD (Underweight)"]
df_world_mort.drop(["Indicator"], axis="columns", inplace=True)
cols = ["Total", "Male", "Female"]
alt.data_transformers.disable_max_rows()
chart = alt.Chart(df_world_mort, title="World Wide mortality Rate of Infants / 1000 births").mark_line().encode(
    alt.X('Year', title="Year"),
    alt.Y('mean(value)', title="Number of deaths / 1000 birth"),
    color='Sex:N',
    tooltip=['Year:O', 'mean(value):Q', 'Sex:N']
).properties(
    width='container',
    background='transparent'
).configure_view(
    strokeWidth=0,
    fill='transparent'
).transform_filter(
    alt.FieldOneOfPredicate(field='Sex', oneOf=cols)
)
chart_html_time_series = chart.to_html()


#  stunting trendline

stuning_chart = alt.Chart(df_world_stunting).mark_line().encode(
    x='Year:N',  # N for nominal scale
    # Q for quantitative scale
    y=alt.Y('mean(value):Q', axis=alt.Axis(title='Percent')),
    color='Sex:N',  # N for nominal scale
    tooltip=['Year:N', 'mean(value):Q', 'Sex:N']
).properties(
    title='World Wide Height-for-age <-2 SD (stunting)',
    width='container',
    background='transparent'
).configure_axis(
    labelAngle=-90  # Rotate the x-axis labels
)
stuning_chart_html = stuning_chart.to_html()
