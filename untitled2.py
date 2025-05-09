# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oKCdqt4MLmpQkBjOTWhs2YZmANy8exnJ
"""

import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Generate 100 fake geospatial points
n = 100
soil_data = pd.DataFrame({
    "Latitude": np.random.uniform(22.0, 28.0, n),
    "Longitude": np.random.uniform(72.0, 78.0, n),
    "Region": np.random.choice(['North', 'South', 'East', 'West', 'Central'], n),
    "pH": np.round(np.random.uniform(4.5, 8.5, n), 2),
    "Nitrogen": np.random.randint(50, 500, n),  # in ppm
    "Phosphorus": np.random.randint(5, 50, n),  # in ppm
    "Potassium": np.random.randint(50, 400, n)  # in ppm
})

soil_data.head()

import seaborn as sns
import matplotlib.pyplot as plt

# Soil pH distribution
plt.figure(figsize=(8,5))
sns.histplot(soil_data['pH'], kde=True, color="green")
plt.title("Soil pH Distribution")
plt.xlabel("pH Level")
plt.show()

# Regional comparison of nutrients
plt.figure(figsize=(10,6))
sns.boxplot(data=soil_data, x='Region', y='Nitrogen')
plt.title("Nitrogen Levels by Region")
plt.show()

import folium
from folium.plugins import MarkerCluster

# Create map centered on synthetic area
m = folium.Map(location=[25, 75], zoom_start=5)
marker_cluster = MarkerCluster().add_to(m)

# Add soil points
for idx, row in soil_data.iterrows():
    popup_text = f"Region: {row['Region']}<br>pH: {row['pH']}<br>N: {row['Nitrogen']} ppm<br>P: {row['Phosphorus']} ppm<br>K: {row['Potassium']} ppm"
    folium.Marker(location=[row['Latitude'], row['Longitude']], popup=popup_text).add_to(marker_cluster)

m.save("synthetic_soil_map.html")
m

def soil_quality_index(row):
    # Simple weighted scoring: ideal pH ~ 6.5, nutrients moderate-high
    pH_score = max(0, 1 - abs(row['pH'] - 6.5)/2)
    n_score = min(row['Nitrogen']/300, 1)
    p_score = min(row['Phosphorus']/30, 1)
    k_score = min(row['Potassium']/250, 1)
    return round((pH_score + n_score + p_score + k_score) / 4 * 100, 2)

soil_data['QualityIndex'] = soil_data.apply(soil_quality_index, axis=1)

# Visualize by region
plt.figure(figsize=(10,6))
sns.boxplot(data=soil_data, x='Region', y='QualityIndex', palette='coolwarm')
plt.title("Soil Quality Index by Region")
plt.ylabel("Quality Index (0–100)")
plt.show()

import plotly.express as px

fig = px.scatter_geo(
    soil_data,
    lat='Latitude',
    lon='Longitude',
    color='QualityIndex',
    size='QualityIndex',
    hover_name='Region',
    projection='natural earth',
    color_continuous_scale='Viridis',
    title='Soil Quality Index Across Regions'
)
fig.show()

