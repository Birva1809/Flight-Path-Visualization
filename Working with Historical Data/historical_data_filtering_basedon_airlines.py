import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import plotly.graph_objects as go
import os

# Change working directory to project root (Update this path as needed)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of this script

df_airport = pd.read_csv(os.path.join(BASE_DIR, "Historical Data", "airport - airport.csv"))
df_network = pd.read_csv(os.path.join(BASE_DIR, "Historical Data", "airline_network.csv"))


# Load the world map
world = gpd.read_file("World Map - Countries\World_Map_Countires.shp")  # Adjust path if needed

# Dropping Duplicates and checking for null and unique values

df_network.drop_duplicates(inplace=True)

# Working with null values

df_network.dropna(subset=["Destination airport ID"], inplace=True)
df_network.drop(columns=["Codeshare"], inplace=True)
df_network["Equipment"].fillna("Unknown", inplace=True)

df_merged = df_network.merge(
    df_airport, left_on="Source airport", right_on="IATA", how="left"
)
df_merged = df_merged.merge(
    df_airport,
    left_on="Destination airport",
    right_on="IATA",
    how="left",
    suffixes=("_source", "_destination"),
)

# Dropping na from merged Dataset
df_cleaned = df_merged.dropna()


# Dropdown and filtering based on airlines
# Sampled top airlines
top_airlines = df_cleaned["Airline"].value_counts().head(10).index.tolist()
fig = go.Figure()
dropdown_buttons = []
colors_pool = ["blue", "purple", "orange", "teal", "magenta", "cyan", "limegreen", "gold", "pink", "coral", "darkred", "olive"]

# How many routes per airline
sample_size = 150
total_traces = 0

for i, airline in enumerate(top_airlines):
    df_airline = df_cleaned[df_cleaned["Airline"] == airline].sample(sample_size, random_state=42+i)

    airline_traces = []

    # Add flight paths
    for _, row in df_airline.iterrows():
        color = np.random.choice(colors_pool)
        airline_traces.append(go.Scattergeo(
            lon=[row["Longitude_source"], row["Longitude_destination"]],
            lat=[row["Latitude_source"], row["Latitude_destination"]],
            mode='lines',
            line=dict(width=1.2, color=color),
            hoverinfo='text',
            text=f'{row["City_source"]}, {row["Country_source"]} ➝ {row["City_destination"]}, {row["Country_destination"]}',
            name=f'{airline} Route',
            showlegend=False,
            visible=(i == 0)
        ))

    # Source Airports (Random colored dots)
    source_color = np.random.choice(colors_pool)
    airline_traces.append(go.Scattergeo(
        lon=df_airline["Longitude_source"],
        lat=df_airline["Latitude_source"],
        mode='markers',
        marker=dict(size=4, color=source_color, opacity=0.6),
        name=f"{airline} Source",
        hoverinfo='skip',
        visible=(i == 0)
    ))

    # Destination Airports (Random colored dots)
    dest_color = np.random.choice(colors_pool)
    airline_traces.append(go.Scattergeo(
        lon=df_airline["Longitude_destination"],
        lat=df_airline["Latitude_destination"],
        mode='markers',
        marker=dict(size=4, color=dest_color, opacity=0.6),
        name=f"{airline} Destination",
        hoverinfo='skip',
        visible=(i == 0)
    ))

    for trace in airline_traces:
        fig.add_trace(trace)

    # Button for dropdown
    visibility_array = [False] * total_traces + [True] * len(airline_traces)
    visibility_array += [False] * (3 * len(top_airlines) - len(visibility_array))  # padding if any
    dropdown_buttons.append(dict(
        args=[{"visible": visibility_array}],
        label=airline,
        method="update"
    ))

    total_traces += len(airline_traces)

# "Show All" button (CAREFUL: this can still be heavy!)
dropdown_buttons.append(dict(
    args=[{"visible": [True] * total_traces}],
    label="Show All",
    method="update"
))

# Map layout
fig.update_geos(
    projection_type="natural earth",
    showcountries=True,
    landcolor="lightgrey",
    showocean=True,
    oceancolor="lightblue"
)

fig.update_layout(
    title_text='Flight Paths by Airline (Colorful + Interactive)',
    showlegend=True,
    height=650,
    margin={"r":0,"t":50,"l":0,"b":0},
    template="plotly_white",
    updatemenus=[dict(
        active=0,
        buttons=dropdown_buttons,
        x=0.1,
        xanchor="left",
        y=1.1,
        yanchor="top"
    )]
)

fig.show()

