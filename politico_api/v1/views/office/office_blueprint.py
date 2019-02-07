from flask import Blueprint, jsonify, request, make_response
from politico_api.v1.models.office import OfficeModel
from politico_api.v1.views.api_functions import ApiFunctions
from politico_api.v1.views.api_response_data import mandatory_fields, error_dictionary

office_blueprint_v1 = Blueprint('office_blueprint', __name__, url_prefix="/api/v1")

@office_blueprint_v1.route("/offices/", strict_slashes=False, methods=['POST'])
def create_office():
    json_data = request.get_json(force=True)

    create_office_required_fields = mandatory_fields["create_office"]
    create_office_errors = error_dictionary["create_office"]
    error = None 
    
    # checks if all the mandatory fields are present
    required_fields_present = ApiFunctions.test_required_fields(create_office_required_fields, json_data)
    data_types_correct = None
    
    
    if required_fields_present == True:
        # checks for the data type of the fields that have been confirmed to be present
        data_types_correct = ApiFunctions.test_data_type(create_office_required_fields, json_data)
        if data_types_correct != True and error == None:
            # this is done since the ApiFunctions.test_data_type() returns the field whose data type is not correct, 
            # and this is stored in the data_type_correct variable, this will be used to format the message output
            error = create_office_errors["WRONG_DATA_TYPE"].format(data_types_correct[0], data_types_correct[1])
            
    elif error == None: 
            error = create_office_errors["MANDATORY_FIELD"].format(required_fields_present)

    if error != None:
        return make_response(jsonify({
            "status": 406,
            "error": error
        }), 406)
        
    new_office = OfficeModel(json_data)
    office_info = new_office.create_office()

    # makes sure that the office information has been found and there are no errors so far
    if office_info != None and error == None:
        return make_response(jsonify({
            "status": 200,
            "data": [
                office_info
                ]
            }), 200)
    
    error = create_office_errors["UNABLE_TO_ADD_OFFICE"]
    return make_response(jsonify({
        "status": 406,
        "error": error
    }), 406)

@office_blueprint_v1.route("/offices", strict_slashes=False)
def get_all_offices():
    office = OfficeModel.get_all_offices()
    return make_response(jsonify({
        "status": 200,
        "data": office
    }), 200)


@office_blueprint_v1.route("/offices/<officeID>", strict_slashes=False)
def get_single_office(officeID):
    
    # gets all the errors for the get_single_office function
    # this is from the error_dictionary in the required_fields.py
    errors = error_dictionary["get_single_office"]
    office = OfficeModel.get_single_office(officeID)
    error = None 

    if ApiFunctions.check_is_integer(officeID) == False:
        error = errors["OFFICEID_MUST_BE_REAL_NUMBER"]
        print("STEP1")
    
    # makes sure the officeID is not less than 1
    elif int(officeID) < 1:
        error = errors["OFFICEID_CANNOT_BE_ZERO_OR_NEGATIVE"]
        print("STEP2")
    
    # office = Office.get_single_office(officeID)
    elif office != None:
        return make_response(jsonify({
            "status": 200,
            "data": office
        }), 200)
        print("STEP3")
    
    if error == None : error =  ApiFunctions.check_error_if_item_is_true(office, None, error, errors["COULD_NOT_FIND_OFFICE"].format(officeID)) 

    print(error)
    return make_response(jsonify({
        "status": 406,
        "error": error
    }), 406)
    
