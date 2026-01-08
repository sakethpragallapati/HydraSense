import sys
from src.logger import logging

def error_message_details(error,error_details : sys) -> tuple[str]:

    _,_,exc_tb = error_details.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = (
        f"\nError occured in python script [{file_name}] \n"
        f"Line number [{line_number}] \n"
        f"Error message [{str(error)}]"
    )
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_details:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(
            error_message,
            error_details
        )

    def __str__(self):
        return self.error_message