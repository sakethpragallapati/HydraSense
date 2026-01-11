import os
import sys
import pickle

from sklearn.metrics import accuracy_score

from src.exception import CustomException
from src.logger import logging

def save_object(file_path: str, obj):
    """
    Saves any Python object as a pickle file.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file:
            pickle.dump(obj, file)

        logging.info(f"Object saved successfully at {file_path}")

    except Exception as e:
        custom_exception = CustomException(e, sys)
        logging.error(custom_exception)
        raise custom_exception
    
def test_model(y_test,y_pred)->int:
    try:
        model_accuracy_score = accuracy_score(y_test,y_pred)
        return model_accuracy_score
    
    except Exception as e:
        custom_exception = CustomException(e, sys)
        logging.error(custom_exception)
        raise custom_exception

def load_object(file_path : str):
    try:
        with open(file_path,"rb") as file_object:
            return pickle.load(file_object)
    except Exception as e:
        custom_exception = CustomException(e, sys)
        logging.error(custom_exception)
        raise custom_exception