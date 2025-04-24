import pandas as pd
from sklearn import preprocessing
import numpy as np
from sklearn.preprocessing import StandardScaler
def eng_data(data):

    # Cleaning the data and calculating additional columns
    data.dropna(inplace=True)
    data.sort_values(by=['date'])
    data['avg_temp'] = (data['temp_max'] + data['temp_min']) / 2
    data['avg_humidity'] = (data['humidity_max'] + data['humidity_min']) / 2
    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    
    # i did this to make months closer to each other if they are close in reallity, jan-dec
    data['month_sin'] =np.sin(2*np.pi * data['month'].astype(int)/12)
    data['month_cos'] = np.cos(2*np.pi*data['month'].astype(int)/12)
   

    # Calculate monthly averages for each feature
    data['month_precipitation'] = data.groupby(by=['year', 'month'])['precipitation'].transform('mean')
    data['month_temp'] = data.groupby(by=['year', 'month'])['avg_temp'].transform('mean')
    data['month_windy'] = data.groupby(by=['year', 'month'])['windspeed'].transform('mean')
    data['month_humidity'] = data.groupby(by=['year', 'month'])['avg_humidity'].transform('mean')
 # creating lagged features, basicly this adds as much previous values we want, on example, for july i want to have temp_lag1 for jun and temp_lag2 for may since we will need to predict future values
    features = ['month_precipitation','month_temp','month_windy','month_humidity','NDVI']
    # here we are shift for vales 1 and 2
    for feature in features:
        for lag in range(1,3):
            data[f"{feature}_lag{lag}"] = data[feature].shift(lag)
    
    columns_to_drop = ['temp_max', 'date', 'temp_min', 'humidity_max', 'humidity_min', 'windspeed', 'precipitation', 'avg_temp', 'avg_humidity']
    data.drop(columns=columns_to_drop, inplace=True)
    data.drop_duplicates(['year', 'month'], inplace=True)
    
    # we normalize data because most algorithm work better with it, after prediction we can inverse transofrmation
    scaler = StandardScaler()
    data_to_scale = [column for column in data.columns if 'lag' in column ]
    data[data_to_scale] = scaler.fit_transform(data[data_to_scale])
    data.dropna()
    return data,scaler


if __name__ == '__main__':
    data = pd.read_csv('processed_weather.csv')
    data.drop(columns=['date'], inplace=True)
    
    monthly_df = eng_data(data)
    
    monthly_df.to_csv('processed_weather_with_honey_points.csv', index=False)
    print(monthly_df.head())  
