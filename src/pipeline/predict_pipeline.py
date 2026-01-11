import numpy as np
import pandas as pd
import sys
import os

from dataclasses import dataclass

from src.utils import load_object
from src.exception import CustomException
from src.logger import logging

class CustomData:
    def __init__(self,
        age : int,
        gender : str,
        weight : int,
        daily_water_intake : float,
        physical_activity_level : str,
        weather : str
    ):
        self.age = age
        self.gender = gender
        self.weight = weight
        self.daily_water_intake = daily_water_intake
        self.physical_activity_level = physical_activity_level
        self.weather = weather
    
    def get_data_dataframe(self):
        try:
            user_data_dataframe = {
                "Age" : [self.age],
                "Gender" : [self.gender],
                "Weight (kg)" : [self.weight],
                "Daily Water Intake (liters)" : [self.daily_water_intake],
                "Physical Activity Level" : [self.physical_activity_level],
                "Weather" : [self.weather]
            }
            return pd.DataFrame(user_data_dataframe)
        except Exception as e:
            custom_exception = CustomException(e,sys)
            logging.error(custom_exception)
            raise custom_exception


@dataclass
class Prediction:
    model_path = os.path.join("artifacts", "model.pkl")
    preprocessor_x_path = os.path.join("artifacts", "preprocessorX.pkl")
    preprocessor_y_path = os.path.join("artifacts", "preprocessorY.pkl")
    
    def predict(self,user_data_df):

        try:
            model = load_object(self.model_path)
            preprocessorX = load_object(self.preprocessor_x_path)
            preprocessorY = load_object(self.preprocessor_y_path)
            
            preprocessed_user_data = preprocessorX.transform(user_data_df)
            
            raw_prediction = model.predict(preprocessed_user_data)
            prediction_indices = raw_prediction.astype(int).ravel()
            prediction = preprocessorY.inverse_transform(prediction_indices)

            return prediction[0]
        
        except Exception as e:
            custom_exception = CustomException(e, sys)
            logging.error(custom_exception)
            raise custom_exception