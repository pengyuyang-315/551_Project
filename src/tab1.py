import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import altair as alt
import numpy as np

# Assuming your data file is located in the same directory as this script
df_avg = pd.read_csv("data/country-wise-average.csv")
columns_1 = df_avg.drop("Country", axis=1).columns

df_total = pd.read_excel("data/mul_sum.xlsx",sheet_name="Stunting Proportion (Model)")
countryNames = df_total["Country and areas"].unique().tolist()[:202]
columns_2 = ['Stunting','Overweight']
def create_world_map(column_name):
    
    fig = go.Figure()

    fig.add_trace(go.Choropleth(
        locations=df_avg["Country"],
        z=df_avg[column_name],
        locationmode='country names',
        colorscale=[[0, 'lightblue'], [1, 'darkblue']],  # Manually specify color range
        colorbar=dict(title=column_name + ' Rate'),
        hoverinfo='location+z'
    ))

    fig.update_layout(
        title=dict(text='Average ' + column_name + ' Rate(From 1997 to 2018)', x=0.5, y=0.9),
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
        html.Label([
            dcc.Dropdown(
                id='column-dropdown',
                options=[{'label': i, 'value': i} for i in columns_1],
                value='Overweight'  # Set 'Overweight' as the default option
            ),
            dcc.Graph(id='world-map'),
        ]),
        
        html.Div([
            html.Div([
                html.Iframe(
                    id='death_number',
                    style={'width': '100%', 'height': '400px'} 
                )
            ], style={'width': '43%', 'display': 'inline-block','float':'left'}),

            html.Div([
                html.Iframe(
                    id='Compare',
                    style={'width': '70%', 'height': '400px', 'float': 'left'}
                ),
                html.Div([
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': country, 'value': country} for country in countryNames],
                        value=["China"],
                        multi=True,
                        placeholder="Search and select countries...",
                    ),
                    dcc.RadioItems(
                        id='estimate-radio',
                        options=[{'label': i, 'value': i} for i in columns_2],
                        value='Overweight',  # Set 'Overweight' as the default option
                         # Add some top margin for separation
                    )
                ], style={'width': '20%', 'float': 'right'})
            ], style={'width': '55%', 'height':'380px','display': 'inline-block','float':'right'}),
        ]),
        
        
    ])

    @app.callback(
        Output('world-map', 'figure'),
        [Input('column-dropdown', 'value')]
    )
    def update_world_map(column_name):
        print("column_name")
        if column_name is None:  # If no option is chosen, default to 'Overweight'
            column_name = 'Overweight'
        return create_world_map(column_name)
    


    @app.callback(
        Output('Compare', 'srcDoc'),
        [Input('country-dropdown', 'value'),
        Input('estimate-radio','value')]
    )
    def displayCompare(countries, indicator):
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
            temp.columns = ['Point Estimate', 'Lower Uncertainty Bound', 'Upper Uncertainty Bound']
            temp['Year'] = temp.index
            temp.reset_index(drop=True, inplace=True)
            temp['Country'] = country
            
            # Concatenate current country data to the main dataframe
            df_tol = pd.concat([df_tol, temp], ignore_index=True)
        
        # Convert 'Year' column to datetime and numeric columns to appropriate data types
        df_tol['Year'] = pd.to_datetime(df_tol['Year'], format='%Y')
        df_tol['Point Estimate'] = pd.to_numeric(df_tol['Point Estimate'], errors='coerce')
        df_tol['Lower Uncertainty Bound'] = pd.to_numeric(df_tol['Lower Uncertainty Bound'], errors='coerce')
        df_tol['Upper Uncertainty Bound'] = pd.to_numeric(df_tol['Upper Uncertainty Bound'], errors='coerce')

        area = alt.Chart(df_tol).mark_area(opacity=0.5).encode(
            x=alt.X('Year', title='Year'),
            y=alt.Y('Upper Uncertainty Bound', title='Proportion'),
            y2='Lower Uncertainty Bound',
            color='Country',
            tooltip=['Year', 'Country', 'Point Estimate','Upper Uncertainty Bound','Lower Uncertainty Bound']
        )

        charts = area+alt.Chart(df_tol).mark_line().encode(
            x=alt.X('Year', title='Year'),
            y="Point Estimate",
            color='Country'
        )

        return charts.to_html()


    @app.callback(
        Output('death_number','srcDoc'),
        [Input('world-map', 'hoverData')]
    )
    def deathNumberDisplay(hoverData):
        country_names = pd.read_csv("data/death_infant.csv")["Country Name"].unique().tolist()
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
        df0 = df0[df0["Country Name"]==country].iloc[:, -63:].T
        df0.columns = ["Death Number"]
        df0["Range"] ="Infant"
        df0['Year'] = df0.index
        df0.reset_index(drop=True, inplace=True)
        df0['Country'] = country

        df1 = pd.read_csv("data/death_under_5.csv")
        df1 = df1[df1["Country Name"]==country].iloc[:, -63:].T
        df1.columns = ["Death Number"]
        df1["Range"] ="Under 5"
        df1['Year'] = df1.index
        df1.reset_index(drop=True, inplace=True)
        df1['Country'] = country

        df2 = pd.read_csv("data/death_5-9.csv")
        df2 = df2[df2["Country Name"]==country].iloc[:, -63:].T
        df2.columns = ["Death Number"]
        df2["Range"] ="5-9"
        df2['Year'] = df2.index
        df2.reset_index(drop=True, inplace=True)
        df2['Country'] = country

        df3 = pd.read_csv("data/death_10-14.csv")
        df3 = df3[df3["Country Name"]==country].iloc[:, -63:].T
        df3.columns = ["Death Number"]
        df3["Range"] ="10-14"
        df3['Year'] = df3.index
        df3.reset_index(drop=True, inplace=True)
        df3['Country'] = country

        df4 = pd.read_csv("data/death_15-19.csv")
        df4 = df4[df4["Country Name"]==country].iloc[:, -63:].T
        df4.columns = ["Death Number"]
        df4["Range"] ="16-19"
        df4['Year'] = df4.index
        df4.reset_index(drop=True, inplace=True)
        df4['Country'] = country

        sum = pd.concat([df0,df1,df2,df3,df4])
        sum['Year']=pd.to_datetime(sum['Year'], format='%Y') 
        sum_2000_2021 = sum.query("Year > 1999 and Year <2022")
        chart = alt.Chart(sum_2000_2021).mark_bar().encode(
            alt.X("Year"),
            alt.Y("Death Number"),
            color="Range",
            tooltip=["Year","Death Number","Range"]
        )  
        return chart.to_html()
    return layout

