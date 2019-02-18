from flask import Blueprint, jsonify, make_response, request
from random import randint
from politico_api.v1.models.party import PartyModel
from politico_api.v1.views.api_response_data import error_dictionary, mandatory_fields
from politico_api.v1.views.api_functions import ApiFunctions

party_blueprint_v1 = Blueprint('party_blueprint', __name__, url_prefix="/api/v1/parties")

@party_blueprint_v1.route("/", strict_slashes=False)
def get_all_parties():
    party = PartyModel()
    return make_response(jsonify({
        "status": 200,
        "data": party.get_all_parties()
    }), 200)

@party_blueprint_v1.route("/<int:partyID>", methods=['PATCH'], strict_slashes=False)
def edit_party(partyID):

    edit_party_response = None 
    json_data = request.get_json()
    party_name = json_data["party_name"]

    error = None
    
    # partyID cannot be 0 or a negative number
    if partyID < 1 and error == None:
        error = [400, "partyID has to be more than 0"]

    # make sure the party exists before it is edited
    # edit_party_output will return False if the party does not exist but will return the party details after editing if the party exists
    
    else:
        party = PartyModel()
        edit_party_response = party.edit_party(int(partyID), party_name)
    
    if edit_party_response == False and error == None:
        error = [404, "cannot find party with ID {}".format(partyID)]

    if error != None:
        return make_response(jsonify({
            "status": error[0],
            "error": error[1]
        }), error[0])

    
    return make_response(jsonify({
        "message": "successfully edited party",
        "status": 200, "data": [edit_party_response]
    }), 200)


@party_blueprint_v1.route("/<int:partyID>", methods=['DELETE'], strict_slashes=False)
def delete_party(partyID):

    error = None 
    party = PartyModel()

    if partyID < 1:
        error = [400, "partyID cannot be 0 or a negative number"]

    # deletePartyOutput = PartyModel.delete_party(int(partyID))
    elif party.delete_party(int(partyID)) == False:
        error = [404, "unable to find party with ID {}".format(partyID)]

    if error != None:
        return make_response(jsonify({
            "status": error[0],
            "error": error[1]
        }), error[0])

    return make_response(jsonify({
        "status": 200,
        "data": "successfully deleted"
    }), 200)
    

@party_blueprint_v1.route("/<partyID>", strict_slashes=False)
def get_single_party(partyID):
    
    error = None 
    get_party_output=None
    party = PartyModel()

    if not ApiFunctions.check_is_integer(partyID):
        error = [400, "partyID must be an integer"]
    
    else:
        get_party_output = party.get_single_party(int(partyID))
    

    if get_party_output == None and error == None:
        error = [404, "unable to find party with ID {}".format(partyID)]
    
    if error != None:
        return make_response(jsonify({
            "status": error[0],
            "error": error[1]
        }), error[0])
    
    return make_response(jsonify({
        "status": 200,
        "data": [get_party_output]
    }), 200)


@party_blueprint_v1.route("/", methods=['POST'], strict_slashes=False)
def create_party():
    json_data = request.get_json(force=True)

    # dictionary of the mandatory fields together with the datatypes that they are required to be of
    create_party_required = {
        "party_name": str, 
        "party_hq_address": str, 
        "party_logo_url": str, 
        "party_motto": str, 
        "party_members": int
    }
    error = None
    created_party_output = None
    
    for field in create_party_required:

        # checks if any of the mandatory field is absent in the JSON data which will lead to a 404 error
        if field not in json_data:
            error = [400, "'{}' is a mandatory field".format(field)]
            break 

        # testing for the data type of the fields based on the corresponding value in required_fields dictionary
        elif type(json_data[field]) != create_party_required[field]:
            error = [400, "'{}' field must be a {}".format(field, create_party_required[field])]
            break
            
    # initialize a party using the PartyModel
    
    if error == None:
        party = PartyModel(json_data)
        created_party_output = party.createParty()
        if created_party_output == None:
            error = [400, "Party with name {} has already been created".format(json_data["party_name"])]

    if created_party_output != None:
        return make_response(jsonify({
            "status": 201,
            "data": [created_party_output]
        }), 201)
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])

    
    
    


