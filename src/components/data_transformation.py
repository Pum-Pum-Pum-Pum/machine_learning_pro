import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer ## This is for missing values
from sklearn.pipeline import Pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    # to save pickle file
    preprocessor_obj_file_path = os.path.join('artifact','preprocessor.pkl')
    
class DataTransformation:
    def __init__(self):
        self.data_tranformation_config = DataTransformationConfig()
    
    # to create pickle files, after doing cat to numerical, standard scaler or onhot    
    def get_data_transformater_object(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = ["gender", "race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
            
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scalar",StandardScaler(with_mean=False))
                ]
            )
            
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            
            logging.info("Numerical scalling and Categorical columns encoding completed")
            
            # now we need combine Numerical and Categorical pipeline together so we use preprocessing for that
            preprocessor = ColumnTransformer(
                                                [
                                                    ("num_pipeline",num_pipeline,numerical_columns),
                                                    ("cat_pipeline", cat_pipeline,categorical_columns)
                                                ]
                                            )
            
            logging.info("preprocessor is successful")
            return preprocessor
        except Exception as e:
            CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info(f"train_df is loaded {train_df.shape}")
            logging.info(f"test_df is loaded {test_df.shape}")
            
            logging.info("obtaining preprocessing object and processing")
            
            preprocessing_obj = self.get_data_transformater_object()
            
            target_column_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]
            
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = train_df[target_column_name]
            
            logging.info("applying preprocessing object on train and test df")
            
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            
            # Umm he did input_feature_train_df shouldn't it be test?
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            
            # np.c_ is a NumPy shorthand for column-wise concatenation. It combines two arrays (or dataframes converted to arrays) as columns to form a single array.
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            logging.info("Savied preprocessing objects.")
            
            save_object (
                            file_path = self.data_tranformation_config.preprocessor_obj_file_path,
                            obj = preprocessing_obj
                
                        )
            
            return(
                train_arr,
                test_arr,
                self.data_tranformation_config.preprocessor_obj_file_path # Looks like some issue here
            )
        except Exception as e:
            CustomException(e, sys)