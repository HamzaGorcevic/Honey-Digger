import pandas as pd
from google_earth_engine import get_ndvi_data
from get_weather_data import fetch_data
from data_engineering import eng_data
from datetime import datetime, timedelta
from prediction_model import features_model
import streamlit as st
import folium
from streamlit.components.v1 import html

class honey_digger:
    def __init__(self, lat, lon, date,start_year=2019) -> None:
        self.data = None
        self.lat = lat
        self.lon = lon
        self.date = date
        self.start_year= start_year

    def run_pipeline(self):
        date = datetime.now().date()
        self.data = fetch_data(self.lat, self.lon, self.start_year,self.date)
        self.data = get_ndvi_data(self.lat, self.lon, self.data)
        self.data.to_csv("raw_data.csv", index=False)
        self.data = eng_data(self.data)
        self.data.to_csv('processed_weather.csv', index=False)
        return features_model(self.data, date, self.lat, self.lon)

# Streamlit UI
st.set_page_config(page_title="Honey Potential Prediction")

st.title("🍯 Honey Potential Prediction")

st.markdown("### Select a location on the map or enter coordinates manually.")

# Folium map creation
default_location = [43.5, 20.2]
m = folium.Map(location=default_location, zoom_start=8)
m.add_child(folium.LatLngPopup())

# Save map to HTML file
map_file = "map.html"
m.save(map_file)

# Load map HTML
with open(map_file, 'r') as f:
    map_html = f.read()

html(map_html, height=400, width=750)

st.markdown("### Enter coordinates manually (no click support in iframe):")

lat = st.number_input("Latitude", value=43.578, format="%.6f")
lon = st.number_input("Longitude", value=20.186, format="%.6f")

five_days_ago = (datetime.now() - timedelta(days=5)).date()

if st.button("🔍 Predict Honey Potential"):
    st.write(f"Running pipeline for: **Lat:** {lat}, **Lon:** {lon}")
    hd = honey_digger(lat, lon, five_days_ago)
    result = hd.run_pipeline()
    st.success(f"🍯 Honey potential score: `{result}`")
