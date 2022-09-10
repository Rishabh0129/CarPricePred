from flask import render_template, request, Flask
import requests
from datetime import date
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
# import jsonify
app=Flask(__name__)
model=pickle.load(open('rfModel.pkl','rb'))

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')



standardScaler=StandardScaler()
@app.route('/predict',methods=['POST'])
def predict():
    # Fuel_Type_Diesel=0
    if request.method=='POST':
        Year= int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if (Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        todays_date = date.today()
        Current_year = todays_date.year
        Year = Current_year - Year
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if (Seller_Type_Individual == 'Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Mannual = request.form['Transmission_Mannual']
        if (Transmission_Mannual == 'Mannual'):
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0
        prediction = model.predict([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol,
                                     Seller_Type_Individual, Transmission_Mannual]])
        output = round(prediction[0], 2)
        if output < 0:
            return render_template('index.html', prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html', prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')




if __name__ == "__main__":
    app.run(debug=True)