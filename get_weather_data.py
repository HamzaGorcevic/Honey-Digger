import requests
import pandas as pd

def fetch_data(lat,lon,end_date):
    start_year = 2019
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_year}-01-01&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,relative_humidity_2m_max,relative_humidity_2m_min&timezone=auto"
    data = requests.get(url)    
    data = data.json()
    df= pd.DataFrame(data['daily'])
    # df['latitude'] = lat
    # df['longitude'] = lon
    df['date'] = pd.to_datetime(df['time'])
    df.drop(columns=['time'],inplace=True)
    df.columns = ["temp_max", "temp_min", "precipitation", "windspeed",'humidity_max',"humidity_min" ,"date"]
    return df
    
    

