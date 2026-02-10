# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 17:36:41 2026

@author: betul
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix

veriler=pd.read_csv("C:/Users/betul/egitim/diabetes.csv")
x=veriler.iloc[:,0:8].values
y=veriler.iloc[:,8].values

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x, y,test_size=0.33,random_state=0)

from sklearn.ensemble import RandomForestClassifier
rf_reg=RandomForestClassifier(n_estimators=100,criterion='log_loss')
rf_reg.fit(x_train,y_train)
y_pred=rf_reg.predict(x_test)

cm=confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import classification_report
print(classification_report(y_test,y_pred))


import pickle
pickle.dump(rf_reg,open('diabetes_model','wb'))

