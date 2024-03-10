import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import altair as alt
import numpy as np
import sys
import os
import dash_bootstrap_components as dbc
from datetime import datetime

# set root path as default
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# read data from country-wise-average.csv
df_avg = pd.read_csv("data/country-wise-average.csv")
# country names from df_avg
columns_1 = df_avg.drop("Country", axis=1).columns


df_total = pd.read_excel(
    "data/mul_sum.xlsx", sheet_name="Stunting Proportion (Model)")
countryNames = df_total["Country and areas"].unique().tolist()[:202]
columns_2 = ['Stunting', 'Overweight']

# indicators explanation
growth_indicators_dict = {
    "Income Classification": "The income classification of a country typically refers to the categorization of countries based on their gross national income (GNI) per capita. Common classifications include low-income, middle-income, and high-income countries, as defined by organizations like the World Bank.",
    "Severe Wasting": "Percentage of children aged 0–59 months who are below minus three standard deviations from median weight-for-height of the WHO Child Growth Standards.",
    "Wasting": "Moderate and severe: Percentage of children aged 0–59 months who are below minus two standard deviations from median weight-for-height of the WHO Child Growth Standards.",
    "Overweight": "Moderate and severe: Percentage of children aged 0-59 months who are above two standard deviations from median weight-for-height of the WHO Child Growth Standards.",
    "Stunting": "Moderate and severe: Percentage of children aged 0–59 months who are below minus two standard deviations from median height-for-age of the WHO Child Growth Standards.",
    "Underweight": "Moderate and severe: Percentage of children aged 0–59 months who are below minus two standard deviations from median weight-for-age of the World Health Organization (WHO) Child Growth Standards.",
    "U5 Population ('000s)": "Population of children under the age of 5, measured in thousands (000s)."
}

# create earth plot


