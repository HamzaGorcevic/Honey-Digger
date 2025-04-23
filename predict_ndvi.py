import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
from datetime import datetime,timedelta
from sklearn.metrics import mean_squared_error
import math
def model(data:pd.DataFrame,curr_date,months_arg=1):
    data_to_predict = curr_date + timedelta(days=months_arg*30)
    
    X = data.drop(columns=['honey_points_month'])
    y = data['honey_points_month']
    split_size = math.floor(X.shape[0]*0.8)
    X_train = X[split_size:]
    y_train = y[split_size:]
    X_test = X[:split_size]
    y_test = y[:split_size]
    lr_model = LinearRegression()
    lr_model.fit(X_train,y_train)
    y_pred = lr_model.predict(X_test)
    error = mean_squared_error(y_test,y_pred)
    
    sorted_df = pd.DataFrame({
        'date':pd.to_datetime(X_test['year'].astype(str)+'-'+X_test['month'].astype(str)),
        'Actual':y_test.values,
        'Predicted':y_pred
    }).sort_values(by='date')
    
    plt.figure(figsize=[8,3])
    plt.scatter(sorted_df['date'],sorted_df['Actual'],color='red',s=110,alpha=0.6)
    
    plt.scatter(sorted_df['date'],sorted_df['Predicted'],color='blue',s=90,alpha=0.6)
    plt.xlabel('Months')
    plt.ylabel("Honey Points")
    plt.legend()
    plt.title('ACTUAL vs PREDICTED, based on rewards data')
    plt.plot(sorted_df['date'],sorted_df['Actual'],label='Actual')
    plt.plot(sorted_df['date'],sorted_df['Predicted'],label='Precited',color='blue')
    plt.show()
    
    print(error)
    

if __name__ =='__main__':
    date = datetime.now().date()
    data = pd.read_csv('processed_weather.csv')
    model(data,date)

# print(model(data).shape)

# So i have data aboud NDVI for each month, in time when user wants its result, i should predict ndvi for next month, based on current weather and ndvi data from previous year i have
# but also not only NDVI i should predict all other factors, and tell use if month will bring them honey
