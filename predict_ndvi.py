import pandas as pd
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from datetime import datetime,timedelta
def model(data:pd.DataFrame,curr_date,months=1):
    data_to_predict = curr_date + timedelta(months=months)
    X = data.drop('NDVI')
    y = data['NDVI']
    X_train,X_test,y_train,y_yest =  train_test_split(X,y,test_size=0.2,random_state=42)
    
    
    

date = datetime.now().date()
data = pd.read_csv('processed_weather.csv')
print(data.tail(5))

# print(model(data).shape)

# So i have data aboud NDVI for each month, in time when user wants its result, i should predict ndvi for next month, based on current weather and ndvi data from previous year i have
# but also not only NDVI i should predict all other factors, and tell use if month will bring them honey
