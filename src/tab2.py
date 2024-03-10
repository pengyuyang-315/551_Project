from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.graph_objects as go
import pandas as pd
import altair as alt

# Load your data
MPI_nat = pd.read_csv("data/MPI_national.csv")
MPI_sub = pd.read_csv("data/MPI_subnational.csv")

# Extract columns and unique country names for dropdown options
columns_1 = MPI_nat.drop("Country", axis=1).columns.tolist()
countryNames = MPI_sub["Country"].unique().tolist()

# MPI dict
MPI_national_dict = {
    "MPI Urban": "The Multidimensional Poverty Index for urban areas, quantifying the severity of poverty by considering multiple deprivation factors at the household level within urban settings.",
    "Headcount Ratio Urban": "The proportion of the population living in multidimensional poverty in urban areas. It represents the percentage of people whose household deprivation score is above a certain threshold, indicating they are multidimensionally poor.",
    "Intensity of Deprivation Urban": "The average proportion of deprivation suffered by people in multidimensional poverty in urban areas. It reflects the average share of indicators in which poor people are deprived among the total number of indicators considered in the MPI.",
    "MPI Rural": "The Multidimensional Poverty Index for rural areas, measuring the severity of poverty by accounting for various deprivation factors at the household level within rural settings.",
    "Headcount Ratio Rural": "The proportion of the population living in multidimensional poverty in rural areas. This metric indicates the percentage of individuals whose household deprivation score surpasses a predefined threshold, signifying they are multidimensionally poor.",
    "Intensity of Deprivation Rural": "The average proportion of deprivation experienced by people in multidimensional poverty in rural areas. This shows the average number of indicators in which poor individuals are deprived relative to the total indicators used in the MPI."
}

###
# Initialize the Dash app


def create_world_map_1(column_name):
    fig = go.Figure()
    fig.add_trace(go.Choropleth(
        locations=MPI_nat["Country"],
        z=MPI_nat[column_name],
        locationmode='country names',
        colorscale='Plasma',
        colorbar=dict(title=column_name + ' Rate'),
        hoverinfo='location+z'
    ))
    fig.update_layout(
        title=dict(text='Average ' + column_name + ' Rate', x=0.5),
        geo=dict(
            showcoastlines=True,
            projection_type='equirectangular',
            showocean=True, oceancolor="LightBlue",
            showland=True, landcolor="White",
            showcountries=True, countrycolor="Gray"
        ),
    )
    return fig
###


def create_altair_bar_plot(selected_country, selected_region):
    # Filter the DataFrame for the selected country and sub-national region
    filtered_df = MPI_sub[(MPI_sub['Country'] == selected_country) &
                          (MPI_sub['Sub-national region'] == selected_region)]

    # Prepare data in long format for Altair
    # We will use 'MPI Regional', 'Headcount Ratio Regional', and 'Intensity of deprivation Regional' columns for the bar plot
    long_df = filtered_df.melt(value_vars=['MPI Regional', 'Headcount Ratio Regional', 'Intensity of deprivation Regional'],
                               var_name='Indicator', value_name='Value')

    # Create the Altair bar chart
    chart = alt.Chart(long_df).mark_bar().encode(
        x=alt.X('Indicator:N', title='Indicator'),
        y=alt.Y('Value:Q', title='Value'),
        color='Indicator:N',
        tooltip=['Indicator:N', 'Value:Q']
    ).properties(
        title=f'Poverty Metrics in {selected_region}, {selected_country}'
    )

    return chart
###


def create_country_bar_plot(selected_country):
    # Filter the DataFrame for the selected country
    filtered_df = MPI_nat[MPI_nat['Country'] == selected_country]

    # Prepare data in long format for Altair
    # We will use 'MPI Rural', 'Headcount Ratio Rural', and 'Intensity of Deprivation Rural' columns for the bar plot
    long_df = filtered_df.melt(value_vars=['MPI Rural', 'Headcount Ratio Rural', 'Intensity of Deprivation Rural'],
                               var_name='Indicator', value_name='Value')

    # Create the Altair bar chart
    chart = alt.Chart(long_df).mark_bar().encode(
        x=alt.X('Indicator:N', title='Indicator'),
        y=alt.Y('Value:Q', title='Value'),
        color='Indicator:N',
        tooltip=['Indicator:N', 'Value:Q']
    ).properties(
        title=f'Rural Poverty Metrics in {selected_country}'
    )

    return chart