def create_world_map(column_name):

    fig = go.Figure()

    fig.add_trace(go.Choropleth(
        locations=df_avg["Country"],
        z=df_avg[column_name],
        locationmode='country names',
        # Manually specify color range
        colorscale=[[0, 'rgb(255, 255, 204)'], [0.25, 'rgb(255, 237, 160)'], [0.5, 'rgb(254, 178, 76)'], [0.75, 'rgb(253, 141, 60)'], [1, 'rgb(227, 26, 28)']],
        # colorscale=[[0, 'lightblue'], [1, 'darkblue']],
        colorbar=dict(title=column_name + ' Rate'),
        hoverinfo='location+z'
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        title=dict(text='Average ' + column_name +
                   ' Rate(From 1997 to 2018)', x=0.5, y=0.9),
        geo=dict(
            showcoastlines=True,
            projection_type='equirectangular',
            showocean=True, oceancolor="LightBlue",
            showland=True, landcolor="White",
            showcountries=True, countrycolor="Gray"
        )
    )

    return fig

def create_layout(app):

    layout = html.Div([


        html.Div([
            html.H4("Feature Choose:", style={
                 'margin-left': '10px','font-family':' Georgia'}),
            # display indicator
            # get indicator selected
            html.Label([
                dcc.Dropdown(
                    id='column-dropdown',
                    options=[{'label': i, 'value': i} for i in columns_1],
                    value='Overweight',  # Set 'Overweight' as the default option
                    placeholder="Select indicator",
                    style={'width': '150%','margin-left': '5px','fontSize': '13px'}
                ),
            ]),
            html.Div([
                html.H6("Explanation:",
                        style={'margin-bottom': '5px','font-family':'Georgia'}),
                html.Div(id='indicator_explain', style={
                        'font-size': '13px', 'width': '40%','font-style':'italic'}),
            ], style={'margin-bottom': '20px','margin-left': '9px'}),  # Add margin between the H5 and the Div
        
        ]),
        html.Div(style={'border-bottom': '2px solid #ccc','margin-bottom':'5px'}),
        
        # display earth plot and death plot
        html.Div([
            dcc.Graph(
                id='world-map',
                style={'height':'100%','width': '60%'}
            ),

            # death number bar plot
            html.Div([
                html.Iframe(
                    id='death_number',
                    style={'height':'85%','width': '100%', 'background-color': 'transparent'}
                )
            ], style={'width': '40%'}),
        ], style={'display': 'flex','height':'10%'}),

        html.Div(style={'border-bottom': '2px solid #ccc','margin-bottom':'5px'}),
        # display two other plots for specific country
        dbc.Row([

            dbc.Col([
                html.Div([
                    html.H4("Temporal Distribution Model", style={'font-family':'Georgia'}),
                    html.P("Note: While WHO has not conducted annual data collection for every indicator, it has established corresponding estimation models for certain critical metrics. Consequently, it is able to present specific data for each year from 2000 to 2020.",style={"font-size":"13px","font-style":"italic"}),
                    html.H5("Countries to Compare", style={'font-family':'Georgia'}),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': country, 'value': country}
                                    for country in countryNames],
                        value=["China", "Benin","Haiti"],
                        multi=True,
                        placeholder="Search and select countries...",
                        style={'width': '80%','margin-left': '1px','fontSize': '13px','margin-bottom': '20px'}
                    ),
                    # html.P(style={'width':'15px'}),
                    html.Div([
                        html.Img(src='assets/ip.jpeg', height='100%', width='45%', style={'display': 'inline-block', 'vertical-align': 'middle'}),
                    ])
                ], style={'width': '100%'}),

            ]),
            dbc.Col([
                html.Iframe(
                    id='Compare',
                    style={'width': '100%', 'height': '400px'}
                ),
            ], width=8),
            
        ], style={'height': '400px','margin-left': '9px','margin-bottom':'5px'}),


        html.Div([
            html.Div([
                f" Copyright © {datetime.now().year}. Created by ",
                html.A(
                    "Yuyang Peng", href="https://github.com/pengyuyang-315/551_Project", target='_blank')
            ], style={'font-size': '9pt'})
        ], style={'width': '100%', 'margin-left': '4px'})

    ], style={'backgroundColor': '#FAF5F4'}
    )

    # earth plot for different indicators

    @app.callback(
        [Output('world-map', 'figure'),
         Output('indicator_explain', 'children')],
        [Input('column-dropdown', 'value')]
    )
    def update_world_map(column_name):
        print(column_name)
        if column_name is None:  # If no option is chosen, default to 'Overweight'
            column_name = 'Overweight'
        explain = growth_indicators_dict[column_name]

        # also return indicator explantion
        return create_world_map(column_name), explain

    # display one indicator different countries

    
    @app.callback(
    Output('Compare', 'srcDoc'),
    Input('country-dropdown', 'value')
)
    def displayCompare(countries):
        df_tol_1 = prepare_data("Stunting", countries)
        df_tol_2 = prepare_data("Overweight", countries)

        area_1 = create_chart(df_tol_1, "Stunting", countries)
        area_2 = create_chart(df_tol_2, "Overweight", countries)

        combined_chart = area_1 | area_2

        return combined_chart.to_html()

    def prepare_data(indicator, countries):
        sheetName = indicator + ' Proportion (Model)'
        df_tol = pd.DataFrame()

        # Iterate over each country
        for country in countries:
            # Read data from Excel file
            temp = pd.read_excel("data/mul_sum.xlsx", sheet_name=sheetName)

            # Filter data for the current country and select relevant columns
            temp = temp[(temp["Country and areas"] == country) &
                        (temp['Estimate'].isin(['Point Estimate', 'Lower Uncertainty Bound', 'Upper Uncertainty Bound']))].iloc[:, -23:].T

            # Rename columns and add 'Country' column
            temp.columns = ['Point Estimate',
                            'Lower Uncertainty Bound', 'Upper Uncertainty Bound']
            temp['Year'] = temp.index
            temp.reset_index(drop=True, inplace=True)
            temp['Country'] = country

            # Concatenate current country data to the main dataframe
            df_tol = pd.concat([df_tol, temp], ignore_index=True)

        # Convert 'Year' column to datetime and numeric columns to appropriate data types
        df_tol['Year'] = pd.to_datetime(df_tol['Year'], format='%Y')
        df_tol['Point Estimate'] = pd.to_numeric(
            df_tol['Point Estimate'], errors='coerce')
        df_tol['Lower Uncertainty Bound'] = pd.to_numeric(
            df_tol['Lower Uncertainty Bound'], errors='coerce')
        df_tol['Upper Uncertainty Bound'] = pd.to_numeric(
            df_tol['Upper Uncertainty Bound'], errors='coerce')
        df_tol['Point Estimate'] /= 100
        df_tol['Upper Uncertainty Bound'] /= 100
        df_tol['Lower Uncertainty Bound'] /= 100

        return df_tol

    def create_chart(df_tol, indicator, countries):
        # Construct the title
        title = f"{indicator} Model Estimates in {', '.join(countries)}"
        area = alt.Chart(df_tol).mark_area(opacity=0.5).encode(
            x=alt.X('Year', title='Year'),
            y=alt.Y('Upper Uncertainty Bound', title='Proportion',
                    axis=alt.Axis(format='%')),
            y2='Lower Uncertainty Bound',
            color='Country',
            tooltip=['Year', 'Country', alt.Tooltip('Point Estimate', format='.2%'), alt.Tooltip(
                'Upper Uncertainty Bound', format='.2%'), alt.Tooltip('Lower Uncertainty Bound', format='.2%')]
        ).properties(
            title =title
        )

        line = alt.Chart(df_tol).mark_line().encode(
            x=alt.X('Year', title='Year'),
            y="Point Estimate",
            color='Country'
        )

        

        return area + line


    @app.callback(
        Output('death_number', 'srcDoc'),
        [Input('world-map', 'hoverData')]
    )
    def deathNumberDisplay(hoverData):
        country_names = pd.read_csv(
            "data/death_infant.csv")["Country Name"].unique().tolist()
        if hoverData is None:
            country = "China"
        else:
            country = hoverData['points'][0]['location']
            country = ' '.join(word.capitalize() for word in country.split())
            print(country)
            if country not in country_names:
                print("No such")
                country = "China"
            print(country)
            
        df0 = pd.read_csv("data/death_infant.csv")
        df0 = df0[df0["Country Name"] == country].iloc[:, -63:].T
        df0.columns = ["Death Number"]
        df0["Range"] = "Infant"
        df0['Year'] = df0.index
        df0.reset_index(drop=True, inplace=True)
        df0['Country'] = country

        df1 = pd.read_csv("data/death_under_5.csv")
        df1 = df1[df1["Country Name"] == country].iloc[:, -63:].T
        df1.columns = ["Death Number"]
        df1["Range"] = "Under 5"
        df1['Year'] = df1.index
        df1.reset_index(drop=True, inplace=True)
        df1['Country'] = country

        df2 = pd.read_csv("data/death_5-9.csv")
        df2 = df2[df2["Country Name"] == country].iloc[:, -63:].T
        df2.columns = ["Death Number"]
        df2["Range"] = "5-9"
        df2['Year'] = df2.index
        df2.reset_index(drop=True, inplace=True)
        df2['Country'] = country

        df3 = pd.read_csv("data/death_10-14.csv")
        df3 = df3[df3["Country Name"] == country].iloc[:, -63:].T
        df3.columns = ["Death Number"]
        df3["Range"] = "10-14"
        df3['Year'] = df3.index
        df3.reset_index(drop=True, inplace=True)
        df3['Country'] = country

        df4 = pd.read_csv("data/death_15-19.csv")
        df4 = df4[df4["Country Name"] == country].iloc[:, -63:].T
        df4.columns = ["Death Number"]
        df4["Range"] = "16-19"
        df4['Year'] = df4.index
        df4.reset_index(drop=True, inplace=True)
        df4['Country'] = country

        sum = pd.concat([df0, df1, df2, df3, df4])
        sum['Year'] = pd.to_datetime(sum['Year'], format='%Y')
        sum_2000_2021 = sum.query("Year > 1999 and Year <2022")
        title = 'Death Number by Age in ' + country + ' from 2000 to 2021'
        subtitle = 'Source from the UN Inter-agency Group for Child Mortality Estimation'
        chart = alt.Chart(sum_2000_2021,
                          title=alt.TitleParams(
                              text=title,
                              subtitle=subtitle,
                              anchor='start',
                              subtitleFontSize=10)
                          ).mark_bar().encode(
            alt.X("Year",
                  scale=alt.Scale(domain=['2000', '2021'])
                  ),
            alt.Y("Death Number"),
            color=alt.Color("Range",
                            title="Age Range",
                            sort=["Infant", "Under 5", "5-9", "10-14", "16-19"]
                            ),
            tooltip=[
                # Custom tooltip for Year
                alt.Tooltip("Year", title="Survey Year"),
                # Custom tooltip for Death Number
                alt.Tooltip("Death Number", title="Death Number"),
                # Custom tooltip for Range
                alt.Tooltip("Range", title="Age Range")
            ]
        ).properties(
            width='container',
            background='transparent'
        ).configure_view(
            strokeWidth=0,
            fill='transparent'
        )
        

        chart_html = chart.to_html()

        return chart_html
    return layout
