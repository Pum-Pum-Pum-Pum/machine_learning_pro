import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import ModelTrainer, ModelTrainerConfig

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('artifact','data.csv')
    train_data_path: str = os.path.join('artifact','train.csv')
    test_data_path: str = os.path.join('artifact','test.csv')
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion initiation part")
        try:
            df = pd.read_csv(r'notebook\data\stud.csv')
            logging.info(f"Data frame was loaded {df.shape}")
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True) 
            
            train_set, test_set = train_test_split(df, test_size= 0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True) 
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True) 
            
            logging.info("Ingestion of data completed")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path            
            )
        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    
    data_transformation = DataTransformation()
    train_array, test_array, obj_path = data_transformation.initiate_data_transformation(train_data, test_data)
    
    model_trainer = ModelTrainer()
    r2_score=model_trainer.initiate_model_trainer(train_array, test_array)
    logging.info(f"the best models r2 score is {r2_score}")
    
    