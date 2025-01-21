import dash
import requests
from io import StringIO
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Constants
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
YEAR_LIST = [i for i in range(1980, 2024, 1)]


# Fetch data
def fetch_data(url):
    response = requests.get(url, verify=True)
    return pd.read_csv(StringIO(response.text))


data = fetch_data(URL)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"


def create_layout():
    return html.Div(
        [
            html.H1(
                "Automobile Sales Statistics Dashboard",
                style={"textAlign": "center", "color": "#503D36", "font-size": 24},
            ),
            html.Div(
                [
                    html.Label("Select Statistics:"),
                    dcc.Dropdown(
                        id="dropdown-statistics",
                        options=[
                            {
                                "label": "Yearly Statistics",
                                "value": "Yearly Statistics",
                            },
                            {
                                "label": "Recession Period Statistics",
                                "value": "Recession Period Statistics",
                            },
                        ],
                        value="Select Statistics",
                        placeholder="Select a report type",
                    ),
                ]
            ),
            html.Div(
                dcc.Dropdown(
                    id="select-year",
                    options=[{"label": i, "value": i} for i in YEAR_LIST],
                    value="Select-year",
                    placeholder="Select-year",
                )
            ),
            html.Div(
                [
                    html.Div(
                        id="output-container",
                        className="chart-grid",
                        style={"display": "flex"},
                    ),
                ]
            ),
        ]
    )

app.layout = create_layout()

# Callbacks
@app.callback(
    Output(component_id="select-year", component_property="disabled"),
    Input(component_id="dropdown-statistics", component_property="value"),
)
def update_input_container(selected_statistics):
    return selected_statistics != "Yearly Statistics"


@app.callback(
    Output(component_id="output-container", component_property="children"),
    [
        Input(component_id="dropdown-statistics", component_property="value"),
        Input(component_id="select-year", component_property="value"),
    ],
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == "Recession Period Statistics":
        # Filter the data for recession periods
        recession_data = data[data["Recession"] == 1]
        yearly_rec = (
            recession_data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        )
        r_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title="Average Automobile Sales fluctuation over Recession Period",
            )
        )
        average_sales = (
            recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        r_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average Automobile Sales by Vehicule Type",
            )
        )
        exp_rec = (
            recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        r_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total Expenditure share by vehicule type during recessions",
            )
        )

        unemp_data = (
            recession_data.groupby(
                ["unemployment_rate", "Vehicle_Type"], as_index=False
            )["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        r_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x="unemployment_rate",
                y="Automobile_Sales",
                labels={
                    "unemployment_rate": "Unemployment Rate",
                    "Automobile_Sales": "Average Automobile Sales",
                },
                title="Effect of Unemployment Rate on Vehicle Type and Sales",
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[html.Div(children=r_chart1), html.Div(children=r_chart2)],
                style={"display": "flex", "flex-wrap": "wrap"},
            ),
            html.Div(
                className="chart-item",
                children=[html.Div(children=r_chart3), html.Div(children=r_chart4)],
                style={"display": "flex", "flex-wrap": "wrap"},
            ),
        ]

    elif input_year and selected_statistics == "Yearly Statistics":
        yearly_data = data[data["Year"] == input_year]

        yas = data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        y_chart4 = dcc.Graph(
            figure=px.line(
                yas, x="Year", y="Automobile_Sales", title="Yearly Automobile Sales"
            )
        )

        mas = data.groupby("Month")["Automobile_Sales"].mean().reset_index()
        y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x="Month",
                y="Automobile_Sales",
                title="Total Monthly Automobile Sales",
            )
        )

        avr_vdata = yearly_data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Year",
                y="Automobile_Sales",
                title="Average Vehicles Sold by Vehicle Type in the year {}".format(
                    input_year
                ),
            )
        )

        exp_data = (
            yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total Advertisment Expenditure for Each Vehicle",
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[html.Div(children=y_chart4), html.Div(children=y_chart2)],
                style={"display": "flex", "flex-wrap": "wrap"},
            ),
            html.Div(
                className="chart-item",
                children=[html.Div(children=y_chart3), html.Div(children=y_chart4)],
                style={"display": "flex", "flex-wrap": "wrap"},
            ),
        ]

    else:
        return None


if __name__ == "__main__":
    app.run_server(debug=True)
