# # Importing Libraries
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# # Reading CSV
Crop_data = pd.read_csv("PraveenNewCropDataset.csv")
Crop_data.head(5)

# # Wrangling Data
Crop_data.drop(['District_Name','Crop','Season'],axis=1,inplace= True)
Crop_data.head(5)

##Training Dataset
X = Crop_data[['Crop_Year','Area','Temperature','Rainfall',]]
Y = Crop_data['Production']


reg = LinearRegression()

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=1)

reg.fit(X_train,y_train)

predictions = reg.predict(X_test)

print(predictions)

print(reg.score(X_test,y_test))

print(reg.predict([[2010,20089,25.2,25.98]]))