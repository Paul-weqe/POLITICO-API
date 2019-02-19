from flask import Blueprint, jsonify, request, make_response
from politico_api.v2.models.models import Office
from politico_api.v2.views.jtw_decorators import token_required
from politico_api.v2.views.api_functions import ApiFunctions
from politico_api.v2.validators import Validate
from politico_api.v2.views.jtw_decorators import admin_required, token_required

office_blueprint_v2 = Blueprint('office_blueprint_v2', __name__, url_prefix="/api/v2/offices")

@office_blueprint_v2.route("/get-office-results/<office_id>", strict_slashes=False)
@token_required
def get_office_results(office_id):
    error = None 
    office_results = None
    if not ApiFunctions.check_is_integer(office_id):
        error = [400, "office_id must be an integer"]
    
    
    if error == None:
        office_obj = Office()
        office_results = office_obj.count_office_votes(office_id)
    
    if error == None and office_results == None:
        error = [404, "office with ID {} does not exist".format(office_id)]
    
    if error == None:
        return make_response(jsonify({
            "status": 200,
            "data": office_results
        }), 200)

    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])

@office_blueprint_v2.route("/", methods=['POST'], strict_slashes=False)
@admin_required
def create_office():

    required_fields = {
        "office_name": str, "office_type": str
    }
    office_types = ["federal", "legislative", "state", "local_government"]

    json_data = request.get_json()
    error = None
    office_created = None

    for field in required_fields:
        if field not in json_data:
            error = [400, "{} is a mandatory field".format(field)]
            break

        elif type(json_data[field]) != required_fields[field]:
            error = [400, "{} must be a {}".format(request, required_fields[field])]
            break

        elif Validate.validate_field(json_data[field]) != True:
            validation_message = Validate.validate_field(json_data[field])
            error = [400, validation_message.format(field)]
            break

    if error == None and json_data["office_type"] not in office_types:
        error_message = "office_type has to be one of: 'federal', 'legislative', 'state' or 'local_government' not {}".format(json_data["office_type"])
        error = [404, error_message]
    
    if error == None:
        office = Office(office_name=json_data["office_name"], office_type=json_data["office_type"])
        office_created = office.create_office()
    
    if error == None and office_created == None:
        error = [404, "an office with these parameters already exists"]
    
    if error == None:
        return make_response(jsonify({
            "status": 201,
            "data": "office {} successfully created".format(json_data["office_name"])
        }), 201)
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])

@office_blueprint_v2.route("/", strict_slashes=False)
def get_all_offices():
    office_conn = Office()
    all_offices = office_conn.get_all_offices()

    if not all_offices:
        return make_response(jsonify({
            "status": 500,
            "message": "The error is on our side. We will be back to you shortly"
        }), 500)
    
    return make_response(jsonify({
        "status": 200,
        "data": all_offices
    }), 200)
