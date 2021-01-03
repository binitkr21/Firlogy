import numpy as np
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

data = pd.read_csv(r"/content/drive/My Drive/Colab Notebooks/Churn_Modelling.csv")
data

data.isnull().sum()
data.dtypes

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data["Geography"] = le.fit_transform(data["Geography"])
data["Gender"] = le.fit_transform(data["Gender"])
data

data.corr()

x = data.drop(["Exited","Surname","CustomerId"], axis = 1)
y = data["Exited"]

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

ct = ColumnTransformer([('encoder',  OneHotEncoder(), [2])], remainder='passthrough')
x = ct.fit_transform(x)

x.shape

from sklearn.model_selection import train_test_split
xtr, xts, ytr, yts = train_test_split(x, y, test_size = 0.2, random_state = 0)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
xtr = sc.fit_transform(xtr)
xts = sc.fit_transform(xts)



def nlpclassifier(data):
    classifier = Sequential()

    classifier.add(Dense(units = 6, activation = "relu", kernel_initializer = "he_uniform", input_dim = 13))

    classifier.add(Dense(units = 6, activation = "relu", kernel_initializer = "he_uniform"))

    classifier.add(Dense(units = 1 , activation = "softmax" , kernel_initializer = "glorot_uniform"))

    classifier.compile(optimizer= "adam", loss = "binary_crossentropy", metrics= ["accuracy"])

    model_history = classifier.fit(xtr, ytr, validation_split= 0.33, batch_size = 10, nb_epoch = 100)

    ypred = classifier.predict(xts)
    ypred = (ypred > 0.5)

    return ypred



