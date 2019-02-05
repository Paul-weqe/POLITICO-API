from flask import Blueprint, jsonify, make_response, request
from random import randint
from politico_data import political_parties

party_blueprint = Blueprint('party_blueprint', __name__)

@party_blueprint.route("/parties/")
def getAllParties():
    return make_response(jsonify({
        "status": 200,
        "data": [
            political_parties
        ]
    }), 200)

@party_blueprint.route("/parties/<partyID>/<partyName>", methods=['PATCH'])
def editParty(partyID, partyName):

    for party in political_parties:
        if party["id"] == int(partyID):
            party["name"] = partyName
            return make_response(jsonify({
                "status": 200, 
                "data": [{
                    "id": party["id"],
                    "name": party["name"]
                }]
            }), 200)
    
    return make_response(jsonify({
        "status": 404,
        "error": "could not find party with ID {}".format(partyID)
    }), 200)

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


@party_blueprint.route("/parties", methods=['POST'])
def create_party():
    json_data = request.get_json(force=True)
    required_fields = {
        "party_name": str, 
        "party_hq_address": str, 
        "party_logo_url": str, 
        "party_motto": str, 
        "party_members": int
    }

    for field in required_fields:
        if field not in json_data:
            return make_response(jsonify({
                "status": 404,
                "error": "'{}' is a mandatory field".format(field)
            }), 404)
    
    new_party_id = randint(1, 100)
    new_party_name = json_data["party_name"]
    new_party_hq_address = json_data["party_hq_address"]
    new_party_logo_url = json_data["party_logo_url"]
    new_party_motto = json_data["party_motto"]
    new_party_members = json_data["party_members"]

    new_party = {
        "id": new_party_id, "name": new_party_name, "hqAddress": new_party_hq_address, 
        "logoUrl": new_party_logo_url, "motto": new_party_motto, "members": new_party_members
    }
    political_parties.append(new_party)

    return make_response(jsonify({
        "status": 404, 
        "data": [{
            "id": new_party_id,
            "name": new_party_name
        }]
    }), 200)
