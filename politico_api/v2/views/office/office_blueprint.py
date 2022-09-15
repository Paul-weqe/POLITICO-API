from flask import Blueprint, jsonify, request, make_response
from politico_api.v2.models.models import Office, Candidate
from politico_api.v2.validators import Validate
from politico_api.v2.views.decorators import admin_required, token_required, json_required

office_blueprint_v2 = Blueprint('office_blueprint_v2', __name__, url_prefix="/api/v2/office")

@office_blueprint_v2.route("/<int:office_id>/result", strict_slashes=False)
@token_required
def get_office_results(office_id):
    db = request.args.get("db")
    error = None 
    office_results = None
    
    if error == None:
        office_obj = Office(db=db)
        office_results = office_obj.get_office_results(office_id)
    
    if error == None and office_results == None:
        error = [404, "office with ID {} does not exist".format(office_id)]
    
    office_results_list = []
    if error == None:
        for candidate_info in office_results: 
            result_info = {
                "username": candidate_info[0],
                "votes": candidate_info[1]
            }
            office_results_list.append(result_info)
            
    if error == None:
        return make_response(jsonify({
            "status": 200,
            "results": office_results_list
        }), 200)
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])

@office_blueprint_v2.route("/", methods=['POST'], strict_slashes=False)
@admin_required
@json_required
def create_office():
    db = request.args.get('db')
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
            error = [400, "{} must be a {}".format(field, required_fields[field])]
            break

        elif Validate.validate_field(json_data[field]) != True:
            validation_message = Validate.validate_field(json_data[field])
            error = [400, validation_message.format(field)]
            break

    if error == None and json_data["office_type"] not in office_types:
        error_message = "office_type has to be one of: 'federal', 'legislative', 'state' or 'local_government' not {}".format(json_data["office_type"])
        error = [404, error_message]
    
    if error == None:
        office = Office(office_name=json_data["office_name"], office_type=json_data["office_type"], db=db)
        office_created = office.create_office()
    
    if error == None and office_created == None:
        error = [404, "an office with these parameters already exists"]
    
    if error == None and office_created == True:
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
    db = request.args.get("db")
    office_conn = Office(db=db)
    all_offices = office_conn.get_all_offices()
    
    print(request.content_type)

    all_offices_list = []

    for office in all_offices:
        office_info = { "office_id": office[0], "office_name": office[1], "office_type": office[2] }
        all_offices_list.append(office_info)


    return make_response(jsonify({
        "status": 200,
        "offices": all_offices_list
    }), 200)


@office_blueprint_v2.route("/<int:office_id>/register", methods=['POST'], strict_slashes=False)
@json_required
@admin_required
def create_candidate(office_id):
    db = request.args.get("db")
    required_fields = {
        "candidate_username": str, "party_name": str
    }
    json_data = request.get_json()
    error = None
    
    for field in required_fields:
        if field not in json_data:
            error = [403, "Field {} is a mandatory field".format(field)]
            break

        elif required_fields[field] != type(json_data[field]):
            error = [403, "Field {} must be of type {}".format(field, required_fields[field])]
            break

        elif required_fields[field] == str and Validate.validate_field(json_data[field]) != True:
            validate_message = Validate.validate_field(json_data[field])
            error = [400, validate_message.format(field)]
            break
        
    if error == None:
        
        candidate = Candidate(db=db)
        response = candidate.create_candidate_by_name(json_data["candidate_username"], json_data["party_name"], office_id)
        if response == True:
            return make_response(jsonify({
                "message": "Candidate successfully created",
                "status": 201
            }), 201)
        error = [400, response]
        
    
    if error == None:
        error = [400, "unable to create the user"]
    
    return make_response(jsonify({
        "error": error[1],
        "status": error[0]
    }), error[0])

@office_blueprint_v2.route("/<int:office_id>", strict_slashes=False)
def get_office_by_id(office_id):
    db = request.args.get("db")
    office = Office(db=db)
    office_information = office.get_office_by_id(office_id)
    
    if office_information == None:
        return make_response(jsonify({
            "status": 404,
            "error": "Office with ID {} could not be found".format(office_id)
        }), 404)

    info_dict = {"id": office_information[0], "office name": office_information[1], "office type": office_information[2]}
    return make_response(jsonify({
        "status": 200,
        "office info": info_dict
    }), 200)

@office_blueprint_v2.route("/<office_name>", strict_slashes=False)
def get_office_by_name(office_name):
    db = request.args.get("db")
    office_info = Office(db=db).get_office_by_name(office_name)
    
    if office_info == None:
        return make_response(jsonify({
            "status": 404,
            "error": "Office with name {} could not be found".format(office_name)
        }), 404)
    
    info_dict = {"id": office_info[0], "office name": office_info[1], "office type": office_info[2]}
    return make_response(jsonify({
        "status": 200,
        "office info": info_dict
    }), 200)
