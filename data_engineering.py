import pandas as pd
from sklearn import preprocessing

def eng_data(data):
    # avg temp
    def ndvi_points(ndvi):
        if ndvi < 0.2:
            return -5
        if  ndvi < 0.4:
            return 0
        if ndvi < 0.6:
            return 5
        if ndvi < 0.8:
            return 10
        return -5
    def temp_points(temp):
        if temp < 5:
            return -5  # Very cold
        if temp < 15:
            return 0   # Cool
        if temp < 25:
            return 5   # Mild
        if temp < 35:
            return 10  # Warm
        return 0  # Very hot, can be stressful for bees

    # For Humidity (percentage)
    def humidity_points(humidity):
        if humidity < 30:
            return -5  # Too dry
        if humidity < 50:
            return 0   # Low humidity
        if humidity < 70:
            return 5   # Moderate humidity
        if humidity < 90:
            return 10  # High humidity, good for bees
        return 0  # Too humid

    # For Precipitation (mm)
    def precipitation_points(precipitation):
        if precipitation < 0.5:
            return 10  # No rain, good conditions for bees to forage
        if precipitation < 2:
            return 0   # Light rain, may impact bee activity
        if precipitation < 5:
            return -5  # Moderate rain, bees stay in the hive
        return -10  # Heavy rain, bees can't fly
    def windy_points(wind_speed):
        if wind_speed < 5:
            return 10  # Calm, good for bees
        if wind_speed < 10:
            return 5   # Mild wind, bees can fly
        if wind_speed < 20:
            return 0   # Strong wind, bees less active
        return -5  # Very windy, bees won't fly     
    data.dropna(inplace=True)
    data.sort_values(by=['date'])
    data['avg_temp'] = (data['temp_max'] + data['temp_min'])/2
    data['avg_humidity'] = (data['humidity_max'] + data['humidity_min'])/2
    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year
    data['month'] =  data['date'].dt.month

    
    data['month_precipitation'] = data.groupby(by=['year','month'])['precipitation'].transform('mean')
    data['month_temp'] = data.groupby(by=['year','month'])['avg_temp'].transform('mean')
    data['month_windy'] = data.groupby(by=['year','month'])['windspeed'].transform('mean')
    data['month_humidity'] = data.groupby(by=['year','month'])['avg_humidity'].transform('mean')
    
    #normalization system
    data['month_precipitation'] = preprocessing.normalize(data[['month_precipitation']]).flatten()
    data['month_temp'] = preprocessing.normalize(data[['month_temp']]).flatten()
    data['month_windy'] = preprocessing.normalize(data[['month_windy']]).flatten()
    data['month_humidity'] = preprocessing.normalize(data[['month_humidity']]).flatten()
        
    # rating system 
    # data['NDVI_rate'] = data['NDVI'].map(lambda x:ndvi_points(x))
    # data['month_temp'] = data['month_temp'].map(lambda x:temp_points(x))
    # data['month_windy'] = data['month_windy'].map(lambda x:windy_points(x))
    # data['month_humidity'] = data['month_humidity'].map(lambda x:humidity_points(x))
    # data['month_precipitation'] = data['month_precipitation'].map(lambda x:precipitation_points(x))
    # honey points
    data['honey_points_month'] = (
        data['month_temp']  + 
        # data['NDVI_rate'] +
        data["NDVI"] +
        data['month_precipitation'] +
        data['month_humidity']  - 
        data['month_windy'] 
    )
    columns_to_drop = ['temp_max','date','NDVI', 'temp_min', 'humidity_max', 'humidity_min', 'windspeed', 'precipitation', 'avg_temp', 'avg_humidity']
    data.drop(columns=columns_to_drop, inplace=True)
    data.drop_duplicates(['year','month'],inplace=True)
    return data

if __name__ =='__main__':
    data = pd.read_csv('processed_weather.csv')
    data.drop(columns=['date'],inplace=True)
    #i could drop duplicate by any month counted value since they are same for each day
    monthly_df = data.drop_duplicates(['year','month'])
    monthly_df.to_csv("processed_weather.csv")
    print(monthly_df['NDVI'])

# next task should be to eng data a little bit more, need to think is it better to have only points for prediction or whole values but engineered more
