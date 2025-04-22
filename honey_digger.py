import pandas as pd
from google_earth_engine import get_ndvi_data
from get_weather_data import fetch_data
from data_engineering import eng_data
from datetime import datetime,timedelta

class honey_digger:
    

    def __init__(self,lat,lon,date) -> None:
        self.data = None
        self.lat = lat
        self.lon = lon
        self.date = date
    def run_pipeline(self):
        self.data = fetch_data(self.lat,self.lon,self.date)
        self.data = get_ndvi_data(self.lat,self.lon,self.data)
        self.data = eng_data(self.data)
        self.data.to_csv('processed_weather.csv',index=False)

if __name__ == "__main__":
    five_days_ago = (datetime.now() - timedelta(days=5)).date()
    lat = 43.1059
    lon=20.6389
    hd = honey_digger(lat,lon,five_days_ago)
    hd.run_pipeline()
