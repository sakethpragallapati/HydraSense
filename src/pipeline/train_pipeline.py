from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

import sys

from src.exception import CustomException
from src.logger import logging

if __name__ == "__main__":
    try:
        ingestion_object = DataIngestion()
        transformation_object = DataTransformation()
        model_object = ModelTrainer()

        ingestion_object.initiate_ingestion()

        train_path = ingestion_object.data_ingestion_config.train_data_path
        test_path = ingestion_object.data_ingestion_config.test_data_path

        transformation_results = transformation_object.initiate_transformation(
            train_path,
            test_path
        )

        preprocessed_train_array = transformation_results[0]
        preprocessed_test_array = transformation_results[1]

        model_object.initiate_model_training(preprocessed_train_array,preprocessed_test_array)
    except Exception as e:
        custom_excpetion = CustomException(e,sys)
        logging.info("An error occurred in the training pipeline")
        logging.error(custom_excpetion)
        raise custom_excpetion