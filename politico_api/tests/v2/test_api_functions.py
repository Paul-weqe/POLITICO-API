"""
File holds tests for the ApiFunctions class in the politico_api.v2.views.api_functions file
This file is used to store functions that are repetitively used by various routes in version 2 of the API
"""
from politico_api.v2.views.api_functions import ApiFunctions
import unittest

class TestRequiredFields(unittest.TestCase):
    """
    Tests for what happens when a field that is mandatory is not present
    Run by the ApiFunctions.test_required_fields() static function
    """

    def test_when_present(self):
        # Tests what happens when all the fields are present
        # the required fields are stored in the 'required_fields' dictionary
        required_fields = {
            "name": "my_name", "surname": "my_surname"
        }
        received_fields = {
            "name": "slks", "surname": "LLLLL"
        }
        response = ApiFunctions.test_required_fields(required_fields, received_fields)

        self.assertEqual(response, None)
    
    def test_when_absent(self):
        # tests what happens when one or more of the required fields are not present
        # the required fields stored in the 'required_fields' dictionary
        required_fields = {
            "name": "my_name", "surname": "my_surname"
        }
        received_fields = {
        }
        response = ApiFunctions.test_required_fields(required_fields, received_fields)

        self.assertEqual(response, "name")

class TestIsInteger(unittest.TestCase):
    """
    Tests for if a specific value is an integer
    Run using the ApiFunctions.check_is_integer static method
    """

    def test_with_valid_input(self):
        # Tests when a valid integer is entered. 
        # The expected output is True
        response = ApiFunctions.check_is_integer(19)

        self.assertEqual(response, True)
    
    def test_with_invalid_input(self):
        # Tests when a string that cannot be converted to an integer is used
        # The expected output is False
        response = ApiFunctions.check_is_integer("po")

        self.assertEqual(response, False)
    
class TestDataType(unittest.TestCase):
    """
    Tests for the required datatypes of a specific field
    e.g if we expect the id to be an integer, then a string should bring an error
    Run using the ApiFunctions.test_data_type() static method

    required_input holds the dictionary with the field name as the key and the field data type as the required data type
    e.g required_input = {"id": int, "name": str}
    """

    def test_correct_datatype(self):
        # tests with all the correct data types
        # name is supposed to be string and age integer. Supposed to return None
        required_input = {
            "name": str, "age": int
        }
        received_input = {
            "name": "Paul", "age": 22
        }

        response = ApiFunctions.test_data_type(required_input, received_input)
        self.assertEqual(response, None)
    
    def test_wrong_datatype(self):
        # test when one or both of the inputs are wrong
        # name is expected to be a string and age integer but we receive a name as an integer and age as a string
        required_input = {
            "name": str, "age": int
        }
        received_input = {
            "name": 1, "age": "Paul"
        }

        response = ApiFunctions.test_data_type(required_input, received_input)
        self.assertEqual("name", response[0])




