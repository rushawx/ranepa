import datetime

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dash_table, dcc, html


df = pd.read_csv("vgsales.csv")

app = Dash(__name__)

app.layout = [
    html.Div(children="My First Dash App with Data"),
    html.Div(
        className="row",
        children=[
            html.Div(
                className="four columns",
                children=[
                    dcc.DatePickerRange(
                        min_date_allowed=datetime.date(
                            year=df["Year"].min().astype(int), month=1, day=1
                        ),
                        max_date_allowed=datetime.date(
                            year=df["Year"].max().astype(int), month=12, day=31
                        ),
                        start_date=datetime.date(
                            year=df["Year"].min().astype(int), month=1, day=1
                        ),
                        end_date=datetime.date(
                            year=df["Year"].max().astype(int), month=12, day=31
                        ),
                        display_format="YYYY",
                        id="year-selector",
                        style={"width": "100%"},
                    ),
                ],
            ),
            html.Div(
                className="four columns",
                children=[
                    dcc.Dropdown(
                        options=sorted(df["Platform"].unique()),
                        value="Wii",
                        id="platform-selector",
                        multi=True,
                        style={"width": "100%"},
                    ),
                ],
            ),
            html.Div(
                className="four columns",
                children=[
                    dcc.Dropdown(
                        options=sorted(df["Genre"].unique()),
                        value="Sports",
                        id="genre-selector",
                        multi=True,
                        style={"width": "100%"},
                    ),
                ],
            ),
        ],
    ),
    html.Div(
        className="row",
        children=[
            html.Div(
                className="six columns",
                children=[
                    dash_table.DataTable(
                        data=[],
                        page_size=10,
                        id="data-table",
                    ),
                ],
            ),
            html.Div(
                className="six columns",
                children=[
                    dcc.Graph(
                        figure={},
                        id="sales-graph",
                    ),
                ],
            ),
        ],
    ),
    html.Div(
        className="row",
        children=[
            html.Div(
                className="six columns",
                children=[
                    dcc.Graph(
                        figure={},
                        id="whiskers-graph",
                    )
                ],
            ),
        ],
    ),
]


@callback(
    Output(component_id="data-table", component_property="data"),
    Input(component_id="year-selector", component_property="start_date"),
    Input(component_id="year-selector", component_property="end_date"),
    Input(component_id="platform-selector", component_property="value"),
    Input(component_id="genre-selector", component_property="value"),
)
def update_table(start_date, end_date, selected_platforms, selected_genres):
    if isinstance(selected_genres, str):
        selected_genres = [selected_genres]
    if isinstance(selected_platforms, str):
        selected_platforms = [selected_platforms]
    start_date = pd.to_datetime(start_date).year
    end_date = pd.to_datetime(end_date).year
    df_filtered = df[
        (df["Year"] >= start_date)
        & (df["Year"] <= end_date)
        & (df["Platform"].isin(selected_platforms))
        & (df["Genre"].isin(selected_genres))
    ].reset_index(drop=True)
    df_filtered = df_filtered[["Year", "Platform", "Genre", "Name", "Global_Sales"]]
    return df_filtered.to_dict("records")


@callback(
    Output(component_id="sales-graph", component_property="figure"),
    Input(component_id="year-selector", component_property="start_date"),
    Input(component_id="year-selector", component_property="end_date"),
    Input(component_id="platform-selector", component_property="value"),
    Input(component_id="genre-selector", component_property="value"),
)
def update_graph(start_date, end_date, selected_platforms, selected_genres):
    if isinstance(selected_genres, str):
        selected_genres = [selected_genres]
    if isinstance(selected_platforms, str):
        selected_platforms = [selected_platforms]
    start_date = pd.to_datetime(start_date).year
    end_date = pd.to_datetime(end_date).year
    df_filtered = df[
        (df["Year"] >= start_date)
        & (df["Year"] <= end_date)
        & (df["Platform"].isin(selected_platforms))
        & (df["Genre"].isin(selected_genres))
    ].reset_index(drop=True)
    df_filtered = df_filtered[["Year", "Platform", "Genre", "Name", "Global_Sales"]]
    return px.histogram(df_filtered, x="Platform", y="Global_Sales", barmode="group")


@callback(
    Output(component_id="whiskers-graph", component_property="figure"),
    Input(component_id="year-selector", component_property="start_date"),
    Input(component_id="year-selector", component_property="end_date"),
    Input(component_id="platform-selector", component_property="value"),
    Input(component_id="genre-selector", component_property="value"),
)
def update_whiskers(start_date, end_date, selected_platforms, selected_genres):
    if isinstance(selected_genres, str):
        selected_genres = [selected_genres]
    if isinstance(selected_platforms, str):
        selected_platforms = [selected_platforms]
    start_date = pd.to_datetime(start_date).year
    end_date = pd.to_datetime(end_date).year
    df_filtered = df[
        (df["Year"] >= start_date)
        & (df["Year"] <= end_date)
        & (df["Platform"].isin(selected_platforms))
        & (df["Genre"].isin(selected_genres))
    ].reset_index(drop=True)
    df_filtered = df_filtered[["Year", "Platform", "Genre", "Name", "Global_Sales"]]
    return px.box(
        df_filtered, x="Platform", y="Global_Sales", hover_data=["Name", "Genre"]
    )


if __name__ == "__main__":
    app.run(debug=True)
