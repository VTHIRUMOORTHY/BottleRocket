from BottleRocketConstants import Constants
import os
import json
import requests
import logging

class Helpers:
    
    @staticmethod
    def get_file_path(parent_folder, new_file) -> str:
        return os.path.join(os.getcwd(), parent_folder, new_file)

    @staticmethod
    def increment_second_octet(ip) -> str:
        # increment second number in ip_prefix
        octets = ip.split('.')
        new_octet = int(octets[1]) + Constants.INCREMENT_COUNT
        if new_octet <= 255:
            octets[1] = str(new_octet)
        else:
            logging.debug("increment ip address octet cannot be done for '%s'. Value goes above 255 !!!" %ip)
        return '.'.join(octets)

    @staticmethod
    def write_content_to_new_file(file_path, element):
        if os.path.exists(file_path):
            # If file already exists, append data
            with open(file_path, 'a') as f:
                f.write(',\n')
                json.dump(element,f,indent=4)                    
        else:
            # else, create new file and write data 
            with open(file_path, 'w') as f:
                json.dump(element,f,indent=4)

    @staticmethod
    def read_response_from_url():
        response = requests.get(Constants.AWS_URL)
        status = response.status_code
        if status == Constants.HTTP_SUCCESS:
            return response.text
        else:
            logging.error(f'Get request failed with status code{status}')
            raise Exception

    @staticmethod
    def filter_by_uuid_region(element, region_filter):
        if element['region'] == region_filter:
            uuid_filename = element['id'] + '.json'
            uuid_file_path = Helpers.get_file_path(Constants.EC2_FILTERED_DIRECTORY, uuid_filename)
            Helpers.write_content_to_new_file(uuid_file_path, element)

    @staticmethod
    def filter_by_region(element):
        region = element['region']
        region_filename = region + '.json'
        ec2_region_file_path = Helpers.get_file_path(Constants.EC2_REGION_DIRECTORY, region_filename)
        Helpers.write_content_to_new_file(ec2_region_file_path, element)

    @staticmethod
    def get_json_data(directory, filename) -> json:
        file_path = Helpers.get_file_path(directory, filename)
        f = open(file_path,)
        return json.load(f)