import logging
import os
import datetime
import random
from pathlib import Path
from .models import *
from django.conf import settings
logger = logging.getLogger("api_calls")

class APILogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.path.split('/')[2:-1],"request.path")  
        module_name = '_'.join(request.path.split('/')[2:-1])
        random_number = random.randint(1, 1000)

        # Log information about the API call
        if not request.path.startswith('/admin/')and self.is_logging_enabled(module_name):
            self.log_api_call(request, module_name, random_number)

        response = self.get_response(request)

        # Log information about the API response if logging is enabled
        if not request.path.startswith('/admin/') and self.is_logging_enabled(module_name):
            self.log_api_response(request, response, module_name, random_number)

        return response
    
    def is_logging_enabled(self, module_name):
        try:
            system_config = SystemConfig.objects.get(api_name=module_name)
            return system_config.config_value
        except SystemConfig.DoesNotExist:
            return False

    def log_api_call(self, request, module_name, random_number):
        
        base_dir = settings.BASE_DIR
        log_directory = os.path.join(base_dir, 'data','logs') 
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file_path = os.path.join(log_directory, current_date, f"{module_name}.log")

        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        
        log_message = f"[{datetime.datetime.now()}] [Random: {random_number}] API call: {request.method} {request.path} from {request.META['REMOTE_ADDR']} headers {request.headers}"
        with open(log_file_path, 'a') as file:
            file.write(log_message + '\n')

        logger.info(log_message) # Log to console

    def log_api_response(self, request, response, module_name, random_number):
            print("log_api_response,,,,,,,,,")
            base_dir = settings.BASE_DIR
            log_directory = os.path.join(base_dir, 'data','logs') 
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            log_file_path = os.path.join(log_directory, current_date, f"{module_name}.log")
            
            
            log_message = f"[{datetime.datetime.now()}] [Random: {random_number}] API response: {response.status_code} for {request.method} {request.path} response data {response.data}"

            with open(log_file_path, 'a') as file:
                file.write(log_message + '\n')

            logger.info(log_message) 