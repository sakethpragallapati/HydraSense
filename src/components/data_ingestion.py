import pandas as pd
from dataclasses import dataclass
import os
import sys

from sklearn.model_selection import train_test_split

from src.components.data_transformation import DataTransformation

from src.exception import CustomException
from src.logger import logging

@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join("artifacts","train.csv")
    test_data_path = os.path.join("artifacts","test.csv")
    raw_data_path = os.path.join("artifacts","raw.csv")

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
    
    def initiate_ingestion(self):
        try:
            logging.info("Data ingestion started")

            logging.info("Making Artifacts directory")
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path),exist_ok=True)
            logging.info("Artifacts directory is created successfully")

            logging.info("Reading the raw data from the notebook directory")

            df = pd.read_csv("notebook/data/data.csv")
            x = df.iloc[:,:-1]
            y = df.iloc[:,-1]

            logging.info("Initating Train test split")
            x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42,shuffle=True)
            logging.info("Train test split was successful!")

            df.to_csv(self.data_ingestion_config.raw_data_path,index=False)
            pd.concat([x_train,y_train],axis=1).to_csv(self.data_ingestion_config.train_data_path,index=False)
            pd.concat([x_test,y_test],axis=1).to_csv(self.data_ingestion_config.test_data_path,index=False)
            logging.info("Saved the Train and Test datafiles in the artifacts folder")

            return(
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path
            )

        except Exception as e:
            custom_exception = CustomException(e,sys)
            logging.info(custom_exception)
            raise custom_exception

if __name__ == "__main__":
    ingestion = DataIngestion()
    ingestion.initiate_ingestion()

    transformation = DataTransformation()
    transformation_results = transformation.initiate_transformation(
        ingestion.data_ingestion_config.train_data_path,
        ingestion.data_ingestion_config.test_data_path
    )