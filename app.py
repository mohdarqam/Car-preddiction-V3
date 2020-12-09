# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 19:53:13 2020

@author: Mohd Arqam
"""

from flask import Flask, render_template, request
import jsonify
#import pickle
import numpy as np
import joblib

app = Flask(__name__)

model = joblib.load('model.pkl', mmap_mode=None)

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
#    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Km_driven=int(request.form['Kms_Driven'])
        transmission=request.form['transmission']
        if(transmission=='Manual'):
            transmission = 0
        else:
             transmission = 1
        Owner=request.form['Owner']
        if(Owner=='first owner'):
            Owner = 1
        elif(Owner=='second owner'):
            Owner = 2
        elif(Owner=='third owner'):
            Owner = 3 
        else:
             Owner = 4
        mileage=float(request.form['mileage'])
        engine=float(request.form['engine'])
        max_power=float(request.form['max_power'])
        car_seat=int(request.form['car_seat'])
        
        fuel_Petrol=request.form['Fuel_Type_Petrol']
        if(fuel_Petrol=='Petrol'):
                fuel_Petrol=1
                fuel_Diesel=0
                fuel_LPG = 0
        elif(fuel_Petrol=='Diesel'):
            fuel_Petrol=0
            fuel_Diesel=1
            fuel_LPG = 0
        elif(fuel_Petrol=='LPG'):
            fuel_Petrol=0
            fuel_Diesel=0
            fuel_LPG = 1  
        else:
            fuel_Petrol=0
            fuel_Diesel=0
            fuel_LPG = 0
        Seller_Type=request.form['Seller_Type_Individual']
        if(Seller_Type=='Individual'):
                seller_type_Individual=1
                seller_type_Trustmark_Dealer=0
        elif(Seller_Type=='Trustmark_dealer'):
            seller_type_Individual=0
            seller_type_Trustmark_Dealer=1
        else:
             seller_type_Individual=0
             seller_type_Trustmark_Dealer=0
        Year=2020-Year
        prediction=model.predict([[Year,Km_driven,transmission,Owner,mileage,engine,max_power,car_seat,fuel_Diesel,fuel_LPG,fuel_Petrol,seller_type_Individual,seller_type_Trustmark_Dealer]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
    
    
