import os
import sys
import pickle
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