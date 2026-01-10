import numpy as np
import pandas as pd
from dataclasses import dataclass
import os
import sys

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,LabelEncoder,StandardScaler
from sklearn.compose import ColumnTransformer

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    x_preprocessor_path = os.path.join("artifacts","preprocessorX.pkl")
    y_preprocessor_path = os.path.join("artifacts","preprocessorY.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_transformation_object(self,numerical_cols,categorical_cols):

        try:
            numerical_pipeline_x = Pipeline([
            ("imputer",SimpleImputer(strategy="mean")),
            ("scale",StandardScaler())
        ])

            categorical_pipeline_x = Pipeline([
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("encoder",OneHotEncoder())
            ])

            preprocessor_x = ColumnTransformer(
                transformers = ([
                    ("numerical_pipeline",numerical_pipeline_x,numerical_cols),
                    ("categorical_pipeline",categorical_pipeline_x,categorical_cols)
                ])
            )

            lb_y = LabelEncoder()

            return (
                preprocessor_x,
                lb_y
            )
        except Exception as e:
            custom_exception = CustomException(e,sys)
            logging.error(custom_exception)
            raise custom_exception


    def initiate_transformation(self,train_path : str,test_path : str):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Loaded training and test Data successfully")

            logging.info("Data transformation is initiated")
            x_train = train_df.iloc[:,:-1]
            x_test = test_df.iloc[:,:-1]

            y_train = train_df.iloc[:,-1]
            y_test = test_df.iloc[:,-1]

            numerical_cols_x = [col for col in x_train.columns if x_train[col].dtype != "O"]
            categorical_cols_x = [col for col in x_train.columns if x_train[col].dtype == "O"]

            preprocessing_objects = self.get_transformation_object(numerical_cols_x,categorical_cols_x)

            x_train_preprocessed = preprocessing_objects[0].fit_transform(x_train)
            x_test_preprocessed = preprocessing_objects[0].transform(x_test)

            y_train_preprocessed = preprocessing_objects[1].fit_transform(y_train)
            y_test_preprocessed = preprocessing_objects[1].transform(y_test)

            preprocessed_train_array = np.c_[x_train_preprocessed,y_train_preprocessed]
            preprocessed_test_array = np.c_[x_test_preprocessed,y_test_preprocessed]
            logging.info("Data transformation is Complete")

            save_object(
                self.data_transformation_config.x_preprocessor_path,
                preprocessing_objects[0]
            )
            save_object(
                self.data_transformation_config.y_preprocessor_path,
                preprocessing_objects[1]
            )
            logging.info("X and Y Preprocessing objects are saved successfully")

            return(
                preprocessed_train_array,
                preprocessed_test_array,
                self.data_transformation_config.x_preprocessor_path,
                self.data_transformation_config.y_preprocessor_path
            )
        except Exception as e:
            custom_exception = CustomException(e,sys)
            logging.error(custom_exception)
            raise custom_exception