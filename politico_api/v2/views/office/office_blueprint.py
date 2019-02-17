from flask import Blueprint, jsonify, request, make_response
from politico_api.v2.models.models import Office
from politico_api.v2.views.jtw_decorators import token_required

office_blueprint_v2 = Blueprint('office_blueprint_v2', __name__, url_prefix="/api/v2/offices")

@office_blueprint_v2.route("/get-office-results/", strict_slashes=False)
def get_office_results():

    error = None 
    json_data = request.get_json()
    office_results = None 

    if "office_id" not in json_data:
        error = [400, "office_id is a mandatory field"]
        
    elif type(json_data["office_id"]) != int:
        error = [400, "office_id must be an integer"]
    
    
    if error == None:
        office_obj = Office()
        office_results = office_obj.count_office_votes(json_data["office_id"])
    
    if error == None and office_results == None:
        error = [404, "office with ID {} does not exist".format(json_data["office_id"])]

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
@token_required
def create_office():

    required_fields = {
        "office_name": str, "office_type": str
    }
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
    
    if error == None:
        office = Office(office_name=json_data["office_name"], office_type=json_data["office_type"])
        office_created = office.create_office()
    
    if error == None and office_created == None:
        error = [404, "an office with these parameters already exists"]
    
    if error == None:
        return make_response(jsonify({
            "status": 201,
            "data": "office successfully created"
        }), 201)
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])

@office_blueprint_v2.route("/", strict_slashes=False)
@token_required
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
