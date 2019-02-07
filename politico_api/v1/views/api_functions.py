
class ApiFunctions:

    # this method checks for the presence of the mandatory fields in specific input data
    # both the required_input and received_input will be dictionaries
    @staticmethod
    def test_required_fields(required_input, received_input):
        for input_data in required_input:
            if input_data not in received_input:
                return input_data
        return True

    # this method checks if all the data in the required input has the same data type as it's corresponding values in received_input
    # both will be dictionaries. 
    @staticmethod
    def test_data_type(required_input, received_input):
        for input_data in received_input:
            if type(received_input[input_data]) != required_input[input_data]:
                return [input_data, required_input[input_data]]
        
        return True
    
    # checks for the presence of special characters in any string
    # this may be useful when trying to generate or filter words and do not need special characters
    @staticmethod
    def check_for_special_characters(string_input):
        special_characters = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "[", "]"]
        
        for character in special_characters:
            if character in string_input:
                return True
        return False
    
    # checks for an item to be an integer
    # useful when checking for values that have been entered as the ID of an item and one may have input a string
    @staticmethod
    def check_is_integer(string_input):
        try:
            int(string_input)
            return True
        except ValueError:
            return False
    