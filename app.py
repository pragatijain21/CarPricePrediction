# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UD4oGEDPpkO0qQnn3f089PcFKORVejQy
"""

import numpy as np
from flask import Flask, request, jsonify,render_template
import requests
import pickle
from sklearn.preprocessing import StandardScaler
from datetime import date
import sklearn

app= Flask(__name__)
model= pickle.load(open('Car_prediction.pkl','rb'))

@app.route('/',methods=['GET'])
def Home():
  return render_template('index.html')


standard_to= StandardScaler()

@app.route('/predict',methods=['POST'])
def predict():
  Fuel_Type_Diesel=0
  if request.method=='POST':
    Year= int(request.form['Year'])
    Present_Price= float(request.form['Present_Price'])
    Kms_Driven= int(request.form['Kms_Driven'])
    Owner= int(request.form['Owner'])
    Fuel_Type_Petrol= request.form['Fuel_Type_Petrol']
    if Fuel_Type_Petrol=='Petrol':
      Fuel_Type_Petrol=1
      Fuel_Type_Diesel=0
    elif Fuel_Type_Petrol=='Diesel':
      Fuel_Type_Petrol=0
      Fuel_Type_Diesel=1
    else:
      Fuel_Type_Petrol=0
      Fuel_Type_Diesel=0
    Present_year= int(str(date.today())[0:4])
    Year=Present_year-Year
    Seller_Type_Individual= request.form['Seller_Type_Individual']
    if Seller_Type_Individual=='Individual':
      Seller_Type_Individual=1
    else:
      Seller_Type_Individual=0
    Transmission_Manual=request.form['Transmission_Manual']
    if Transmission_Manual=='Manual':
      Transmission_Manual=1
    else:
      Transmission_Manual=0
    features= np.array([Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual])
    y_predict= model.predict([features])
    output= round(y_predict[0],2)
    if output<0:
      return render_template('index.html',prediction_texts="Sorry, You cannot sell this Car")
    else:
      return render_template('index.html',prediction_texts="You can sell the Car at {} Lacs".format(output))
  else:
    return render_template('index.html')

if __name__=="__main__":
  app.run(debug=True)
