from dash import Dash, html, dash_table, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px


df = pd.read_csv("vgsales.csv")

app = Dash(__name__)

app.layout = [
    html.Div(children="Hello, Ranepa!"),
    dcc.Dropdown(
        options=df["Platform"].unique(),
        value="Wii",
        clearable=False,
        id="platform-selector",
    ),
    dcc.DatePickerRange(
        min_date_allowed=pd.to_datetime(df["Year"], format="%Y").min(),
        max_date_allowed=pd.to_datetime(df["Year"], format="%Y").max(),
        start_date=pd.to_datetime(df["Year"], format="%Y").min(),
        end_date=pd.to_datetime(df["Year"], format="%Y").max(),
        display_format="YYYY",
        id="date-picker",
    ),
    dash_table.DataTable(data=[], page_size=10, id="data-table"),
    dcc.Graph(figure={}, id="genre-sales-graph"),
]


@callback(
    Output(component_id="data-table", component_property="data"),
    Input(component_id="platform-selector", component_property="value"),
    Input(component_id="date-picker", component_property="start_date"),
    Input(component_id="date-picker", component_property="end_date"),
)
def update_data_table(selected_platform, start_date, end_date):
    start_date = pd.to_datetime(start_date).year
    end_date = pd.to_datetime(end_date).year
    df_filtered = df[
        (df["Platform"] == selected_platform)
        & (df["Year"] >= start_date)
        & (df["Year"] <= end_date)
    ].sort_values(by="Global_Sales", ascending=False)
    return df_filtered.to_dict("records")


@callback(
    Output(component_id="genre-sales-graph", component_property="figure"),
    Input(component_id="platform-selector", component_property="value"),
    Input(component_id="date-picker", component_property="start_date"),
    Input(component_id="date-picker", component_property="end_date"),
)
def update_genre_sales_graph(selected_platform, start_date, end_date):
    start_date = pd.to_datetime(start_date).year
    end_date = pd.to_datetime(end_date).year
    df_filtered = df[
        (df["Platform"] == selected_platform)
        & (df["Year"] >= start_date)
        & (df["Year"] <= end_date)
    ].sort_values(by="Global_Sales", ascending=False)
    fig = px.histogram(
        df_filtered,
        x="Genre",
        y="Global_Sales",
        title=f"Global Sales by Genre for {selected_platform}",
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
