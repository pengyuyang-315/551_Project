from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.graph_objects as go
import pandas as pd
import altair as alt
import dash_bootstrap_components as dbc
#dbc row and dbc col in 

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
        colorbar=dict(title='Rate'),
        hoverinfo='location+z'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        title=dict(text='Average ' + column_name + ' Rate', x=0.5,y=0.9),
        geo=dict(
            showcoastlines=True,
            projection_type='equirectangular',
            showocean=True, oceancolor="LightBlue",
            showland=True, landcolor="White",
            showcountries=True, countrycolor="Gray"
        ),
        width=700,  
        height=600,
    )
    return fig
###

def create_altair_bar_plot(selected_country, selected_region):
    # Filter the DataFrame for the selected country and sub-national region
    filtered_df = MPI_sub[(MPI_sub['Country'] == selected_country) &
                          (MPI_sub['Sub-national region'] == selected_region)]

    # Prepare data in long format for Altair
    # We will use 'MPI Regional', 'Headcount Ratio Regional', and 'Intensity of deprivation Regional' columns for the bar plot
    long_df = filtered_df.melt(value_vars=[ 'Headcount Ratio Regional', 'Intensity of deprivation Regional'],
                               var_name='Indicator', value_name='Value')

    # Create the Altair horizontal bar chart
    chart = alt.Chart(long_df).mark_bar().encode(
        y=alt.Y('Indicator:N', title='Indicator', sort='-x'),  # Sorting bars by value
        x=alt.X('Value:Q', title='Value'),
        color=alt.Color('Indicator:N', scale=alt.Scale(scheme='dark2')),
        tooltip=['Indicator:N', 'Value:Q']
    ).properties(
        title=f'Poverty Metrics in {selected_region}, {selected_country}',
        width=374,  
        height=30
    
    )

    return chart
###

def create_country_bar_plot(selected_country):
    # Filter the DataFrame for the selected country
    filtered_df = MPI_nat[MPI_nat['Country'] == selected_country]

    # Prepare data in long format for Altair
    # We will use 'MPI Rural', 'Headcount Ratio Rural', and 'Intensity of Deprivation Rural' columns for the bar plot
    long_df = filtered_df.melt(value_vars=[ 'Headcount Ratio Rural', 'Intensity of Deprivation Rural'],
                               var_name='Indicator', value_name='Value')

    # Create the Altair horizontal bar chart
    chart = alt.Chart(long_df).mark_bar().encode(
        y=alt.Y('Indicator:N', title='Indicator', sort='-x'),  # Use sort to order bars by value
        x=alt.X('Value:Q', title='Value'),
        color=alt.Color('Indicator:N', scale=alt.Scale(scheme='dark2')),
        tooltip=['Indicator:N', 'Value:Q']
    ).properties(
        title=f'Rural Poverty Metrics in {selected_country}',
        width=400,  
        height=30
    )

    return chart
###

