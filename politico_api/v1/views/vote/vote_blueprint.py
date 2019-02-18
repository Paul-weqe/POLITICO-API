from flask import Blueprint, request, make_response, jsonify
from politico_api.v1.models.user import UserModel
from politico_api.v1.models.vote import VoteModel


vote_blueprint_v1 = Blueprint('vote_blueprint_v1', __name__, url_prefix="/api/v1/votes")

@vote_blueprint_v1.route("/new-vote", methods=["POST"])
def new_vote():
    json_data = request.get_json()
    required_fields = {
        "position": str, "voter_id": int, "candidate_id": int
    }
    user = UserModel()
    error = None 
    voter_info = None 
    candidate_info = None
    vote_inserted = None

    for field in required_fields:
        if field not in json_data:
            error = [400, "{} is a mandatory field".format(field)]
            break 
        elif type(json_data[field]) != required_fields[field]:
            error = [400, "{} must be a {}".format(field, required_fields[field])]
            break
    

    if error == None:
        voter_info = user.get_single_user(int(json_data["voter_id"]))
        candidate_info = user.get_single_user(int(json_data["candidate_id"]))

    if voter_info == None and error == None:
        error = [404, "Cannot find voter with ID {}".format(json_data["voter_id"])]
    elif candidate_info == None and error == None:
        error = [404, "Cannot find voter with ID {}".format(json_data["candidate_id"])]
    
    if error == None:
        vote = VoteModel(voter_info=voter_info, candidate_info=candidate_info, position=json_data["position"])
        vote_inserted = vote.insert_vote()
        if vote_inserted == None and error == None:
            error = [400, "the user {} has already voted for position {}".format(json_data["voter_id"], json_data["position"])]

    if vote_inserted and error == None:
        return make_response(jsonify({
            "status": 200,
            "data": "{} voted for {}".format(voter_info["username"], candidate_info["username"])
        }), 200)
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])

@vote_blueprint_v1.route("/", strict_slashes=False)
def get_all_votes():
    vote_model = VoteModel()
    return make_response(jsonify({
        "status": 200,
        "data": vote_model.get_all_votes()
    }), 200)
