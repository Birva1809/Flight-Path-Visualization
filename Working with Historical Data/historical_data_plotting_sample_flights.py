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

# Single sample flight
# sample_route = df_cleaned.sample(1).iloc[0]

# source_coords = (sample_route["Longitude_source"], sample_route["Latitude_source"])
# dest_coords = (sample_route["Longitude_destination"], sample_route["Latitude_destination"])


# Plotting multiple flight paths - Top 500
fig, ax = plt.subplots(figsize=(18, 10))
world.plot(ax=ax, color="lightgrey", edgecolor="white")

# Plot top N routes (e.g., 500)
for _, row in df_cleaned.sample(500).iterrows():
    source = (row["Longitude_source"], row["Latitude_source"])
    dest = (row["Longitude_destination"], row["Latitude_destination"])
    
    plt.plot(
        [source[0], dest[0]],
        [source[1], dest[1]],
        color="blue", alpha=0.1  # Faint lines for better visibility
    )

plt.title("Sample of 500 Global Flight Paths")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)
plt.show()