import json
from typing import Dict, List
from BottleRocketConstants import Constants
from BottleRocketHelpers import Helpers
from netaddr import IPSet
import os
import uuid
import shutil
import netaddr
import logging
logging.basicConfig(level = logging.INFO)

class BottleRocket:

    REGION_FILTER = ''
    ec2_ip_list = []

    # create directories
    @staticmethod
    def create_directories():
        for directory in Constants.DIRECTORIES_LIST:
            try:
                if os.path.exists(directory):
                    logging.warning("Directory '%s' already exists. Removing it!" %directory)
                    shutil.rmtree(directory, ignore_errors=True)
                    os.makedirs(directory)
                    logging.info("New Directory '%s' created successfully" %directory)
                else:
                    os.makedirs(directory)
                    logging.info("Directory '%s' created successfully" %directory)
            except OSError as error:
                logging.error(error) 

    # Write the response to ip-ranges.json in incoming directory
    @staticmethod
    def store_response_json():
        logging.info("Reading content from '%s'" %Constants.AWS_URL)
        data = Helpers.read_response_from_url()
        # Store in incoming directory
        file_path = Helpers.get_file_path(Constants.INCOMING_DIRECTORY, Constants.IP_RANGES_FILE)
        with open(file_path, 'w') as f:
            f.write(data)
        logging.info("Finished writing the response to '%s' file" %Constants.IP_RANGES_FILE)

    @staticmethod
    def parse_and_filter() -> json:
        data = Helpers.get_json_data(Constants.INCOMING_DIRECTORY, Constants.IP_RANGES_FILE)
        prefix = data['prefixes']
        
        for element in prefix:
            ip = element['ip_prefix']
            element['ip_prefix'] = Helpers.increment_second_octet(ip)
            # check for EC2 service
            if 'EC2' in element['service']:
                # create a new key 'id' and assign uuid as value
                element['id'] = str(uuid.uuid4())
                Helpers.filter_by_region(element)
                
                # filter based on region
                region_filter = BottleRocket.REGION_FILTER
                Helpers.filter_by_uuid_region(element, region_filter)
                
                if element['region'] == region_filter:
                    BottleRocket.ec2_ip_list.append(element['ip_prefix'])
        logging.info("Finished filtering records based on '%s' region" %BottleRocket.REGION_FILTER) 
        return prefix

    @staticmethod
    def get_cidr_merge_list() -> List:
        # Create a list after cidr_merge
        return netaddr.cidr_merge(BottleRocket.ec2_ip_list)

    @staticmethod
    def calculate_adjoining_networks() -> Dict:
        logging.info("Finished creating cidr_merge list")
        merged_list = BottleRocket.get_cidr_merge_list()

        # Calculation for adjoining networks
        result = {} #Create a dictionary to store ip and merged value from cidr list
        logging.info("started calculating adjoining networks")

        if merged_list is None:
            logging.error("Error occured while doing a cidr_merge")

        if BottleRocket.ec2_ip_list is None:
            logging.error("Error occured while collecting IPs for region '%s'" %BottleRocket.REGION_FILTER)

        for m_val in merged_list:
            for ip in BottleRocket.ec2_ip_list:
                set1 = IPSet([m_val])
                set2 = IPSet([ip])
                if set1.issuperset(set2):
                    #appending values to result dictionary. With key as 'ip' and value as 'merged val'
                    result[str(ip)] = str(m_val)
        logging.info("Finished calculating adjoining networks")
        return result

    @staticmethod
    def write_to_extra_credit_json(prefix_dict):
        result = BottleRocket.calculate_adjoining_networks()

        if result is None:
            logging.error("Error occured while calculating adjoining networks")

        result_ip_list = result.keys()
        for element in prefix_dict:
            if 'EC2' in element['service']:
                ip = element['ip_prefix']
                if ip in result_ip_list:
                    element['ip_prefix'] = result[ip]
                    extra_credit_file_path = Helpers.get_file_path(Constants.EC2_REGION_DIRECTORY, 
                                                Constants.EXTRA_CREDIT_JSON)

                    # Write to extra_credit.json file
                    Helpers.write_content_to_new_file(extra_credit_file_path, element)
        logging.info('Finished writing to extra_credit.json')