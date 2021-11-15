from BottleRocket import BottleRocket
from BottleRocketConstants import Constants
import sys
import logging
import re

class Main:

    def __init__(self):
       BottleRocket.REGION_FILTER = self.get_region_filter()

    # get the region from input argument
    def get_region_filter(self):
        n = len(sys.argv) - 1 
        if n > 1:
            logging.error("Bottle Rocket can accept only single argument")
            sys.exit()
        elif n == 0:
            logging.error("Please provide a region as argument while running BottleRocket.py")
            sys.exit()
        else:
            region_filter = sys.argv[1]
            if re.match(Constants.EXPECTED_PATTERN, region_filter):
                return region_filter
            else:
                logging.error("Provided region must contain only allowed characters (numbers, alphabets or dashes)")
                sys.exit()

if __name__ == "__main__":
    Main()
    BottleRocket.create_directories()
    BottleRocket.store_response_json()
    region_filtered_dict = BottleRocket.parse_and_filter()
    BottleRocket.write_to_extra_credit_json(region_filtered_dict)
    logging.info("Done!!")