import numpy as np
import pandas as pd
from dataclasses import dataclass
import os
import sys

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,test_model

@dataclass
class ModelTrainerConfig:
    model_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_training(self,preprocessed_train_array,preprocessed_test_array):

        try:
            logging.info("Model Training is initiated")
            models = {
                "LogisticRegression" : LogisticRegression(),
                "KNeighborsClassifier" : KNeighborsClassifier(),
                "LinearSVC" : LinearSVC(),
                "GaussianNB" : GaussianNB(),
                "DecisionTreeClassifier" : DecisionTreeClassifier(),
                "RandomForestClassifier" : RandomForestClassifier(),
                "GradientBoostingClassifier" : GradientBoostingClassifier(),
                "XGBClassifier" : XGBClassifier(),
                "LGBMClassifier" : LGBMClassifier(verbosity=-1)
            }
            x_train = preprocessed_train_array[:,:-1]
            y_train = preprocessed_train_array[:,-1]

            x_test = preprocessed_test_array[:,:-1]
            y_test = preprocessed_test_array[:,-1]

            best_model_name = ""
            best_accuracy = 0

            for model_name in models:
                model = models[model_name]
                model.fit(x_train,y_train)
                y_pred = model.predict(x_test)

                model_accuracy_score = test_model(y_test,y_pred)

                if(model_accuracy_score > best_accuracy):
                    best_model_name = model_name
                    best_accuracy = model_accuracy_score
            
            if best_accuracy < 0.6:
                custom_exception = CustomException("No best model found for the dataset",sys)
                logging.error(custom_exception)
                raise custom_exception
            
            best_model = models[best_model_name]

            save_object(
                self.model_trainer_config.model_path,
                best_model
            )

            logging.info(f"{model_name} model chosen and saved successfully")

            return (
                model_name,
                best_accuracy,
                self.model_trainer_config.model_path
            )
        except Exception as e:
                custom_exception = CustomException(e,sys)
                logging.error(custom_exception)
                raise custom_exception