from flask import Blueprint, request, jsonify, make_response
from politico_api.v2.views.jtw_decorators import token_required
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
            error = [400, "{} is a required field"]
            break
        elif required_fields[field] != type(json_data[field]):
            error = [400, "{} must be a {}".format(field, required_fields[field])]
            break
    
    if error == None:
        petition = Petition(json_data["created_by"], json_data["office"], json_data["body"])
        create_petition_response = petition.create_petition()

        if not create_petition_response:
            error = [500, "There is a problem on our side. We will be back to you shortly"]
    
    if error == None:
        return make_response(jsonify({
            "status": 200,
            "message": "petition successfully created"
        }), 200)
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])
    