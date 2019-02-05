from flask import Blueprint, jsonify, make_response, request
from random import randint
from politico_app.politico_data import political_parties
from politico_app.models.party import Party

party_blueprint = Blueprint('party_blueprint', __name__)

@party_blueprint.route("/parties/")
def getAllParties():
    parties = Party.getAllParties()
    
    if parties == None:
        return make_response(jsonify({
            "status": 404,
            "error": "request failed"
        }), 404)
    
    return make_response(jsonify({
        "status": 200,
        "data": parties
    }), 200)


@party_blueprint.route("/parties/<partyID>/<partyName>", methods=['PATCH'])
def editParty(partyID, partyName):

    editPartyOutput = Party.editParty(int(partyID), partyName)
    
    if editPartyOutput == None:
        return make_response(jsonify({
            "status": 404,
            "error": "cannot find party with ID {}".format(partyID)
        }), 404)
    
    return make_response(jsonify({
        "status": 200,
        "data": editPartyOutput
    }))

@party_blueprint.route("/parties/<partyID>", methods=['DELETE'])
def deleteParty(partyID):

    deletePartyOutput = Party.deleteParty(int(partyID))

    if not deletePartyOutput:
        return make_response(jsonify({
            "status": 404, 
            "error": "unable to delete party with ID {}".format(partyID) 
        }), 404)
    
    return make_response(jsonify({
        "status": 200,
        "data": "successfully deleted"
    }), 200)

@party_blueprint.route("/parties/<partyID>")
def getSingleParty(partyID):
    getPartyOutput = Party.getSingleParty(int(partyID))

    if getPartyOutput == False:
        return make_response(jsonify({
            "status": 404,
            "erorr": "unable to find party with ID {}".format(partyID)
        }), 404)
    
    return make_response(jsonify({
        "status": 200,
        "data": [ getPartyOutput ]
    }), 200)

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

    party = Party(new_party_name, new_party_hq_address, new_party_logo_url)
    createPartyOutput = party.createParty()

    return make_response(jsonify({
        "status": 200,
        "data": [
            createPartyOutput
        ]
    }), 200)
