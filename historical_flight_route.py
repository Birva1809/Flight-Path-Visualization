import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import geopandas as gpd

# Change working directory to project root (Update this path as needed)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of this script

df_airport = pd.read_csv(os.path.join(BASE_DIR, "Historical Data", "airport - airport.csv"))
df_network = pd.read_csv(os.path.join(BASE_DIR, "Historical Data", "airline_network.csv"))


# Load the world map
world = gpd.read_file("World Map - Countries\World_Map_Countires.shp")  # Adjust path if needed


# Checking Dataset Info

# print("Head\n", df_airport.head())
# print("Info\n", df_airport.info())
# print("Describe\n", df_airport.describe())

# print("Head\n", df_network.head())
# print("Info\n", df_network.info())
# print("Describe\n", df_network.describe())


# Dropping Duplicates and checking for null and unique values

df_network.drop_duplicates(inplace=True)
# print(df_network.isnull().sum())
# print("Unique Airlines:", df_network["Airline"].nunique())
# print("Unique Equipment types:", df_network["Equipment"].nunique())


# Working with null values

df_network.dropna(subset=["Destination airport ID"], inplace=True)
df_network.drop(columns=["Codeshare"], inplace=True)
df_network["Equipment"].fillna("Unknown", inplace=True)

# print(df_network.isnull().sum())


# Merging the two dataframes
# Merged Twice, once for Source Airport, other for Destination Airport

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
# print(df_merged.head())
# print(df_merged.info())
# print(df_merged.isnull().sum())


# Dropping na from merged Dataset
df_cleaned = df_merged.dropna()
# print(df_cleaned.isnull().sum())


# Checking Cleaned Dataset
# print(df_cleaned.shape)
# print("Unique Source Countries:", df_cleaned["Country_source"].nunique())
# print("Unique Destination Countries:", df_cleaned["Country_destination"].nunique())
# print(df_cleaned.sample(5))


# Count number of flights per country
country_counts = df_cleaned["Country_source"].value_counts().head(20)  # Top 20

# Plot
plt.figure(figsize=(12, 6))
sns.barplot(x=country_counts.values, y=country_counts.index, palette="Blues_r")
plt.xlabel("Number of Flights")
plt.ylabel("Country")
plt.title("Top 20 Countries by Number of Flights")
plt.show()



# Plot the map
fig, ax = plt.subplots(figsize=(12, 6))
world.plot(ax=ax, color="lightgrey")

plt.title("World Map")
plt.show()
