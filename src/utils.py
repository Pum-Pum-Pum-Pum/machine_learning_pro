import os
import sys
import numpy as np
import pandas as pd
from src.exception import CustomException
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path,"wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        CustomException(e,sys)
        
def evaluate_model(X_train, y_train, X_test, y_test, models,param):
    try:
        report = {}
        best_models = {}
        
        for i, model_name in enumerate(models.keys()):
            model = models[model_name]
            para = param.get(model_name, {})  # Get parameter grid for the model
            
            # Perform GridSearchCV
            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)
            
            # Get the best estimator from GridSearchCV
            best_model = gs.best_estimator_
            
            # Make predictions using the best model
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)
            
            # Calculate r2 scores
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            
            # Store the test score and the fitted model
            report[model_name] = test_model_score
            best_models[model_name] = best_model

        return report, best_models  # Return both scores and fitted models
    except Exception as e:
        CustomException(e, sys)
        
def load_object(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        CustomException(e, sys)        