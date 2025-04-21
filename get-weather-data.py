import requests
import pandas as pd

def fetch_data(lat,lon,start_year=2023,end_year=2025):
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_year}-01-01&end_date={end_year}-01-01&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,relative_humidity_2m_max,relative_humidity_2m_min&timezone=auto"
    data = requests.get(url)    
    data = data.json()
    df= pd.DataFrame(data['daily'])
    df['latitude'] = lat
    df['longitude'] = lon
    df['date'] = pd.to_datetime(df['time'])
    df.drop(columns=['time'],inplace=True)
    df.columns = ["temp_max", "temp_min", "precipitation", "windspeed", "latitude", "longitude",'humidity_max',"humidity_min" ,"date"]
    df.to_csv('weather.csv',index=False)
    print(df)
    
latitude = 44.7866
longitude = 20.4489

fetch_data(latitude, longitude)