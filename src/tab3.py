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


def create_layout(app):
    layout = html.Div(

        html.Div([
            html.Div([
                html.H3(
                    "The situation seems to be improving, but... is it too soon to celebrate?")
            ], style={"text-align": "center", 'font-family': 'Georgia', 'color': 'rgba(255, 255, 255, 0.8)'}),
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
        }),)
    return layout
