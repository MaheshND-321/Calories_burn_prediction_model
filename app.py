from flask import Flask, render_template, request
from termcolor import colored
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics
import pickle

app = Flask(__name__)

@app.route('/',methods = ["GET","POST"])
def prediction():
    if request.method == "POST":
        #Data collection and processing
        model = pickle.load(open('calmodel.pkl','rb'))
        list=[]
        gender = request.form.get("gender")
        if gender=='male'or gender=='Male':
            gender=0
        else:
            gender=1
        list.append(gender)
        age = request.form.get("age")
        list.append(age)
        height = request.form.get("height")
        list.append(height)
        weight = request.form.get("weight")
        list.append(weight)
        duration = request.form.get("duration")
        list.append(duration)
        heart_rate = request.form.get("heart_rate")
        list.append(heart_rate)
        Body_temperature = request.form.get("Body_temperature")
        list.append(Body_temperature)
        # Changing the list into Numpy_array
        input_data = np.asarray(list)
        #reshaping the array
        input_data = input_data.reshape(1,-1)  # Just Giving only 1 row soo...
        prediction = model.predict(input_data)
        # print("The Calories Burnt Value is : ",prediction[0])
        return render_template("form.html",text = str("The Amount Of Calories Burnt Value is :   " + str(prediction[0]) +  "  KJ"))
    return render_template("form.html")

if __name__ == '__main__':
    app.run(debug=True)