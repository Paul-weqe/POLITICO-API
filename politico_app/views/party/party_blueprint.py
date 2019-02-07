from flask import Blueprint, jsonify, make_response, request
from random import randint
from politico_app.models.party import PartyModel
from politico_app.views.required_fields import error_dictionary, mandatory_fields

party_blueprint = Blueprint('party_blueprint', __name__, url_prefix="/api/v1")

@party_blueprint.route("/parties/", strict_slashes=False)
def get_all_parties():
    parties = PartyModel.get_all_parties()
    
    return make_response(jsonify({
        "status": 200,
        "data": parties
    }), 200)


@party_blueprint.route("/parties/<partyID>/<partyName>", methods=['PATCH'], strict_slashes=False)
def edit_party(partyID, partyName):

    error_statements = error_dictionary["edit_party"]
    error = None

    # make sure the partyID is a number(int)
    try:
        partyID = int(partyID)
    except ValueError:
        error = error_statements["ID_HAS_TO_BE_NUMBER"]
    
    # partyID cannot be 0 or a negative number
    if partyID < 1 and error == None:
        error = error_statements["ID_HAS_TO_BE_MORE_THAN_ZERO"]

    # making sure that the partyName does not contain any special characters
    special_characters = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]
    for character in special_characters:
        if (character in partyName) and (error == None):
            error = error_statements["NAME_CANNOT_CONTAIN_SPECIAL_CHARACTERS"]
    
    # make sure the party exists before it is edited
    edit_party_output = PartyModel.edit_party(partyID, partyName)
    if edit_party_output == False and error==None:
        error = error_statements["CANNOT_FIND_PARTY"].format(partyID)

    if error != None:
        return make_response(jsonify({
            "status": 404,
            "error": error
        }), 404)

    return make_response(jsonify({
        "status": 200,
        "data": edit_party_output
    }), 200)

@party_blueprint.route("/parties/<partyID>", methods=['DELETE'], strict_slashes=False)
def delete_party(partyID):

    deletePartyOutput = PartyModel.delete_party(int(partyID))

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
def get_single_party(partyID):
    getPartyOutput = PartyModel.get_single_party(int(partyID))

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

    # dictionary of the mandatory fields together with the datatypes that they are required to be of
    create_party_required = mandatory_fields["create_party"]

    for field in create_party_required:

        # checks if any of the mandatory field is absent in the JSON data which will lead to a 404 error
        if field not in json_data:
            return make_response(jsonify({
                "status": 404,
                "error": "'{}' is a mandatory field".format(field)
            }), 404)
        

        # testing for the data type of the fields based on the corresponding value in required_fields dictionary
        elif type(json_data[field]) != create_party_required[field]:
            return make_response(jsonify({
                "status": 404,
                "error": "'{}' field must be a '{}'".format(field, create_party_required[field])
            }), 404)

    # initialize a party using the PartyModel
    party = PartyModel(json_data)
    created_party_output = party.createParty()

    return make_response(jsonify({
        "status": 200,
        "data": [
            created_party_output
        ]
    }), 200)
