from BottleRocketHelpers import Helpers
from BottleRocket import BottleRocket
from BottleRocketConstants import Constants
import unittest
import os
import logging

class BottleRocketTest(unittest.TestCase):

    mock_json = {"ip_prefix": "142.14.160.72/29","region": "us-east-1",
            "service": "EC2","network_border_group": "us-east-1-mci-1",
            "id": "0a98474e-3afd-4b5b-89c3-ab902560501e"}

    def test_increment_second_octet(self):
        actual = Helpers.increment_second_octet('192.245.255.1')
        expected = '192.255.255.1'
        self.assertEqual(actual, expected)

    def test_create_directories(self):
        BottleRocket.create_directories()
        self.assertTrue(True, os.path.exists(Constants.INCOMING_DIRECTORY))
        self.assertTrue(True, os.path.exists(Constants.EC2_FILTERED_DIRECTORY))
        self.assertTrue(True, os.path.exists(Constants.EC2_REGION_DIRECTORY))

    def test_read_response_from_url(self):
        response = Helpers.read_response_from_url()
        self.assertIsNotNone(response)

    def test_filter_by_uuid_region(self):
        Helpers.filter_by_uuid_region(BottleRocketTest.mock_json, 'us-east-1')
        path = os.path.join(os.getcwd(), Constants.EC2_FILTERED_DIRECTORY, 
                        '0a98474e-3afd-4b5b-89c3-ab902560501e.json')
        self.assertTrue(True, path)

    def test_filter_by_region(self):
        Helpers.filter_by_region(BottleRocketTest.mock_json)
        path = os.path.join(os.getcwd(), Constants.EC2_REGION_DIRECTORY, 
                        'us-east-1.json')
        self.assertTrue(True, path)

    def test_get_file_path(self):
        self.assertEqual(Helpers.get_file_path("test","test_file.json"), 
                        os.path.join(os.getcwd(), 'test', 'test_file.json'))

if __name__ == '__main__':
    unittest.main()