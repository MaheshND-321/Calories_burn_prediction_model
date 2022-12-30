from flask import Flask, render_template, request
from termcolor import colored
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics

app = Flask(__name__)

@app.route('/',methods = ["GET","POST"])
def prediction():
    if request.method == "POST":
        #Data collection and processing
        cal = pd.read_csv(r'C:\Users\alexa\Downloads\calories.csv')
        exc = pd.read_csv(r'C:\Users\alexa\Downloads\exercise.csv')

        # As we can say that the heart_rate is the parameter which shows the rate of activity(calories burnt)
        # First combine the Two Datasets
        cal_df = pd.concat([exc, cal['Calories']], axis =1)

        # Converting the text data to numerical value
        cal_df.replace({'Gender':{'male':0,'female':1}}, inplace=True)

        # Separtainhg the features and target values
        x = cal_df.drop(columns=['User_ID','Calories'])
        y = cal_df['Calories']

        # Splitting the data into test and training data
        x_train, x_test, y_train ,y_test = train_test_split(x, y, test_size=0.2, random_state=2)
        # print(x.shape, x_train.shape, x_test.shape)

        # XGBoost Regresssor
        # Loading the model
        model = XGBRegressor()
        # Traing the Data
        model.fit(x_train, y_train)  #Learning the pattern between the x_train and y_train

        # Prediction on the test Data
        train_data_prediction = model.predict(x_train)
        #print(train_data_prediction)
        # Finding the Mean Absolute Value Error
        error1= metrics.mean_absolute_error(y_train, train_data_prediction)
        #Building the Prediction model
        #Inputing the Data
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
        text = "The Amount Of Calories Burnt Value is :   " + str(prediction[0]) +  "  KJ"
        return text
    return render_template("form.html")

if __name__ == '__main__':
    app.run(debug=True)