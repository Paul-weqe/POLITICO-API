from flask import Blueprint, jsonify, request, make_response

from politico_api.v1.models.office import OfficeModel
from politico_api.v1.views.api_functions import ApiFunctions
from politico_api.v1.views.api_response_data import mandatory_fields, error_dictionary

office_blueprint_v1 = Blueprint('office_blueprint', __name__, url_prefix="/api/v1/offices")

@office_blueprint_v1.route("/<int:office_id>", strict_slashes=False)
def get_single_office(office_id):
    
    # gets all the errors for the get_single_office function
    # this is from the error_dictionary in the required_fields.py
    
    error = None 
    office_obj = OfficeModel()
    office = None
        
    # makes sure the officeID is not less than 1
    office = office_obj.get_single_office(office_id)
        
    if office == None and error == None:
        error = [404, "Could not find office with id {}".format(office_id)]
    
    elif office != None and error == None:
        return make_response(jsonify({
            "status": 200,
            "data": [office]
        }), 200)
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])



@office_blueprint_v1.route("/", strict_slashes=False, methods=['POST'])
def create_office():
    json_data = request.get_json(force=True)

    # get all the errors associated with this function and all the required fields for this office
    # required_fields = mandatory_fields["create_office"]
    required_fields = {
        "office_name": str, "office_type": str
        }

    error = None
    # checks if all the mandatory fields are present
    
    for field in required_fields:
        if field not in json_data:
            error = [400, "'{}' is a mandatory field".format(field)]
            break
        elif type(json_data[field]) != required_fields[field]:
            error = [400, "{} must be a {}".format(field, required_fields[field])]
            break
        
    # the following two lines try and create a new office
    if error == None:
        new_office = OfficeModel(json_data)
        office_info = new_office.create_office()
        
        if office_info == False and error == None:
            error = [400, "the office already exists"]

        elif office_info == None and error == None:
            error = [403, "unable to add office"]
    
    
    # makes sure that the office information has been found and there are no errors so far
    if error == None:
        return make_response(jsonify({
            "status": 201,
            "data": "successfully added office"
        }), 201)
    

    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])
    

@office_blueprint_v1.route("/", strict_slashes=False)
def get_all_offices():
    office = OfficeModel()
    return make_response(jsonify({
        "status": 200, 
        "data": office.get_all_offices()
    }), 200)

