from flask import Blueprint, request, jsonify, make_response
from politico_api.v2.models.models import Vote
from politico_api.v2.views.decorators import token_required, json_required
import jwt
import os

votes_blueprint_v2 = Blueprint('vote_blueprint_v2', __name__, url_prefix="/api/v2/votes")

@votes_blueprint_v2.route("/", methods=["POST"], strict_slashes=False)
@token_required
@json_required
def cast_vote():

    json_data = request.get_json()
    required_fields = {
        "candidate_id": int, "office_id": int
    }
    token = request.headers['Authorization'].split(' ')[1]
    jwt_data = jwt.decode(token, os.getenv('SECRET_KEY'))
    user_id = jwt_data["user_id"]
    db = request.args.get("db")
    
    error = None
    vote_inserted = None 
    
    # checks for all the fields that are mandatory
    for field in required_fields:
        if field not in json_data:
            error = [400, "{} is a mandatory field".format(field)]
        elif required_fields[field] != type(json_data[field]):
            error = [400, "{} must be a {}".format(field, required_fields[field])]
    
    
    if error == None:
        vote = Vote( voter_id=user_id, candidate_id=json_data["candidate_id"], office_id=json_data["office_id"], db=db)
        vote_inserted = vote.create_vote()
    
    # # checks for the candidates presence
    if vote_inserted == "Unable to find the candidate" and error == None:
        error = [404, "candidate could not be found"]
    
    elif vote_inserted == False and error == None:
        error = [500, "The problem is on our side"]
    
    # # vote_inserted returns "already voted" in case the user had already voted for a particular position
    elif vote_inserted == "already voted" and error == None:
        # TODO check for the correct status number on this
        error = [400, "user {} has already voted for that office".format(user_id)]
    
    if error == None:
        return make_response(jsonify({
            "status": 201,
            "data": "successfully casted your vote..."
        }), 201)

    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])
