from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('rfrm.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Diesel=0
    Electric=0
    LPG=0
    Trustmark_Dealer=0
    if request.method == 'POST':
        year = int(request.form['year'])
        km_driven=float(request.form['km_driven'])
        mileage=int(request.form['mileage'])
        engine=int(request.form['engine'])
        max_power=int(request.form['max_power'])
        seats=int(request.form['seats'])
        Individual=request.form['Individual']
        if(Individual=='Individual'):
                Individual=1
                Trustmark_Dealer=0
        elif(Individual=="Trustmark_Dealer"):
            Individual=0
            Trustmark_Dealer=1
        else:
            Individual=0
            Trustmark_Dealer=0
        Manual=request.form['Manual']
        if(Manual=='Manual'):
            Manual=1
        else:
            Manual=0	
        Petrol=request.form['Petrol']
        if(Petrol=='Petrol'):
            Petrol=1
            Diesel=0
            Electric=0
            LPG=0
        elif(Petrol=='Diesel'):
            Petrol=0
            Diesel=1
            Electric=0
            LPG=0
        elif(Petrol=='Electric'):
            Petrol=0
            Diesel=0
            Electric=1
            LPG=0
        elif(Petrol=='LPG'):
            Petrol=0
            Diesel=0
            Electric=0
            LPG=1
        elif(Petrol=='CNG'):
            Petrol=0
            Diesel=0
            Electric=0
            LPG=0
        prediction=model.predict([[year,km_driven,mileage,engine,max_power,seats,Individual,Trustmark_Dealer,Manual,Diesel,Electric,LPG,Petrol]])
        output=prediction[0]
        if output<0:
            return render_template('index.html',prediction_texts="Error Prediction")
        else:
            return render_template('index.html',prediction_text="Car Value Rs: {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

