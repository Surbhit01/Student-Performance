from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

#Home route
@app.route('/')
def index():
    print('index.html')
    return render_template('index.html')

#Prediction route
@app.route('/predictdata', methods=['GET','POST'])
def predict_datapoint():
    if request.method == 'GET':
        print('home.html--GET')
        return render_template('home.html')

    else:
        print('home.html--POST')
        data = CustomData(
            gender = request.form.get('gender'),
            race_ethnicity = request.form.get('race_ethnicity'),
            parental_level_of_education = request.form.get('parental_level_of_education'),
            lunch = request.form.get('lunch'),
            test_preparation_course = request.form.get('test_preparation_course'),
            reading_score = request.form.get('reading_score'),
            writing_score = request.form.get('writing_score')
        )
        print('gender: {}'.format(request.form.get('gender')))
        print('race_ethnicity: {}'.format(request.form.get('race_ethnicity')))
        print('parental_level_of_education: {}'.format(request.form.get('parental_level_of_education')))
        print('lunch: {}'.format(request.form.get('lunch')))
        print('test_preparation_course: {}'.format(request.form.get('test_preparation_course')))
        print('reading_score: {}'.format(request.form.get('reading_score')))
        print('writing_score: {}'.format(request.form.get('writing_score')))
        

        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        if results[0] > 100:
            marks = 100
        elif results[0] < 0:
            marks = 0
        else:
            marks = results[0]

        return render_template('home.html', results=marks)


if __name__=="__main__":
    app.run(host='0.0.0.0')


        
