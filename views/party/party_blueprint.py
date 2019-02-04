from flask import Flask, jsonify, make_response, Blueprint
from politico_data import political_parties

party_blueprint = Blueprint('party_blueprint', __name__)

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


