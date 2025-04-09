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

# Making it dynamic
# Sample a subset of flights to keep the map clean
df_sample = df_cleaned.sample(300, random_state=42)  # adjust number as needed

fig = go.Figure()

# Generate random colors for each flight path
colors = np.random.choice([
    "blue", "purple", "orange", "teal", "magenta", "cyan", "limegreen", "gold", "pink"
], size=len(df_sample))

# Plot each flight path with different color
for idx, row in df_sample.iterrows():
    fig.add_trace(go.Scattergeo(
        lon=[row["Longitude_source"], row["Longitude_destination"]],
        lat=[row["Latitude_source"], row["Latitude_destination"]],
        mode='lines',
        line=dict(width=1, color=colors[idx % len(colors)]),
        hoverinfo='text',
        text=f'{row["City_source"]}, {row["Country_source"]} ➝ {row["City_destination"]}, {row["Country_destination"]}',
        showlegend=False
    ))

# Plot Source Airports (smaller dots, light color)
fig.add_trace(go.Scattergeo(
    lon=df_sample["Longitude_source"],
    lat=df_sample["Latitude_source"],
    mode='markers',
    marker=dict(size=3, color='green', opacity=0.5),
    name='Source Airports',
    hoverinfo='skip'
))

# Plot Destination Airports (smaller dots, light color)
fig.add_trace(go.Scattergeo(
    lon=df_sample["Longitude_destination"],
    lat=df_sample["Latitude_destination"],
    mode='markers',
    marker=dict(size=3, color='red', opacity=0.5),
    name='Destination Airports',
    hoverinfo='skip'
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
    title_text='Flight Paths (Sample View)',
    showlegend=True,
    height=650,
    margin={"r":0,"t":50,"l":0,"b":0},
    template="plotly_white"
)

fig.show()

