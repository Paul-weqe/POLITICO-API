
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