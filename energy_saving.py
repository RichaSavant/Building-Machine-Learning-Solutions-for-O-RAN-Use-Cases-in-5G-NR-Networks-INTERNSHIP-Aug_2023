# -*- coding: utf-8 -*-
"""Energy_Saving.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s01Rl4FQdIAHMBtp4hJGFDeFuerIglkQ
"""

'''
BSs (LTE’s eNodeBs) can be
either in an active state (handling UEs’ data) or in an idle state
(transmitting only downlink control signaling).

the classifier determines its
class for the next period of time. We defined the following
two classes:
 IDLE
 DOWNLOADING

CLASSIFICATION: Random Forest, K means clustering

'''

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

df =pd.read_csv("drive/My Drive/Emerged.csv")
df.head()

df.shape

print(df.columns.values)

for i in df.columns:

  if df[i].isnull().sum()>0:
    df[i].fillna(df[i].mode()[0],inplace=True)

df.isnull().sum()

df.drop(df.index[(df["Longitude"] == "Longitude")],axis=0,inplace=True)    #REMOVING string VALUES

df.shape

df=df.drop(['Operatorname','NetworkMode','NRxRSRP','NRxRSRQ','Timestamp'], axis=1)

df.dtypes                     #rsrq,snr,rssi,cqi

df['ServingCell_Distance'] = df['ServingCell_Distance'].replace(['-'], 0)

df['ServingCell_Distance'] = df['ServingCell_Distance'].replace(0,df["ServingCell_Distance"].mode()[0])

df["ServingCell_Distance"] = df["ServingCell_Distance"].apply(pd.to_numeric)

df['ServingCell_Lon'] = df['ServingCell_Lon'].replace(['-'], 0)
df['ServingCell_Lat'] = df['ServingCell_Lat'].replace(['-'], 0)
df['RSRQ'] = df['RSRQ'].replace(['-'], 0)
df['SNR'] = df['SNR'].replace(['-'], 0)
df['CQI'] = df['CQI'].replace(['-'], 0)
df['RSSI'] = df['RSSI'].replace(['-'], 0)

df['State'] = df['State'].replace('D',1)
df['State'] = df['State'].replace('I',0)

df["State"] = df["State"].apply(pd.to_numeric)

df["ServingCell_Lon"] = df["ServingCell_Lon"].apply(pd.to_numeric)
df["ServingCell_Lat"] = df["ServingCell_Lat"].apply(pd.to_numeric)
df["RSRQ"] = df["RSRQ"].apply(pd.to_numeric)
df["RSSI"] = df["RSSI"].apply(pd.to_numeric)
df["CQI"] = df["CQI"].apply(pd.to_numeric)
df["SNR"] = df["SNR"].apply(pd.to_numeric)

df['ServingCell_Lon'] = df['ServingCell_Lon'].replace(0,df["ServingCell_Lon"].mode()[0])
df['ServingCell_Lat'] = df['ServingCell_Lat'].replace(0,df["ServingCell_Lat"].mode()[0])
df['RSRQ'] = df['RSRQ'].replace(0,df["RSRQ"].mode()[0])
df['SNR'] = df['SNR'].replace(0,df["SNR"].mode()[0])
df['CQI'] = df['CQI'].replace(0,df["CQI"].mode()[0])
df['RSSI'] = df['RSSI'].replace(0,df["RSSI"].mode()[0])

df["RSRP"] = df["RSRP"].apply(pd.to_numeric)
df["Longitude"] = df["Longitude"] .apply(pd.to_numeric)
df["Latitude"] = df["Latitude"] .apply(pd.to_numeric)
df["Speed"] = df["Speed"].apply(pd.to_numeric)
df["CellID"] = df["CellID"].apply(pd.to_numeric)
df["DL_bitrate"] = df["DL_bitrate"].apply(pd.to_numeric)
df["UL_bitrate"] = df["UL_bitrate"].apply(pd.to_numeric)

df.dtypes

df.shape

dups = df.duplicated()
df[dups]

df.drop_duplicates(keep=False, inplace=True)

df.shape

'''       SAVE TIME

import plotly.express as px

for col in df.columns:
  fig=px.box(df,y=col)
  fig.show()

  '''

for col in df.columns:                        #calc z score and number of outliers ---- not many outliers so we ignore.
  if df[col].dtypes!=object:
    print(col)
    u=df[col].mean() + 3*df[col].std()
    l=df[col].mean() - 3*df[col].std()
    print("Upper limit",u)
    print("Lower limit",l)
    print(len(df[(df[col] > u) | (df[col]< l)]))

df.columns

#splitting x and y
X=df.iloc[:,:]
X=X.drop(['State'],axis=1)
X.shape

y=df['State']
y.shape

y.head()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print('X_train : ')
print(X_train.head())
print('')
print('X_test : ')
print(X_test.head())
print('')
print('y_train : ')
print(y_train.head())
print('')
print('y_test : ')
print(y_test.head())

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

#RANDOM FOREST CLASSIFIER

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

rf = RandomForestClassifier(random_state=0, n_estimators=500)
rf.fit(X, y)
print(rf.predict(X_test))

(rf.predict(X_test) == 0).sum().sum()

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import math
# Given values
Y_true = y_test  # Y_true = Y (original values)

# calculated values
y_pred = rf.predict(X_test)  # Y_pred = Y'

# Calculation of Mean Squared Error (MSE)
mse=mean_squared_error(Y_true,y_pred)
rmse = math.sqrt(mse)
print(mse)
print("The difference between actual and predicted values", rmse)
print(mean_absolute_error(y_test, y_pred))

#K MEANS CLUSTERING

X1=df.iloc[:,:]
y1=df['State']

X1.columns

cols = X1.columns

from sklearn.preprocessing import MinMaxScaler

ms = MinMaxScaler()

X1 = ms.fit_transform(X1)

X1 = pd.DataFrame(X1, columns=[cols])

X1.head()

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=4, random_state=0)

kmeans.fit(X1)

kmeans.cluster_centers_

kmeans.inertia_

labels = kmeans.labels_

# check how many of the samples were correctly labeled
correct_labels = sum(y1 == labels)

print("Result: %d out of %d samples were correctly labeled." % (correct_labels, y1.size))


print('Accuracy score: {0:0.2f}'. format(correct_labels/float(y1.size)))

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=5,random_state=0)

kmeans.fit(X1)

labels = kmeans.labels_

# check how many of the samples were correctly labeled


correct_labels = sum(y1 == labels)
print("Result: %d out of %d samples were correctly labeled." % (correct_labels, y1.size))

print('Accuracy score: {0:0.2f}'. format(correct_labels/float(y1.size)))