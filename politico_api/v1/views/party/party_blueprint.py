from flask import Blueprint, jsonify, make_response, request
from random import randint
from politico_api.v1.models.party import PartyModel
from politico_api.v1.views.api_response_data import error_dictionary, mandatory_fields
from politico_api.v1.views.api_functions import ApiFunctions

party_blueprint_v1 = Blueprint('party_blueprint', __name__, url_prefix="/api/v1/parties")

@party_blueprint_v1.route("/", strict_slashes=False)
def get_all_parties():
    return make_response(jsonify({
        "status": 200,
        "data": PartyModel.get_all_parties()
    }), 200)

@party_blueprint_v1.route("/<partyID>", methods=['PATCH'], strict_slashes=False)
def edit_party(partyID):

    edit_party_response = None 
    json_data = request.get_json()
    partyName = json_data["partyName"]

    error = None
    
    # make sure the partyID is a number(int)
    if ApiFunctions.check_is_integer(partyID) == False:
        error = "partyID has to be a number"
    
    # partyID cannot be 0 or a negative number
    elif int(partyID) < 1 and error == None:
        error = "partyID has to be more than 0"

    # making sure that the partyName does not contain any special characters
    elif ApiFunctions.check_for_special_characters(partyName):
        error = "partyName cannot contain special characters like @ or $"
    
    # make sure the party exists before it is edited
    # edit_party_output will return False if the party does not exist but will return the party details after editing if the party exists
    
    else:
        edit_party_response = PartyModel.edit_party(int(partyID), partyName)
    
    if edit_party_response == False and error == None:
            return "cannot find party with ID {}".format(partyID)

    if error != None:
        return make_response(jsonify({
            "status": 406,
            "error": error
        }), 406)

    
    return make_response(jsonify({
        "status": 200, "data": [edit_party_response]
    }), 200)


@party_blueprint_v1.route("/<partyID>", methods=['DELETE'], strict_slashes=False)
def delete_party(partyID):

    delete_party_error_statements = error_dictionary["delete_party"]

    delete_party_output = None
    error = None 

    # check if partyID is integer 
    if ApiFunctions.check_is_integer(partyID) == False:
        error = "partyID has to be a number"
    
    elif int(partyID) < 1:
        error = "partyID cannot be 0 or a negative number"

    # deletePartyOutput = PartyModel.delete_party(int(partyID))
    elif PartyModel.delete_party(int(partyID)) == False:
        error = "unable to delete party with ID {}".format(partyID)

    if error != None:
        return make_response(jsonify({
            "status": 406,
            "error": error
        }), 406)

    return make_response(jsonify({
        "status": 200,
        "data": "successfully deleted"
    }), 200)
    

@party_blueprint_v1.route("/<partyID>", strict_slashes=False)
def get_single_party(partyID):
    
    error = None 
    get_party_output=None

    if not ApiFunctions.check_is_integer(partyID):
        error = "partyID must be an integer"
    
    else:
        get_party_output = PartyModel.get_single_party(int(partyID))
    

    if get_party_output == None and error == None:
        error = "unable to find party with ID {}".format(partyID)
    
    print(error)
    print("###")
    if error != None:
        return make_response(jsonify({
            "status": 406,
            "error": error
        }), 406)
    
    return make_response(jsonify({
        "status": 200,
        "data": [get_party_output]
    }), 200)


@party_blueprint_v1.route("/", methods=['POST'], strict_slashes=False)
def create_party():
    json_data = request.get_json(force=True)

    # dictionary of the mandatory fields together with the datatypes that they are required to be of
    create_party_required = mandatory_fields["create_party"]
    
    for field in create_party_required:

        # checks if any of the mandatory field is absent in the JSON data which will lead to a 404 error
        if field not in json_data:
            return make_response(jsonify({
                "status": 406,
                "error": "'{}' is a mandatory field".format(field)
            }), 406)

        # testing for the data type of the fields based on the corresponding value in required_fields dictionary
        elif type(json_data[field]) != create_party_required[field]:
            return make_response(jsonify({
                "status": 406,
                "error": "'{}' field must be a {}".format(field, create_party_required[field])
            }), 406)

    # initialize a party using the PartyModel
    party = PartyModel(json_data)
    created_party_output = party.createParty()
    print(created_party_output)

    return make_response(jsonify({
        "status": 200,
        "data": [created_party_output]
    }), 200)

