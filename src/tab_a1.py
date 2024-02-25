import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import flask
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MPI_nat = pd.read_csv("data/MPI_national.csv")
columns_1 = MPI_nat.drop("Country", axis=1).columns

MPI_sub = pd.read__csv("data/MPI_subnational")
countryNames = MPI_sub["Country"].unique().tolist()
cityNames = MPI_sub["Sub-national"].unique().tolist()