def create_layout(app):
    # Define the app layout
    layout = html.Div([
        html.H4("Poverty Data Visualization", style={
                'margin-left': '10px','font-family':' Georgia'}),
        html.H5("Choose a country you are interested in",  # Moved up
                style={'margin-top': '20px','font-family':' Georgia'}),
        dcc.Dropdown(
            id='country-dropdown-1',  # Moved up
            options=[{'label': country, 'value': country}
                     for country in countryNames],
            value="China",  # Default value
            multi=False,
            placeholder="Search and select countries...",
            style={'width': '50%','margin-left': '5px','fontSize': '13px'}
        ),
        html.H5("Choose a poverty indicator you are interested in, the world map will show you the distribution of that indicator all over the world!",  # Moved up
                style={'margin-top': '20px','font-family':' Georgia'}),
        
        dcc.Dropdown(
            id='columns-dropdown',
            options=[{'label': col, 'value': col}
                     for col in columns_1 if col != "ISO"],
            value='MPI Urban',  # Default value
            placeholder="Select indicator",
            
            style={'width': '50%','margin-left': '5px','fontSize': '13px'}
        ),
        
        html.Div([
            html.H6("Indicator explanation:",
                    style={'margin-bottom': '5px','font-family':'Georgia'}),
            html.Div(id='indicator_explain-1', style={
                'font-size': '13px', 'width': '40%','font-style':'italic'}),
        ]),
        html.Div(style={'border-bottom': '2px solid #ccc','margin-bottom':'5px'}),
        html.H5("Hover on the map! it will show you the comparision of key indicator between the country you are interested in and the hovered country",  # Moved up
                style={'margin-top': '20px','font-family':' Georgia'}),
        html.Div([  # This div wraps the world map and Altair chart horizontally
            dcc.Graph(
                id='world-map-1',
                
                style={'height':'100%','width': '60%'}
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
        html.Div(style={'border-bottom': '2px solid #ccc','margin-bottom':'5px'}),
        html.H5("Now lets explore the world poverty indicators with in the country that you are interested in!",  # Moved up
                style={'margin-top': '20px','font-family':' Georgia'}),
        html.Div([  # Continue with the rest of the layout unchanged

            

            dcc.Dropdown(
                id='city-dropdown',
                options=[],  # Initially empty
                multi=False,
                value="Central",  # Default value
                placeholder="Select a region...",
                style={'width': '50%','margin-left': '5px','fontSize': '13px'}
            ),
            html.H5(id='region-title',  # Moved up
                style={'margin-top': '20px','font-family':' Georgia'}),
            dash_table.DataTable(
                id='city-data-table',
                columns=[{"name": i, "id": i} for i in MPI_sub.columns if i not in ["ISO country code", "Country"]],
                data=[],  # Initialize with no data
                style_table={'width': '1000px', 'table-layout': 'fixed'},
        style_cell={
            'minWidth': '15%', 'width': '15%', 'maxWidth': '15%',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        }
            ),
            html.H5(id="region_title_1",  # Moved up
                style={'margin-top': '20px','font-family':' Georgia'}),
            dash_table.DataTable(
                id='country-data-table',
                # Initialize columns with MPI_nat columns
                columns=[{"name": i, "id": i} for i in MPI_nat.columns if i not in ["ISO", "Country"]],
                data=[],  # Initialize with no data
                # Add some margin for spacing
                style_table={'width': '1000px', 'table-layout': 'fixed'},
        style_cell={
            'minWidth': '15%', 'width': '15%', 'maxWidth': '15%',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        }
            ),
           

        dbc.Row([
    dbc.Col(html.Div([
        html.Iframe(
            id='altair-plot-iframe',
            style={'width': '100%', 'height': '100px', 'border': 'none'}
        ),
        html.Iframe(
            id='country-bar-plot-iframe',
            style={'width': '100%', 'height': '100px', 'border': 'none'}
        )
    ]), md=8),  # This column will take 8 parts of the grid system
    
    dbc.Col(html.Div([
        html.Iframe(
            id='DonutChart',
            style={'width': '100%', 'height': '500px', 'border': 'none'}
        )
    ]), md=4)  # This column will take 4 parts of the grid system, thus being on the right side
])
            
            
            
            ])
   
    
   
# Separate Div for the altair plot (above the others)

         
    ], style={'backgroundColor': '#FAF5F4'})

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
            filtered_df = filtered_df.drop(columns=["ISO", "Country"])
            
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
            color=alt.Color('Country:N', legend=None, scale=alt.Scale(scheme='dark2')),
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
            color=alt.Color('Country:N', legend=alt.Legend(title="Country"), scale=alt.Scale(scheme='dark2')),
            column=alt.Column('Indicator:N', title='Indicator'),
            tooltip=['Country', 'Indicator', 'Value']
        ).properties(
            width=150,
            height=300,
            title='MPI Rural'
            
        )

        return chart.to_html()
    
    @app.callback(
    Output('region-title', 'children'),
    [Input('city-dropdown', 'value'),
         Input('country-dropdown-1', 'value')]
    )
    def update_region_title(selected_city, selected_country):
        return f"{selected_city} regional data within {selected_country}"
    

    @app.callback(
    Output('region_title_1', 'children'),
    [Input('country-dropdown-1', 'value')]
)
    def update_region_title_1(selected_country):
        
        return f"National data within {selected_country}"
        
    
       
        ###donut chart
    @app.callback(
        Output('DonutChart', 'srcDoc'),
        [Input('city-dropdown', 'value'),
         Input('country-dropdown-1', 'value')]
    )
    

    def create_donut_data(selected_city, selected_country):
        # Initialization to handle cases where inputs may lead to an empty filtered_df
        filtered_df = pd.DataFrame()
        mpi_regional = None  # Default value for mpi_regional

        # Filter the MPI_sub DataFrame for the selected city and country
        if selected_city and selected_country:
            filtered_df = MPI_sub[(MPI_sub['Country'] == selected_country) &
                                (MPI_sub['Sub-national region'] == selected_city)]
        
        if not filtered_df.empty:
            mpi_regional = filtered_df['MPI Regional'].iloc[0]
        else:
            # If no data for city, consider handling differently or using a default value
            mpi_regional = 0  # Example: Setting mpi_regional to 0 or another default value

        # Proceed only if selected_country is provided and exists in MPI_nat
        if selected_country and not MPI_nat[MPI_nat['Country'] == selected_country].empty:
            mpi_urban = MPI_nat[MPI_nat['Country'] == selected_country]['MPI Urban'].iloc[0]
            mpi_rural = MPI_nat[MPI_nat['Country'] == selected_country]['MPI Rural'].iloc[0]
        else:
            # Handle cases with no valid country input or country not found
            return "No data available for the selected country."

        # Create a new DataFrame for the donut chart
        donut_data = pd.DataFrame({
            'Category': ['MPI Regional', 'MPI Urban', 'MPI Rural'],
            'Value': [mpi_regional, mpi_urban, mpi_rural]
        })

        chart = alt.Chart(donut_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color(field="Category", type="nominal"),
            tooltip=['Category', 'Value']
        ).properties(
            title="MPI Distribution",
            width=200,  # Adjusted width for visibility
            height=200  # Adjusted height for visibility
        )

        return chart.to_html()

        
        ###
        

    return layout

