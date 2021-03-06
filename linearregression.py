# -*- coding: utf-8 -*-
"""LinearRegression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1a8dLjdszVmhKR-qmmEq7qkURPY_TbCv8
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import kurtosis, skew
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import LocalOutlierFactor
from scipy.special import boxcox, inv_boxcox
from sklearn.metrics import mean_absolute_error, mean_squared_error

# load data 

houseData = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Bengaluru_House_Data.csv')

# check columns and data in houseData
print(houseData.columns)

houseData.head()

houseData.info()

print(houseData.apply(lambda col: col.unique()))

houseData.isnull().sum()

houseData=houseData.dropna()

houseData.isna()

houseData.shape

houseData = houseData.drop_duplicates()

# plotting correlation heatmap
# Assumption 3: Data features should not have multicolilinearlity 
dataplot = sns.heatmap(houseData.corr(), cmap="YlGnBu", annot=True)

houseData.shape

sns.displot(houseData['price'])
plt.show()
stats.probplot(houseData['price'],dist="norm", plot=plt)
plt.show()

sns.pairplot(houseData,hue ='price')

skew(houseData.price),kurtosis(houseData.price)

#transform the data using box-cox
price_Transformed, priceLambda = stats.boxcox(houseData['price']);
price_logTransform = np.log(houseData['price']);

#plot the distribution curve and QQ-plot for transformed data
sns.distplot(price_Transformed);
plt.show()
sns.displot(price_logTransform);
plt.show()

stats.probplot(price_Transformed,dist="norm", plot=plt)
plt.show()
stats.probplot(price_logTransform,dist="norm", plot=plt)
plt.show()

print(skew(price_Transformed),kurtosis(price_Transformed))

"""From info of data set we understood these are numeric independent variables, lets see the distribution of the variables



*   Bath
*   Balcony

"""

sns.distplot(houseData['bath'])
plt.show()
stats.probplot(houseData['bath'],dist="norm",plot=plt)

sns.distplot(houseData['balcony'])
plt.show()
stats.probplot(houseData['balcony'],dist="norm",plot=plt)

print(skew(houseData.bath),kurtosis(houseData.bath))
print(skew(houseData.balcony),kurtosis(houseData.balcony))

# print(houseData['bath'].unique())
# bath_transformed ,lambd= stats.boxcox(houseData['bath']);
# sns.displot(bath_transformed)
# plt.show()
# stats.probplot(bath_transformed,dist="norm",plot=plt)
# plt.show()
# print(bath_transformed)


# this was done before checking skewness.
# the kurtosis and skewness gives us idea that applying boxcox is not needed

df1=houseData.drop(['area_type', 'availability','society'], axis = 1)

df1['price_Transformed'] =  price_Transformed

df1['BHK'] = df1['size'].apply(lambda x: x.split(' ')[0])

df1['location'] = df1['location'].apply(lambda x: x.strip())

df1.head(10)

df1.to_csv("data_Location_Column.csv")

print(df1['total_sqft'].unique())

def conv(x):
    arr = x.split('-')
    if len(arr) == 2:
        avg = (float(arr[0]) + float(arr[1]))/2
        return avg
    try:
        return float(x)
    except:
        return None

df1['total_sqft'] = df1['total_sqft'].apply(lambda x: conv(x))

stats.probplot(df1['total_sqft'],dist ="norm",plot=plt)

df1['total_sqft'].dropna()

sns.distplot(df1['total_sqft'])
plt.show()

df1.reset_index(drop=True)

df1.dropna(inplace=True)
df1.total_sqft.isna()
print(df1.total_sqft.sum())
# if df1.total_sqft.any() == 'NaN':
#   print("yes")
print(skew(df1.total_sqft),kurtosis(df1.total_sqft))

stats.probplot(df1['total_sqft'],dist ="norm",plot=plt)

# total_sqft_norm,lambd = stats.boxcox(df1['total_sqft'])
# stats.probplot(total_sqft_norm,dist ="norm",plot=plt)
# #  there are outliers

sns.scatterplot(x=total_sqft_norm,y=df1['price'])

# df1['total_sqft_norm']= total_sqft_norm
df1['total_sqft_norm']= df1.total_sqft

# Remove outliers using boxplot
df1.boxplot(column=['total_sqft_norm'])

df1.drop(['total_sqft','price','size'],axis= 1,inplace=True);
df1.reset_index()
df1.dropna(inplace=True)
df1.shape
df1.columns

location_count=df1.location.value_counts()
location_count

# location count less than 10  mark as other
location_count_10 = location_count[location_count < 10]
df1.location = df1.location.apply(lambda x:'other' if x in location_count_10 else x)

df1.location.value_counts()
len(df1.location)

# one hot encoding for categorial features
dummies = pd.get_dummies(df1.location);

dummies.columns
# df1.drop(['location'],axis=1,inplace=True)
Final_data = pd.concat([df1,dummies],axis=1)

Final_data.drop(['location'],axis=1,inplace=True)

Final_data.fillna("NaN",inplace=True);

# split data using train_test_split
Final_data.dropna(inplace=True)
X = Final_data.drop(['price_Transformed'],axis=1);
Y = Final_data['price_Transformed']
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,random_state=23,test_size=0.33)
print(X_train.shape);
print(X_test.shape);
print(Y_train.shape);
print(Y_test.shape);

# # identify outliers in the training dataset
# # Refered from:https://machinelearningmastery.com/how-to-use-statistics-to-identify-outliers-in-data/
# lof = LocalOutlierFactor()
# yhat = lof.fit_predict(X_train)
# # select all rows that are not outliers
# mask = yhat != -1
# # print()
# X_train, Y_train = X_train.iloc[mask, :].values, Y_train.iloc[mask].values
# # summarize the shape of the updated training dataset
# print(X_train.shape, Y_train.shape)

linerReg = LinearRegression();
linerReg.fit(X_train.values,Y_train);
y_Pred = linerReg.predict(X_test)

y_Pred

# Reference:https://stackoverflow.com/questions/26391454/reverse-box-cox-transformation
Y_Pred_Transform = inv_boxcox(y_Pred, priceLambda)
Y_Pred_Transform

residuals = (Y_test -y_Pred)
residuals
# sns.scatterplot(x=Y_test,y=residual,hue=Final_data['price_Transformed'])

plt.scatter(Y_test, residuals)
plt.plot(Y_test, [0]*len(Y_test))

errors = mean_squared_error(Y_test, y_Pred)
errors

X.total_sqft_norm

def predict_price(location, sqft,bath, bhk,balcony):
  loc_index=np.where(X.columns==location)[0][0]
  x = np.zeros(len(X.columns))
  # print(X.columns)
  x[0] = bath
  x[1] = balcony
  x[2] = bhk
  x[3] = sqft
  if loc_index >= 0 :
    x[loc_index] = 1
  # print(len(x))
  return linerReg.predict([x])[0]
  
location = '1st Phase JP Nagar'
sqft =3453;
pred=predict_price(location,sqft,2,3,1);
print(pred)
print(X.columns)

result = inv_boxcox(pred, priceLambda)
print("price per sqft in area {0} is {1}".format(location,result*100000/sqft))

import pickle 
pickle.dump(linerReg,open('HouseDataPrediction.pkl','wb'));