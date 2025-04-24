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
import numpy as np
import math
def features_model(data:pd.DataFrame,scaler:StandardScaler,curr_date,months_arg=1):
    future_month = curr_date + relativedelta(month=+months_arg)
    data.dropna(inplace=True)
    train_data = data.iloc[:-10]
    test_data = data.iloc[-10:]
    data.drop(columns=['month'],inplace=True)
    features =[column for column in train_data.columns if 'lag' in column or 'month_sin' in column or 'month_cos' in column]
    targets = [column for column in data.columns if 'lag' not in column and 'year' not in column and 'month_sin' not in column and "month_cos" not in column]
    print("features",features)
    rf_predicted_values = pd.DataFrame(columns=targets)
    gb_predicted_values = pd.DataFrame(columns=targets)
    for target in targets:
        X_train = train_data[features]
        y_train = train_data[target]
        X_test = test_data[features]
        y_test = test_data[target]
        
        y_test = y_test.values.ravel()
        rf_model = RandomForestRegressor(n_estimators=50,random_state=42)
        rf_model.fit(X_train,y_train)
        predicted_data = rf_model.predict(X_test)
        rf_predicted_values[target] = predicted_data
        mse = mean_squared_error(y_test,predicted_data)
        
        gb_model = GradientBoostingRegressor(n_estimators=50,random_state=42)
        gb_model.fit(X_train,y_train)
        gb_predicted_data = gb_model.predict(X_test)
        gb_predicted_values[target] = gb_predicted_data

    # honey_test = calculate_honey_points(test_data[targets])
    # honey_prediction = calculate_honey_points(gb_predicted_values[targets])
    # plt.figure(figsize=(10,4))
    # plt.scatter(test_data['month'],honey_test,color='red',alpha=0.6)
    # plt.scatter(test_data['month'],honey_prediction,color='blue',alpha=0.6)
    # plt.xlabel='Months'
    # plt.ylabel='Honey Points'
    # plt.show()
    
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
    final_prediction = gb_model.predict(predict_new_month)
    return final_prediction
    
    
    
def calculate_honey_points(data):
    honey_points = (1 - data['month_precipitation'])*0.2 + 0.3*data['month_humidity'] + 0.3*data['NDVI']+0.2*(1-data['month_windy']+ 0.1*(1-data['month_temp']))
    return honey_points  

if __name__ =='__main__':
    date = datetime.now().date()
    data = pd.read_csv('processed_weather.csv')

# print(model(data).shape)

# So i have data aboud NDVI for each month, in time when user wants its result, i should predict ndvi for next month, based on current weather and ndvi data from previous year i have
# but also not only NDVI i should predict all other factors, and tell use if month will bring them honey
