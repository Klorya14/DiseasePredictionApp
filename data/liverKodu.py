# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 17:40:58 2026

@author: betul
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix

veriler=pd.read_csv("C:/Users/betul/egitim/liver_patient.csv")
age=veriler.iloc[:,0:1].values
cinsiyet=veriler.iloc[:,1:2].values
kalanlar=veriler.iloc[:,2:10].values
y=veriler.iloc[:,10].values

from sklearn import preprocessing
le=preprocessing.LabelEncoder()
cinsiyet[:,0]=le.fit_transform(cinsiyet[:,0])

sonuc=pd.DataFrame(data=cinsiyet,index=range(30691),columns=['gender'])
sonuc2=pd.DataFrame(data=age,index=range(30691),columns=['age'])
sonuc3=pd.DataFrame(data=kalanlar,index=range(30691),columns=['Total Billirubin','Direct Billirubin','Alkphos Alkaline Phosphotase','Sgpt Alamine Aminotransferase','Sgot Aspartate Aminotransferase','Total Protiens','ALB Albumin','A/G Ratio'])
s=pd.concat([sonuc,sonuc2],axis=1)
s1=pd.concat([s,sonuc3],axis=1)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(s1, y,test_size=0.33,random_state=0)

from sklearn.ensemble import RandomForestClassifier
rf_reg=RandomForestClassifier(n_estimators=75,criterion='entropy')
rf_reg.fit(x_train,y_train)
y_pred=rf_reg.predict(x_test)

cm=confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import classification_report
print(classification_report(y_test,y_pred))


import pickle 
pickle.dump(rf_reg,open('liver_model','wb'))



