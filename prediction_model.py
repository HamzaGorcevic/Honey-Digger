import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
from datetime import datetime,timedelta
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime
from dateutil.relativedelta import relativedelta
from land_type import get_land_type_nominatim
import numpy as np
def features_model(data:pd.DataFrame,curr_date,lat,lon,months_arg=1):
    future_month = curr_date + relativedelta(month=+months_arg)
    data.dropna(inplace=True)
    train_data = data.iloc[:-10]
    test_data = data.iloc[-10:]
    # data.drop(columns=['month'],inplace=True)
    
    features =[column for column in train_data.columns if 'lag' in column or 'month_sin' in column or 'month_cos' in column]
    targets = [column for column in data.columns if 'lag' not in column and 'year' not in column and 'month_sin' not in column and "month_cos" not in column]
    gb_predicted_values = pd.DataFrame(columns=targets)
    for target in targets:
        X_train = train_data[features]
        y_train = train_data[target]
        X_test = test_data[features]
        y_test = test_data[target]
        
        y_test = y_test.values.ravel()
        
        gb_model = GradientBoostingRegressor(n_estimators=50,random_state=42)
        gb_model.fit(X_train,y_train)
        gb_predicted_data = gb_model.predict(X_test)
        gb_predicted_values[target] = gb_predicted_data

    print(data[['year','month','month_temp']])
    plt.figure(figsize=(10,4))
    plt.scatter(test_data['month'],gb_predicted_values['month_temp'],color='red',alpha=0.6)
    plt.scatter(test_data['month'],test_data['month_temp'],color='blue',alpha=0.6)
    plt.xlabel='Months'
    plt.ylabel='Honey Points'
    plt.show()

    # future month preparation
    last_row = data.tail(1).copy()
    predict_new_month = pd.DataFrame({
        "month_sin": np.sin(2 * np.pi * future_month.month / 12),
        "month_cos": np.cos(2 * np.pi * future_month.month / 12),
        "month_precipitation_lag1": last_row['month_precipitation'].iloc[0],
        "month_precipitation_lag2": last_row['month_precipitation_lag1'].iloc[0],
        "month_temp_lag1": last_row['month_temp'].iloc[0],
        "month_temp_lag2": last_row['month_temp_lag1'].iloc[0],
        "month_windy_lag1": last_row['month_windy'].iloc[0],
        "month_windy_lag2": last_row['month_windy_lag1'].iloc[0],
        "month_humidity_lag1": last_row['month_humidity'].iloc[0],
        "month_humidity_lag2": last_row['month_humidity_lag1'].iloc[0],
        "NDVI_lag1": last_row['NDVI'].iloc[0],
        "NDVI_lag2": last_row['NDVI_lag1'].iloc[0]
    }, index=[0])
    future_predictions = {}
    for target in targets:
        gb_model = GradientBoostingRegressor(n_estimators=50, random_state=42)
        gb_model.fit(train_data[features], train_data[target])
        prediction = gb_model.predict(predict_new_month)[0]
        future_predictions[target] = prediction

    # Convert predictions to a DataFrame
    final_prediction_df = pd.DataFrame([future_predictions])

    return calculate_honey_points(final_prediction_df, lat, lon)
    
multiplier_map = {
    'forest': 0.9,
    'wood': 0.85,
    'meadow': 0.95,
    'grassland': 0.8,
    'farmland': 0.6,
    'residential': 0.3,
    'industrial': 0.1,
    'amenity': 0.4,
    'unknown': 0.5
}
    
def calculate_honey_points(data, lat, lon):
    """
    Calculate honey production points (0-100) based on environmental conditions and land type.
    
    Parameters:
    - data: DataFrame or dict with columns/keys: NDVI, month, month_precipitation,
      month_temp, month_windy, month_humidity
    - lat, lon: Latitude and longitude for land type determination
    
    Returns:
    - honey_points: Float (0-100), higher indicates better conditions for honey production
    """
    # Convert data to dict if it's a DataFrame
    if isinstance(data, pd.DataFrame):
        data = data.iloc[0].to_dict()
    
    # Extract variables
    ndvi = float(data['NDVI'])
    month = float(data['month'])
    precipitation = float(data['month_precipitation'])
    temp = float(data['month_temp'])
    wind_speed = float(data['month_windy']) / 3.6  # Convert km/h to m/s
    humidity = float(data['month_humidity'])
    
    # Calculate scores for each variable (0-1)
    
    # Temperature: Optimal 20-30°C
    if 20 <= temp <= 30:
        temp_score = 1.0
    elif 10 <= temp < 20:
        temp_score = (temp - 10) / 10
    elif 30 < temp <= 40:
        temp_score = (40 - temp) / 10
    else:
        temp_score = 0.0
    
    # Precipitation: Optimal <1 mm/day
    if precipitation <= 1:
        precip_score = 1.0
    elif 1 < precipitation <= 5:
        precip_score = (5 - precipitation) / 4
    else:
        precip_score = 0.0
    
    # Wind Speed: Optimal <2.5 m/s
    if wind_speed <= 2.5:
        wind_score = 1.0
    elif 2.5 < wind_speed <= 6.7:
        wind_score = (6.7 - wind_speed) / 4.2
    else:
        wind_score = 0.0
    
    # Humidity: Optimal 50-70%
    if 50 <= humidity <= 70:
        humidity_score = 1.0
    elif 30 <= humidity < 50:
        humidity_score = (humidity - 30) / 20
    elif 70 < humidity <= 90:
        humidity_score = (90 - humidity) / 20
    else:
        humidity_score = 0.0
    
    # NDVI: Optimal 0.3-0.8
    if 0.3 <= ndvi <= 0.8:
        ndvi_score = 1.0
    elif 0 <= ndvi < 0.3:
        ndvi_score = ndvi / 0.3
    elif 0.8 < ndvi <= 1:
        ndvi_score = (1 - ndvi) / 0.2
    else:
        ndvi_score = 0.0
    
    month_distance = abs(month - 5.5)  # Peak at mid-May
    month_score = max(0, 1 - month_distance / 5.5)  # Linear decay to 0 at month 1 and 12
    
    # Get land type and multiplier
    land_type = get_land_type_nominatim(lat, lon)
    land_multiplier = multiplier_map.get(land_type, 0.5)  # Default to 'unknown'
    
    # Calculate weighted honey points (0-100)
    honey_points = (
        temp_score * 0.3 +
        precip_score * 0.15 +
        wind_score * 0.15 +
        humidity_score * 0.10 +
        ndvi_score * 0.20 +
        month_score * 0.10
    ) * land_multiplier * 100
    
    return min(max(honey_points, 0), 100)  # Clamp to 0-100

if __name__ =='__main__':
    date = datetime.now().date()
    data = pd.read_csv('processed_weather.csv')

# print(model(data).shape)

# So i have data aboud NDVI for each month, in time when user wants its result, i should predict ndvi for next month, based on current weather and ndvi data from previous year i have
# but also not only NDVI i should predict all other factors, and tell use if month will bring them honey
