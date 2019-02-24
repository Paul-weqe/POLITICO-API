from politico_api.v2.views.decorators import token_required, json_required
from flask import Blueprint, request, jsonify, make_response
from politico_api.v2.models.models import Petition
from politico_api.v2.validators import Validate
import jwt
import os

peition_blueprint_v2 = Blueprint('petition_blueprint_v2', __name__, url_prefix="/api/v2/petitions")


# create a new petition
@peition_blueprint_v2.route("/", methods=["POST"], strict_slashes=False)
@token_required
@json_required
def create_petition():
    db = request.args.get("db")
    json_data = request.get_json()
    required_fields = {
        "office": int, "body": str 
    }
    error = None
    create_petition_response = None

    token = request.headers["Authorization"].split(" ")[1]
    jwt_data = jwt.decode(token, os.getenv('SECRET_KEY'))
    user_id = jwt_data["user_id"]

    
    for field in required_fields:
        if field not in json_data:
            error = [400, "{} is a required field".format(field)]
            break

        elif required_fields[field] != type(json_data[field]):
            error = [400, "{} must be a {}".format(field, required_fields[field])]
            break

    

    if error == None:
        petition = Petition(user_id, json_data["office"], json_data["body"], db=db)
        create_petition_response = petition.create_petition()

        if create_petition_response == False:
            error = [500, "There is a problem on our side. We will be back to you shortly"]
        elif type(create_petition_response) == str:
            error = [404, create_petition_response] 
        elif create_petition_response == None:
            error = [409, "User with ID {} has already filed a petition for office {}".format(json_data["created_by"], json_data["office"])]
    
    if error == None:
        return make_response(jsonify({
            "status": 201,
            "message": "petition successfully created"
        }), 201)
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])
    