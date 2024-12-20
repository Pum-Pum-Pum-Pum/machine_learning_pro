import sys
import os

# Add the parent directory of "src" to sys.path
from src.logger import logging


def error_message_detail(error_msg, error_detail:sys):
    _,_,exc_tb=error_detail.exc_info() # first two variable are not required to not taking them
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = (f"Error occurred in python script name [{file_name}] line number [{exc_tb.tb_lineno}] error message [{str(error_msg)}]")
    return error_message
    
class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
        logging.info(f"Exception :: {self.error_message}")
        
    def __str__(self):
        return self.error_message
    
    
if __name__ == "__main__":
    try:
        a=1/0
    except Exception as e:
        logging.info("Divide by zero error")
        raise CustomException(e, sys)