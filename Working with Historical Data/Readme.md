# 🗂️📊 Historical Flight Data Visualizations

# Developed By: [Birva Dave](https://www.linkedin.com/in/birva-dave/) — with love, logic, and a bit of turbulence ✈️

This folder contains standalone scripts to visualize and analyze **historical flight route data**. Each script is self-contained and focuses on a specific aspect of the dataset, making it easy to explore different angles without needing to combine scripts.

---

## 📁 Scripts and Their Purpose

### `historical_data_filtering_basedon_countries_and_airlines.py`
Filters routes based on both countries and airline names, showing only relevant flights.

### `historical_data_filtering_basedon_airlines.py`
Filters and displays flight routes based on selected airlines.

### `historical_data_dynamic_sample.py`
Plots a random sample of historical flight paths to avoid clutter and highlight route diversity.

### `historical_data_plotting_sample_flights.py`
Plots a few sample flights to quickly visualize how data is structured and displayed.

### `historical_data_top_countries.py`
Analyzes and displays the top countries based on the number of connected routes.

---

## 📂 Data Folders Used

### `Historical Data/`
Contains the cleaned and structured data files:
- `airlines.dat`
- `airport - airport.csv`
- `airline_network.csv`

These are the backbone of all the historical flight route visualizations.

### `World Map - Countries/`
Includes shape files used for plotting country borders on the map:
- `.shp`, `.shx`, `.dbf`, etc.

Make sure all these files are present to enable accurate geographical plotting.

---

## 🛠️ Dependencies

All scripts use the following libraries:

```bash
pip install pandas geopandas matplotlib seaborn plotly cartopy
```

---

✨ Dive in and get visualizing—every script is ready for takeoff!
