import pandas as pd

data = pd.read_csv("weather.csv")
data.dropna(inplace=True)
def eng_data():
    # avg temp
    print(data.info())
    data.sort_values(by=['date'])
    data['avg_temp'] = (data['temp_max'] + data['temp_min'])/2
    data['avg_humidity'] = (data['humidity_max'] + data['humidity_min'])/2
    data['rainy'] = data['precipitation'] > 0.5
    data['windy'] = data['windspeed'] > 10
    data['week_temp'] = data['avg_temp'].rolling(window=7).mean()
    data['week_windy'] = data['windy'].rolling(window=7).sum()
    data['week_humidity'] = data['avg_humidity'].rolling(window=7).mean()
    data.dropna(inplace=True)
    
    # honey points
    data['honey_points_week'] = (
        data['week_temp'] * 0.4 + 
        data['week_humidity'] * 0.4 - 
        data['week_windy'] * 0.2
    )
    print(data['honey_points_week'][100:130])
    
eng_data()