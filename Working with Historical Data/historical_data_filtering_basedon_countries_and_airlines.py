import os
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Load and Prepare Data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Read CSVs
df_airport = pd.read_csv(os.path.join(BASE_DIR, "Historical Data", "airport - airport.csv"))
df_network = pd.read_csv(os.path.join(BASE_DIR, "Historical Data", "airline_network.csv"))

# Clean df_network
df_network.drop_duplicates(inplace=True)
df_network.dropna(subset=["Destination airport ID"], inplace=True)
df_network.drop(columns=["Codeshare"], inplace=True)
df_network["Equipment"].fillna("Unknown", inplace=True)

# Merge airport info for source and destination
df_merged = df_network.merge(df_airport, left_on="Source airport", right_on="IATA", how="left")
df_merged = df_merged.merge(df_airport, left_on="Destination airport", right_on="IATA", how="left", suffixes=("_source", "_destination"))
df_cleaned = df_merged.dropna()

# Load airlines.dat
airlines_path = os.path.join(BASE_DIR, "Historical Data", "airlines.dat")
columns = ["Airline_ID", "Name", "Alias", "IATA", "ICAO", "Callsign", "Country", "Active"]
df_airlines = pd.read_csv(airlines_path, header=None, names=columns, dtype=str)

# Clean airline data
df_airlines = df_airlines[df_airlines["Active"] == "Y"]
df_airlines = df_airlines[df_airlines["IATA"].notnull() & (df_airlines["IATA"] != "\\N")]
df_airlines = df_airlines[["IATA", "Name"]]

# Merge to get airline full name
df_cleaned = df_cleaned.merge(df_airlines, left_on="Airline", right_on="IATA", how="left")
df_cleaned.rename(columns={"Name": "Airline_FullName"}, inplace=True)

# Dropdown options
all_airlines = ["All Airlines"] + sorted(df_cleaned["Airline_FullName"].dropna().unique())
all_countries = ["All Countries"] + sorted(
    set(df_cleaned["Country_source"].dropna()).union(df_cleaned["Country_destination"].dropna())
)

# Generate Plotly traces
def generate_flight_traces(airline=None, country=None):
    filtered_df = df_cleaned.copy()

    if airline and airline != "All Airlines":
        filtered_df = filtered_df[filtered_df["Airline_FullName"] == airline]

    if country and country != "All Countries":
        filtered_df = filtered_df[
            (filtered_df["Country_source"] == country) |
            (filtered_df["Country_destination"] == country)
        ]

    if filtered_df.empty:
        return []

    # Sample only when both filters are 'All'
    if (airline and airline != "All Airlines") or (country and country != "All Countries"):
        sample_df = filtered_df
    else:
        sample_df = filtered_df.sample(min(300, len(filtered_df)), random_state=42)

    traces = []
    colors = np.random.choice([
        "blue", "purple", "orange", "teal", "magenta", "cyan", "gold", "pink"
    ], size=len(sample_df))

    for idx, row in sample_df.iterrows():
        traces.append(go.Scattergeo(
            lon=[row["Longitude_source"], row["Longitude_destination"]],
            lat=[row["Latitude_source"], row["Latitude_destination"]],
            mode='lines',
            line=dict(width=1, color=colors[idx % len(colors)]),
            hoverinfo='text',
            text=f'{row["City_source"]}, {row["Country_source"]} ➝ {row["City_destination"]}, {row["Country_destination"]} ({row["Airline_FullName"]})',
            showlegend=False
        ))

    # Source Airports (limegreen)
    traces.append(go.Scattergeo(
        lon=sample_df["Longitude_source"],
        lat=sample_df["Latitude_source"],
        mode='markers',
        marker=dict(size=4, color='limegreen', opacity=0.7),
        name='Source Airports',
        hoverinfo='skip'
    ))

    # Destination Airports (red)
    traces.append(go.Scattergeo(
        lon=sample_df["Longitude_destination"],
        lat=sample_df["Latitude_destination"],
        mode='markers',
        marker=dict(size=4, color='red', opacity=0.7),
        name='Destination Airports',
        hoverinfo='skip'
    ))

    return traces


# Create figure
def create_figure(airline=None, country=None):
    traces = generate_flight_traces(airline, country)
    fig = go.Figure(data=traces)

    fig.update_geos(
        projection_type="natural earth",
        showcountries=True,
        landcolor="lightgrey",
        showocean=True,
        oceancolor="lightblue"
    )

    fig.update_layout(
        title_text="Flight Paths by Airline and Country",
        showlegend=True,
        height=650,
        margin={"r":0,"t":50,"l":0,"b":0},
        template="plotly_white"
    )

    return fig

# Dash App
app = Dash(__name__)
app.title = "Flight Path Visualizer"

app.layout = html.Div([
    html.H1("Flight Path Visualizer", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Airline:"),
        dcc.Dropdown(
            id='airline-dropdown',
            options=[{"label": a, "value": a} for a in all_airlines],
            value="All Airlines"
        ),
    ], style={"width": "48%", "display": "inline-block"}),

    html.Div([
        html.Label("Select Country:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{"label": c, "value": c} for c in all_countries],
            value="All Countries"
        ),
    ], style={"width": "48%", "display": "inline-block", "marginLeft": "4%"}),

    dcc.Graph(id='flight-map', figure=create_figure())
])

@app.callback(
    Output('flight-map', 'figure'),
    Input('airline-dropdown', 'value'),
    Input('country-dropdown', 'value')
)
def update_figure(selected_airline, selected_country):
    return create_figure(selected_airline, selected_country)

if __name__ == '__main__':
    app.run(debug=True)
