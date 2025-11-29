import datetime
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px


df = pd.read_csv("vgsales.csv")

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = [
    html.Div(
        className="row",
        children=[
            "hello, ranepa!",
        ],
        style={"textAlign": "center", "fontSize": 40, "padding": 10},
    ),
    html.Div(
        className="row",
        children=[
            html.Div(
                className="six columns",
                children=[
                    dcc.Dropdown(
                        options=df["Platform"].unique(),
                        value="Wii",
                        id="platform-selector",
                        clearable=False,
                        style={"width": "50%"},
                    ),
                ],
            ),
            html.Div(
                className="six columns",
                children=[
                    dcc.DatePickerRange(
                        id="date-picker",
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
                        style={"width": "50%"},
                    )
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
                    dcc.Graph(figure={}, id="sales-graph"),
                ],
            ),
        ],
    ),
    html.Div(
        className="row",
        children=[
            dcc.Graph(
                figure={},
                id="whiskers-graph",
            )
        ],
    ),
]


@callback(
    Output(component_id="data-table", component_property="data"),
    [
        Input(component_id="platform-selector", component_property="value"),
        Input(component_id="date-picker", component_property="start_date"),
        Input(component_id="date-picker", component_property="end_date"),
    ],
)
def update_table(selected_platform, start_date, end_date):
    start_year = pd.to_datetime(start_date).year
    end_year = pd.to_datetime(end_date).year
    df_filtered = df[
        (df["Platform"] == selected_platform)
        & (df["Year"] >= start_year)
        & (df["Year"] <= end_year)
    ]
    df_filtered = df_filtered[["Name", "Year", "Genre", "Publisher", "Global_Sales"]]
    df_filtered = df_filtered.sort_values(by="Global_Sales", ascending=False)
    return df_filtered.to_dict("records")


@callback(
    Output(component_id="sales-graph", component_property="figure"),
    [
        Input(component_id="platform-selector", component_property="value"),
        Input(component_id="date-picker", component_property="start_date"),
        Input(component_id="date-picker", component_property="end_date"),
    ],
)
def update_graph(selected_platform, start_date, end_date):
    start_year = pd.to_datetime(start_date).year
    end_year = pd.to_datetime(end_date).year
    df_filtered = df[
        (df["Platform"] == selected_platform)
        & (df["Year"] >= start_year)
        & (df["Year"] <= end_year)
    ]
    fig = px.histogram(
        df_filtered,
        x="Year",
        y="Global_Sales",
        histfunc="sum",
        title=f"Total Global Sales by Year for {selected_platform}",
    )
    return fig


@callback(
    Output(component_id="whiskers-graph", component_property="figure"),
    [
        Input(component_id="platform-selector", component_property="value"),
        Input(component_id="date-picker", component_property="start_date"),
        Input(component_id="date-picker", component_property="end_date"),
    ],
)
def update_whiskers(selected_platform, start_date, end_date):
    start_year = pd.to_datetime(start_date).year
    end_year = pd.to_datetime(end_date).year
    df_filtered = df[
        (df["Platform"] == selected_platform)
        & (df["Year"] >= start_year)
        & (df["Year"] <= end_year)
    ]
    fig = px.box(
        df_filtered,
        x="Year",
        y="Global_Sales",
        color="Genre",
        title=f"Global Sales Distribution by Genre and Year for {selected_platform}",
        hover_data=["Name", "Publisher"],
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
