# -*- coding: utf-8 -*-
"""QoSallocation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yXr1SRE6u8yjGpvNjZV3vh9gwSQubJgW
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

df = pd.read_parquet("drive/My Drive/sidelink_dataframe.parquet")
df.to_csv('sidelink_dataframe.csv')
df.head()

df.shape

print(df.columns.values)

df.dtypes #data type of each column

df['Source'].values

qos = df.filter([ 'Source' ,'Destination', 'SNR' ,'RSRP' ,'RSSI',
 'NOISE POWER', 'RX_GAIN', 'SubFrame_NUMBER' 'SubFrame_LENGHT', 'Rx_power',
 'MCS' ,'Received Packets', 'speed_kmh_destination' ,'distance',
 'Packet_transmission_rate_hz', 'Sub_channels', 'Packet_error_ratio'], axis=1)

for col in qos.columns:
  if qos[col].isnull().sum()>0:
    print(col)
    print(qos[col].isnull().sum())

dups = qos.duplicated()
qos[dups]

qos.columns

qos.dtypes

import re
qos= qos.rename(columns = lambda x:re.sub('[^A-Za-z0-9_]+', '', x))
qos.head()

qos.shape

X=qos.iloc[:,:]
X=X.drop(['Packet_transmission_rate_hz'],axis=1)

y=qos['Packet_transmission_rate_hz']
#y=y.values.reshape(-1,1)

# split the dataset
from sklearn.model_selection import train_test_split
#y=y.values.reshape(-1,1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print('X_train : ')
print(X_train.shape)
print('')
print('X_test : ')
print(X_test.shape)
print('')
print('y_train : ')
print(y_train.shape)
print('')
print('y_test : ')
print(y_test.shape)

#Decision Tree
from sklearn.metrics import mean_squared_error

from sklearn.tree import DecisionTreeRegressor
# Create model
dt_model = DecisionTreeRegressor(max_depth=3)

# Fit the model to the training data
dt_model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = dt_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

print(f'Mean Squared Error: {mse:.4f}')

#LINEAR REGRESSOR

from sklearn.linear_model import LinearRegression
# Create a Linear Regression model
model = LinearRegression()

# Fit the model to the training data
model.fit(X_train, y_train)

# Make predictions on the test data
predictions = model.predict(X_test)

# Calculate Mean Squared Error
mse = mean_squared_error(y_test, predictions)

print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)
print("Mean Squared Error:", mse)

#KNN regressor

# Choose a range of k values
'''k_values = range(1, 20, 2)  # Odd numbers from 1 to 19
from sklearn.neighbors import KNeighborsRegressor

# Find optimal k using cross-validation
best_mse = float('inf')
best_k = None

for k in k_values:
    kmodel = KNeighborsRegressor(n_neighbors=k)
    kmodel.fit(X_train, y_train)
    predictions = kmodel.predict(X_train)
    mse = mean_squared_error(y_train, predictions)

    if mse < best_mse:
        best_mse = mse
        best_k = k

print("Optimal k:", best_k)
'''

from sklearn.neighbors import KNeighborsRegressor
# Create a KNN Regressor model
k = 5  # Number of neighbors
knnmodel = KNeighborsRegressor(n_neighbors=k)

# Fit the model to the training data
knnmodel.fit(X_train, y_train)

# Make predictions on the test data
predictions = knnmodel.predict(X_test)

# Calculate Mean Squared Error
mse = mean_squared_error(y_test, predictions)

print("Mean Squared Error:", mse)

'''from sklearn.svm import SVR

# Create an SVR model
svrmodel = SVR(kernel='linear')  # You can use different kernels like 'linear', 'poly', 'rbf', etc.

# Fit the model to the training data
svrmodel.fit(X_train, y_train)

# Make predictions on the test data
predictions = svrmodel.predict(X_test)

# Calculate Mean Squared Error
mse = mean_squared_error(y_test, predictions)

print("Mean Squared Error:", mse)'''

from sklearn.preprocessing import StandardScaler

yt_train=y_train.values.reshape(-1,1)
yt_test=y_test.values.reshape(-1,1)
# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
y_train_scaled = scaler.fit_transform(yt_train)
y_test_scaled = scaler.transform(yt_test)

from sklearn.svm import SVR
# SVR model
svr = SVR(kernel='linear', C=1.0, gamma=0.1)
svr.fit(X_train_scaled, y_train)

# Predicting
y_pred = svr.predict(X)