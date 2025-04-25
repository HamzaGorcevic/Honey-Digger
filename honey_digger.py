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
        self.data.to_csv("raw_data_ivanjica.csv",index=False)
        self.data = eng_data(self.data)
        self.data.to_csv('processed_weather.csv',index=False)
        return features_model(self.data,date,self.lat,self.lon)

if __name__ == "__main__":
    five_days_ago = (datetime.now() - timedelta(days=5)).date()
    #zabren Honey points for this place 0    0.20
    # lat,lon = 43.17434434405553, 20.12065665469868 
    #Ivanjica Honey points for this place 0    0.25
    lat,lon =43.578489837563446, 20.186082679577883
    hd = honey_digger(lat,lon,five_days_ago)
    print('Honey points for this place',hd.run_pipeline())