###


def create_layout(app):
    # Define the app layout
    layout = html.Div([
        html.H2("Poverty Data Visualization", style={
                'margin-top': '20%', 'margin-left': '10%'}),
        html.H4("Choose a country you are interested in",  # Moved up
                style={'margin-top': '20px'}),
        dcc.Dropdown(
            id='country-dropdown-1',  # Moved up
            options=[{'label': country, 'value': country}
                     for country in countryNames],
            value="China",  # Default value
            multi=False,
            placeholder="Search and select countries...",
        ),
        html.H4("Choose a poverty indicator you are interested in, the world map will show you the distribution of that indicator all over the world!",  # Moved up
                style={'margin-top': '20px'}),
        dcc.Dropdown(
            id='columns-dropdown',
            options=[{'label': col, 'value': col}
                     for col in columns_1 if col != "ISO"],
            value='MPI Urban',  # Default value
            placeholder="Select indicator",
            style={'width': '50%'}
        ),
        html.Div([
            html.H5("Indicator explanation:",
                    style={'margin-bottom': '5px'}),
            html.Div(id='indicator_explain-1', style={
                'font-size': 'small', 'width': '50%'}),
        ]),
        html.H3("Hover on the map! it will show you the comparision of key indicator between the country you are interested in and the hovered country",  # Moved up
                style={'margin-top': '20px'}),
        html.Div([  # This div wraps the world map and Altair chart horizontally
            dcc.Graph(
                id='world-map-1',
                # Adjusted width to 50%
                style={'width': '50%', 'height': '480px'}
            ),
            html.Iframe(
                id='altair-chart-container',
                style={'width': '50%', 'height': '480px', 'border': 'none'}
            ),
            html.Iframe(
                id='altair-chart-container-1',
                style={'width': '50%', 'height': '480px', 'border': 'none'}
            )
        ], style={'display': 'flex', 'justify-content': 'space-around'}),
        html.H3("Now lets explore the world poverty indicators with in the country that you are interested in!",  # Moved up
                style={'margin-top': '20px'}),
        html.Div([  # Continue with the rest of the layout unchanged
            dcc.Dropdown(
                id='city-dropdown',
                options=[],  # Initially empty
                multi=False,
                placeholder="Select a region...",
                style={'margin-top': '20px'}
            ),
            dash_table.DataTable(
                id='city-data-table',
                columns=[{"name": i, "id": i}
                         for i in MPI_sub.columns],  # Initialize columns
                data=[],  # Initialize with no data
            ),
            dash_table.DataTable(
                id='country-data-table',
                # Initialize columns with MPI_nat columns
                columns=[{"name": i, "id": i} for i in MPI_nat.columns],
                data=[],  # Initialize with no data
                # Add some margin for spacing
                style_table={'margin-top': '20px'}
            ),
            html.Div([
                html.Iframe(
                    id='altair-plot-iframe',
                    style={'width': '50%', 'height': '400px', 'border': 'none'}
                ),
                html.Iframe(
                    id='country-bar-plot-iframe',
                    style={'width': '50%', 'height': '400px', 'border': 'none'}
                ),
            ], style={'display': 'flex', 'justify-content': 'space-between'}),
        ], style={'width': '58%', 'float': 'left'}),
    ], style={'width': '100%', 'display': 'inline-block'})


    # Define callbacks to dynamically update content
    @app.callback(
        [Output('world-map-1', 'figure'),
         Output('indicator_explain-1', 'children')],
        [Input('columns-dropdown', 'value')]
    )
    def update_world_map1(column_name):
        if column_name is None:  # If no option is chosen, default to 'Overweight'
            column_name = 'MPI Rural'
        explain = MPI_national_dict[column_name]

        return create_world_map_1(column_name), explain

    @app.callback(
        Output('city-dropdown', 'options'),
        [Input('country-dropdown-1', 'value')]
    )
    def search_city(country):
        if country is not None:
            filtered_df = MPI_sub[MPI_sub['Country'] == country]
            cities = filtered_df['Sub-national region'].unique()
            return [{'label': city, 'value': city} for city in cities]
        return []

    @app.callback(
        Output('city-data-table', 'data'),
        [Input('city-dropdown', 'value'),
         Input('country-dropdown-1', 'value')]
    )
    def update_table(selected_city, selected_country):
        if selected_city and selected_country:
            filtered_df = MPI_sub[(MPI_sub['Country'] == selected_country) & (
                MPI_sub['Sub-national region'] == selected_city)]
            return filtered_df.to_dict('records')
        return []

    @app.callback(
        Output('country-data-table', 'data'),
        [Input('country-dropdown-1', 'value')]
    )
    def update_country_table(selected_country):
        if selected_country:
            # Filter for the selected country
            filtered_df = MPI_nat[MPI_nat['Country'] == selected_country]
            # Convert DataFrame to a list of dictionaries
            return filtered_df.to_dict('records')
        return []

    @app.callback(
        # Assuming an Iframe with this ID is in your layout
        Output('altair-plot-iframe', 'srcDoc'),
        [Input('country-dropdown-1', 'value'), Input('city-dropdown', 'value')]
    )
    def update_altair_plot(selected_country, selected_region):
        if selected_country and selected_region:
            chart = create_altair_bar_plot(selected_country, selected_region)
            return chart.to_html()
        return "Please select a country and a city."

    @app.callback(
        # Assuming an Iframe with this ID is in your layout
        Output('country-bar-plot-iframe', 'srcDoc'),
        [Input('country-dropdown-1', 'value')]
    )
    def update_country_bar_plot(selected_country):
        if selected_country:
            chart = create_country_bar_plot(selected_country)
            return chart.to_html()
        return "Please select a country."

    @app.callback(
        # Assume an html.Iframe to display the chart
        Output('altair-chart-container', 'srcDoc'),
        [Input('world-map-1', 'hoverData'),
         Input('country-dropdown-1', 'value')]
    )
    def update_chart(hoverData, dropdown_value):
        if hoverData is None or dropdown_value is None:
            return None  # Early exit if data is missing

        # Extract country names
        hover_country = hoverData['points'][0]['location']
        selected_country = dropdown_value

        # Filter data for the two countries
        chart_data = MPI_nat[MPI_nat['Country'].isin(
            [hover_country, selected_country])]

    # Then fold the specified columns into 'Indicator' and 'value' for Altair chart
        long_df = chart_data.melt(id_vars=["ISO", "Country"],
                                  value_vars=[
                                       "Headcount Ratio Rural", "Intensity of Deprivation Rural"],
                                  var_name="Indicator", value_name="Value")
        chart = alt.Chart(long_df).mark_bar().encode(
            x=alt.X('Country:N', title='Country'),
            y=alt.Y('Value:Q', title='Value'),
            color=alt.Color('Country:N', legend=alt.Legend(title="Country")),
            column=alt.Column('Indicator:N', title='Indicator'),
            tooltip=['Country', 'Indicator', 'Value']
        ).properties(
            width=150,
            height=300,
            title='Comparison of Key Poverty Variables Between Countries(hovered country and drop-down country)'
        )

        return chart.to_html()

    @app.callback(
        # Assume an html.Iframe to display the chart
        Output('altair-chart-container-1', 'srcDoc'),
        [Input('world-map-1', 'hoverData'),
         Input('country-dropdown-1', 'value')]
    )
    def update_chart_1(hoverData, dropdown_value):
        if hoverData is None or dropdown_value is None:
            return None  # Early exit if data is missing

        # Extract country names
        hover_country = hoverData['points'][0]['location']
        selected_country = dropdown_value

        # Filter data for the two countries
        chart_data = MPI_nat[MPI_nat['Country'].isin(
            [hover_country, selected_country])]

    # Then fold the specified columns into 'Indicator' and 'value' for Altair chart
        long_df = chart_data.melt(id_vars=["ISO", "Country"],
                                  value_vars=[
                                       "MPI Rural"],
                                  var_name="Indicator", value_name="Value")
        chart = alt.Chart(long_df).mark_bar().encode(
            x=alt.X('Country:N', title='Country'),
            y=alt.Y('Value:Q', title='Value'),
            color=alt.Color('Country:N', legend=alt.Legend(title="Country")),
            column=alt.Column('Indicator:N', title='Indicator'),
            tooltip=['Country', 'Indicator', 'Value']
        ).properties(
            width=150,
            height=300,
            title='Comparison of MPI Rural Between Countries(hovered country and drop-down country)'
        )

        return chart.to_html()
        

    return layout