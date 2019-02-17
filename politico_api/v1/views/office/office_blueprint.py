from flask import Blueprint, jsonify, request, make_response

from politico_api.v1.models.office import OfficeModel
from politico_api.v1.views.api_functions import ApiFunctions
from politico_api.v1.views.api_response_data import mandatory_fields, error_dictionary

office_blueprint_v1 = Blueprint('office_blueprint', __name__, url_prefix="/api/v1/offices")

@office_blueprint_v1.route("/<officeID>", strict_slashes=False)
def get_single_office(officeID):
    
    # gets all the errors for the get_single_office function
    # this is from the error_dictionary in the required_fields.py
    
    error = None 
    office_obj = OfficeModel()
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
        office = office_obj.get_single_office(int(officeID))

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
    required_fields = {
        "office_name": str, "office_type": str
    }

    # get all the errors associated with this function and all the required fields for this office
    # required_fields = mandatory_fields["create_office"]
    error = None
    
    

    # checks if the field is mandatory then checks for the datatype of the field
    for field in required_fields:
        if field not in json_data:
            error = [400, "'{}' is a mandatory field".format(field)]
            break
        elif type(json_data[field]) != required_fields[field]:
            error = [400, "'{}' must be a {}".format(field, required_fields[field])]
            break

    
    # the following two lines try and create a new office
    new_office = OfficeModel(json_data)
    office_info = new_office.create_office()

    # makes sure that the office information has been found and there are no errors so far
    if office_info != None and error == None:
        return make_response(jsonify({
            "status": 200,
            "data": [office_info]
        }), 200)
    
    if error == None:
        error = [400, "unable to add office"]
    
    if error != None:
        return make_response(jsonify({
            "status": error[0],
            "data": error[1],
        }), error[0])
        

@office_blueprint_v1.route("/", strict_slashes=False)
def get_all_offices():
    office = OfficeModel()
    return make_response(jsonify({
        "status": 200, 
        "data": office.get_all_offices()
    }), 200)


