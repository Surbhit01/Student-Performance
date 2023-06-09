import os
import sys

import numpy as np 
import pandas as pd
import dill

from src.exception import CustomException
from src.logger import logging
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logging.info('Preprocessor model saved')
        

    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train,y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):

            #Selecting the ith model and parameters
            model = list(models.values())[i]
            pm = param[list(models.keys())[i]]

            gs = GridSearchCV(model,pm,cv=3)
            gs.fit(X_train,y_train)

            #Setting best parameters
            model.set_params(**gs.best_params_)

            #Training model
            model.fit(X_train,y_train)

            #Prediction on training data
            y_train_pred = model.predict(X_train)
            
            #Prediction on testing data
            y_test_pred = model.predict(X_test)

            #Training prediction r2 score
            train_model_r2 = r2_score(y_train,y_train_pred)

            #Testing prediction r2 score
            test_model_r2 = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_r2

            logging.info("MODEL: {} ----TRAINING r2: {}--------TESTING r2: {}".format(list(models.keys())[i], train_model_r2, test_model_r2))
        
        return report



    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e,sys)

