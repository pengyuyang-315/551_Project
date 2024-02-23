import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd

app = dash.Dash(__name__)
df_total = pd.read_excel("data/mul_sum.xlsx",sheet_name="Stunting Proportion (Model)")
countryNames = df_total["Country and areas"].unique().tolist()[:202]
columns = ['Stuning','Overweight']

app.layout = html.Div([
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in countryNames],
        value =["China"],
        multi=True,
        placeholder="Search and select countries...",
        style={'width': '50%'}
    ),
    dcc.Dropdown(
        id='estimate-dropdown',
        options=[{'label': i, 'value': i} for i in columns],
        value='Overweight'  # Set 'Overweight' as the default option
    ),
    html.Iframe(
        id = 'Compare'
    )
])

@app.callback(
    Output('Compare', 'srcDoc'),
    [Input('country-dropdown', 'value'),
     Input('estimate-dropdown','value')]
)
def displayCompare(countries, indicator):
    sheetName = indicator+' Proportion (Model)'
    df_tol =pd.DataFrame()
    for country in countries:
        temp = pd.read_excel("data/mul_sum.xlsx",sheet_name=sheetName)
        temp = temp[(temp["Country and areas"] == country) & (temp['Estimate'] == 'Point Estimate')].iloc[:, -23:].T
        temp.columns = ['Estimate']
        temp['Year'] = temp.index
        temp.reset_index(drop=True, inplace=True)
        temp['Country'] = country
        df_tol = pd.concat([df_tol, temp], ignore_index=True)
    df_tol['Year'] = pd.to_datetime(df_tol['Year'], format='%Y')
    df_tol['Estimate'] = pd.to_numeric(df_tol['Estimate'], errors='coerce')
    charts = alt.Chart(df_tol).mark_line().encode(
        x = "Year",
        y = "Estimate",
        color = "Country"

    )
    return charts.to_html()
    
        

if __name__ == '__main__':
    app.run_server(debug=True,port=8030)
