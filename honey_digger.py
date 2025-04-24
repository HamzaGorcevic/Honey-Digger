import pandas as pd
from google_earth_engine import get_ndvi_data
from get_weather_data import fetch_data
from data_engineering import eng_data
from datetime import datetime,timedelta
from prediction_model import features_model

class honey_digger:
    

    def __init__(self,lat,lon,date) -> None:
        self.data = None
        self.lat = lat
        self.lon = lon
        self.date = date
    def run_pipeline(self):
        date = datetime.now().date()
        self.data = fetch_data(self.lat,self.lon,self.date)
        self.data = get_ndvi_data(self.lat,self.lon,self.data)
        self.data.to_csv("raw_data.csv",index=False)
        self.data,scaler = eng_data(self.data)
        self.data.to_csv('processed_weather.csv',index=False)
        return features_model(self.data,scaler,date)

if __name__ == "__main__":
    five_days_ago = (datetime.now() - timedelta(days=5)).date()
    # lat,lon = 43.14625558273692, 20.470546676707183 [76.99524246]
    lat,lon = 42.95587735274444, 20.751945787687802
    hd = honey_digger(lat,lon,five_days_ago)
    print('Honey points for this place',hd.run_pipeline())
