import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

df = pd.read_csv("source/bi/viz/vgsales.csv")

app = Dash()

app.layout = [
    html.H1(children="My VGS Dashboard"),
    html.Hr(),
    dcc.DatePickerRange(
        min_date_allowed=pd.to_datetime(
            df["Year"].dropna().astype(int).min(), format="%Y"
        ),
        max_date_allowed=pd.to_datetime(
            df["Year"].dropna().astype(int).max(), format="%Y"
        ),
        start_date=pd.to_datetime(df["Year"].dropna().astype(int).min(), format="%Y"),
        end_date=pd.to_datetime(df["Year"].dropna().astype(int).max(), format="%Y"),
        display_format="YYYY",
        id="year-selector",
    ),
    dcc.Dropdown(
        options=df["Platform"].unique(),
        value=df["Platform"].value_counts(ascending=False).index[0],
        id="platform-dropdown",
        placeholder="Select Platform",
        multi=True,
    ),
    dag.AgGrid(
        columnDefs=[{"field": col} for col in df.columns],
        id="data-table",
    ),
    dcc.Graph(id="boxplot-graph"),
]


@callback(
    Output(component_id="data-table", component_property="rowData"),
    Input(component_id="platform-dropdown", component_property="value"),
    Input(component_id="year-selector", component_property="start_date"),
    Input(component_id="year-selector", component_property="end_date"),
)
def update_table(selected_platform, start_date, end_date):
    if isinstance(selected_platform, str):
        selected_platform = [selected_platform]
    filtered_df = df[
        (df["Platform"].isin(selected_platform))
        & (df["Year"] >= pd.to_datetime(start_date).year)
        & (df["Year"] <= pd.to_datetime(end_date).year)
    ]
    return filtered_df.to_dict("records")


@callback(
    Output(component_id="boxplot-graph", component_property="figure"),
    Input(component_id="platform-dropdown", component_property="value"),
    Input(component_id="year-selector", component_property="start_date"),
    Input(component_id="year-selector", component_property="end_date"),
)
def update_boxplot(selected_platform, start_date, end_date):
    if isinstance(selected_platform, str):
        selected_platform = [selected_platform]
    filtered_df = df[
        (df["Platform"].isin(selected_platform))
        & (df["Year"] >= pd.to_datetime(start_date).year)
        & (df["Year"] <= pd.to_datetime(end_date).year)
    ]
    figure = px.box(
        filtered_df,
        y="Global_Sales",
        color="Genre",
        hover_data=["Name"],
    )
    return figure


if __name__ == "__main__":
    app.run(debug=True)
