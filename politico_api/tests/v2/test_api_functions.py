from politico_api.v2.views.api_functions import ApiFunctions
import unittest

class TestRequiredFields(unittest.TestCase):

    def test_when_present(self):
        required_fields = {
            "name": "my_name", "surname": "my_surname"
        }
        received_fields = {
            "name": "slks", "surname": "LLLLL"
        }
        response = ApiFunctions.test_required_fields(required_fields, received_fields)

        self.assertEqual(response, None)
    
    def test_when_absent(self):
        required_fields = {
            "name": "my_name", "surname": "my_surname"
        }
        received_fields = {
        }
        response = ApiFunctions.test_required_fields(required_fields, received_fields)

        self.assertEqual(response, "name")

class TestIsInteger(unittest.TestCase):
    
    def test_with_valid_input(self):
        response = ApiFunctions.check_is_integer(19)

        self.assertEqual(response, True)
    
    def test_with_invalid_input(self):
        response = ApiFunctions.check_is_integer("po")

        self.assertEqual(response, False)
    
class TestDataType(unittest.TestCase):

    def test_correct_datatype(self):
        required_input = {
            "name": str, "age": int
        }
        received_input = {
            "name": "Paul", "age": 22
        }

        response = ApiFunctions.test_data_type(required_input, received_input)
        self.assertEqual(response, None)
    
    def test_wrong_datatype(self):
        required_input = {
            "name": str, "age": int
        }
        received_input = {
            "name": 1, "age": "Paul"
        }

        response = ApiFunctions.test_data_type(required_input, received_input)
        self.assertEqual("name", response[0])




