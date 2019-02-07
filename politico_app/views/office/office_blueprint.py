
from flask import Blueprint, jsonify, request, make_response
from random import randint
from politico_app.models.office import Office
from politico_app.views.api_functions import ApiFunctions
from politico_app.views.required_fields import mandatory_fields, error_dictionary

office_blueprint = Blueprint('office_blueprint', __name__, url_prefix="/api/v1")

@office_blueprint.route("/offices/", strict_slashes=False, methods=['POST'])
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
        if data_types_correct != True:
            # this is done since the ApiFunctions.test_data_type() returns the field whose data type is not correct, 
            # and this is stored in the data_type_correct variable, this will be used to format the message output
            if error == None: 
                error = create_office_errors["WRONG_DATA_TYPE"].format(data_types_correct[0], data_types_correct[1])

    else:
        # since the test_required fields returns the item that is mandatory and is not present in our data
        # the error will be the required field is mandatory in the requested body
        if error == None: 
            error = create_office_errors["MANDATORY_FIELD"].format(required_fields_present)

    if error != None:
        return make_response(jsonify({
            "status": 404,
            "error": error
        }), 404)

    office_type = json_data["office_type"]
    office_name = json_data["office_name"]
    
    new_office = Office(office_name, office_type)
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
        "status": 404,
        "error": error
    }))

@office_blueprint.route("/offices", strict_slashes=False)
def getAllOffices():
    office = Office.get_all_offices()
    return make_response(jsonify({
        "status": 200,
        "data": office
    }), 200)


@office_blueprint.route("/offices/<officeID>", strict_slashes=False)
def getSingleOffice(officeID):
    
    # gets all the errors for the get_single_office function
    # this is from the error_dictionary in the required_fields.py
    errors = error_dictionary["get_single_office"]
    error = None 

    try:
        officeID = int(officeID)

    except ValueError:
        error = errors["OFFICEID_MUST_BE_REAL_NUMBER"]

    # makes sure the officeID is not less than 1
    if error == None and int(officeID) < 1:
        error = errors["OFFICEID_CANNOT_BE_ZERO_OR_NEGATIVE"]
    
    office = Office.get_single_office(officeID)

    # returns true if the office is found
    if error == None and office != None:
        return make_response(jsonify({
            "status": 200,
            "data": office
        }), 200)
    
    elif error == None:
        error = errors["COULD_NOT_FIND_OFFICE"].format(officeID)

    return make_response(jsonify({
        "status": 404,
        "error": error
    }), 404)
    
