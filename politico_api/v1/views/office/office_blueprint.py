from flask import Blueprint, jsonify, request, make_response

from politico_api.v1.models.office import OfficeModel
from politico_api.v1.views.api_functions import ApiFunctions
from politico_api.v1.views.api_response_data import mandatory_fields, error_dictionary

office_blueprint_v1 = Blueprint('office_blueprint', __name__, url_prefix="/api/v1/offices")

@office_blueprint_v1.route("/<officeID>", strict_slashes=False)
def get_single_office(officeID):
    
    # gets all the errors for the get_single_office function
    # this is from the error_dictionary in the required_fields.py
    errors = error_dictionary["get_single_office"]
    error = None 
    office = None 

    if not ApiFunctions.check_is_integer(officeID):
        return make_response(jsonify({
            "status": 406, 
            "error": "office id must be an integer"
        }), 406)

    if ApiFunctions.check_is_integer(officeID) == False:
        error = "you must enter a real number at officeID in '/offices/<officeID>'"
        
    # makes sure the officeID is not less than 1
    elif int(officeID) < 1:
        error = "officeID cannot be zero or a negative number"
    
    else:
        office = OfficeModel.get_single_office(int(officeID))
    

    if office != None and error == None:
        return make_response(jsonify({
            "status": 200,
            "data": [office]
        }), 200)
    
    elif office == None and error == None:
        error = "Could not find office with id {}".format(officeID)
    
    return make_response(jsonify({
        "status": 406,
        "error": error
    }), 406)



@office_blueprint_v1.route("/", strict_slashes=False, methods=['POST'])
def create_office():
    json_data = request.get_json(force=True)

    # get all the errors associated with this function and all the required fields for this office
    required_fields = mandatory_fields["create_office"]
    create_office_errors = error_dictionary["create_office"]
    error = None
    
    # checks if all the mandatory fields are present
    is_data_type_wrong = None
    
    for field in required_fields:
        if field not in json_data:
            error = "'{}' is a mandatory field".format(field)

    if error == None:
        # checks for the data type of the fields that have been confirmed to be present
        # checks the required fields against the json_data that has been received
        is_data_type_wrong = ApiFunctions.test_data_type(required_fields, json_data)
        
        if is_data_type_wrong != None and error == None:
            # this is done since the ApiFunctions.test_data_type() returns the field whose data type is not correct, 
            # and this is stored in the data_type_correct variable, this will be used to format the message output
            error = "Field '{}' has to be a '{}'".format(is_data_type_wrong[0], is_data_type_wrong[1])
    
    if error != None:
        return make_response(jsonify({
            "status": 406,
            "data": error,
        }), 406)
        
    # the following two lines try and create a new office
    new_office = OfficeModel(json_data)
    office_info = new_office.create_office()

    # makes sure that the office information has been found and there are no errors so far
    if office_info != None and error == None:
        return make_response(jsonify({
            "status": 200,
            "data": [office_info]
        }), 200)
    
    error = "unable to add office"
    return make_response(jsonify({
        "status": 406,
        "error": error
    }), 406)
    

@office_blueprint_v1.route("/", strict_slashes=False)
def get_all_offices():
    return make_response(jsonify({
        "status": 200, 
        "data": OfficeModel.get_all_offices()
    }), 200)


