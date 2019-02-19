from politico_api.v2.views.jtw_decorators import token_required
from flask import Blueprint, request, jsonify, make_response
from politico_api.v2.models.models import Petition

peition_blueprint_v2 = Blueprint('petition_blueprint_v2', __name__, url_prefix="/api/v2/petitions")


# create a new petition
@peition_blueprint_v2.route("/", methods=["POST"], strict_slashes=False)
@token_required
def create_petition():
    json_data = request.get_json()
    required_fields = {
        "created_by": int, "office": int, "body": str 
    }
    error = None
    create_petition_response = None

    for field in required_fields:
        if field not in json_data:
            error = [400, "{} is a required field".format(field)]
            break
        elif required_fields[field] != type(json_data[field]):
            error = [400, "{} must be a {}".format(field, required_fields[field])]
            break
    
    if error == None:
        petition = Petition(json_data["created_by"], json_data["office"], json_data["body"])
        create_petition_response = petition.create_petition()

        if create_petition_response == False:
            error = [500, "There is a problem on our side. We will be back to you shortly"]
        elif create_petition_response == None:
            error = [417, "User with ID {} has already filed a petition for office {}".format(json_data["created_by"], json_data["office"])]
    
    if error == None:
        return make_response(jsonify({
            "status": 201,
            "message": "petition successfully created"
        }), 201)
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])
    