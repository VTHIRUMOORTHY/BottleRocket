class Constants:

    EXPECTED_PATTERN = '^[A-Za-z0-9-]*$'
    HTTP_SUCCESS = 200
    AWS_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    IP_RANGES_FILE = 'ip-ranges.json'
    EXTRA_CREDIT_JSON = 'extra_credit.json'
    INCOMING_DIRECTORY = 'incoming'
    EC2_REGION_DIRECTORY = 'ec2_by_region'
    EC2_FILTERED_DIRECTORY = 'ec2_filtered'
    INCREMENT_COUNT = 10
    DIRECTORIES_LIST = [INCOMING_DIRECTORY, 
                        EC2_REGION_DIRECTORY, 
                        EC2_FILTERED_DIRECTORY]