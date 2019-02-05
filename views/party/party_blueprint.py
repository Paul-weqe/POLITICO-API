from flask import Blueprint, make_response, jsonify, request
from politico_data import political_parties

party_blueprint = Blueprint('flask_blueprint', __name__)

@party_blueprint.route("/parties/<partyID>", methods=['DELETE'])
def deleteParty(partyID):

    for party in political_parties:
        if party["id"] == int(partyID):
            message = "successfullly deleted {}".format(party)
            political_parties.remove(party)
            return make_response(jsonify({
                "status": 200,
                "data": message
            }), 200)
    
    return make_response(jsonify({
        "status": 404, "error": "unable to find party with ID {}".format(partyID)
    }), 404)

@party_blueprint.route("/parties/<partyID>")
def getSingleParty(partyID):

    for party in political_parties:
        if int(partyID) == party["id"]:
            return make_response(jsonify({
                    "status": 200,
                    "data": [party]
                }), 200)
    
    return make_response(jsonify({
        "status": 404,
        "error": "could not find party with ID {}".format(partyID)
    }), 404)

