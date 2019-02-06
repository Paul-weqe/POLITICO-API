from flask import Blueprint, jsonify, make_response, request
from random import randint
from politico_app.models.party import Party

party_blueprint = Blueprint('party_blueprint', __name__)

@party_blueprint.route("/parties/", strict_slashes=False)
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


@party_blueprint.route("/parties/<partyID>/<partyName>", methods=['PATCH'], strict_slashes=False)
def editParty(partyID, partyName):

    # make sure the partyID is a number(int)
    try:
        partyID = int(partyID)
    except ValueError:
        return make_response(jsonify({
            "status": 404,
            "error": "partyID has to be a number"
        }), 404)
    
    # partyID cannot be 0 or a negative number
    if partyID < 1:
        return make_response(jsonify({
            "status": 404,
            "error": "partyID has to be more than 0"
        }), 404)

    # making sure that the partyName does not contain any special characters
    special_characters = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]
    for character in special_characters:
        if character in partyName:
            return make_response(jsonify({
                "status": 404,
                "error": "partyName cannot contain special characters like @ or $"
            }), 404)

    
    # make sure the party exists before it is edited
    editPartyOutput = Party.editParty(partyID, partyName)
    if editPartyOutput == False:
        return make_response(jsonify({
            "status": 404,
            "error": "cannot find party with ID {}".format(partyID)
        }), 404)
    
    # returns the new values of the party that has been edited as a response
    return make_response(jsonify({
        "status": 200,
        "data": editPartyOutput
    }))

@party_blueprint.route("/parties/<partyID>", methods=['DELETE'], strict_slashes=False)
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

@party_blueprint.route("/parties/<partyID>", strict_slashes=False)
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

@party_blueprint.route("/parties", methods=['POST'], strict_slashes=False)
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
