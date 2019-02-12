from flask import Blueprint, jsonify, make_response, request
from random import randint
from politico_api.v2.models.party import PartyModel
from politico_api.v2.views.api_response_data import error_dictionary, mandatory_fields
from politico_api.v2.views.api_functions import ApiFunctions

party_blueprint_v2 = Blueprint('party_blueprint_v2', __name__, url_prefix="/api/v1/parties")

@party_blueprint_v2.route("/", strict_slashes=False)
def get_all_parties():
    return ApiFunctions.return_200_response(PartyModel.get_all_parties())

@party_blueprint_v2.route("/<partyID>/<partyName>", methods=['PATCH'], strict_slashes=False)
def edit_party(partyID, partyName):

    edit_party_error_statements = error_dictionary["edit_party"]
    edit_party_output = None 
    
    error = None
    
    # make sure the partyID is a number(int)
    if ApiFunctions.check_is_integer(partyID) == False:
        error = edit_party_error_statements["ID_HAS_TO_BE_NUMBER"]
    
    # partyID cannot be 0 or a negative number
    elif int(partyID) < 1 and error == None:
        error = edit_party_error_statements["ID_HAS_TO_BE_MORE_THAN_ZERO"]

    # making sure that the partyName does not contain any special characters
    elif ApiFunctions.check_for_special_characters(partyName):
        error = edit_party_error_statements["NAME_CANNOT_CONTAIN_SPECIAL_CHARACTERS"]
    
    # make sure the party exists before it is edited
    # edit_party_output will return False if the party does not exist but will return the party details after editing if the party exists
    
    else:
        edit_party_output = PartyModel.edit_party(int(partyID), partyName)
    
    if error == None: error = ApiFunctions.check_error_if_item_is_true(edit_party_output, False, error, edit_party_error_statements["CANNOT_FIND_PARTY"].format(partyID))

    if error != None:
        return ApiFunctions.return_406_response(error)
    
    return ApiFunctions.return_200_response(edit_party_output)

@party_blueprint_v2.route("/<partyID>", methods=['DELETE'], strict_slashes=False)
def delete_party(partyID):

    delete_party_error_statements = error_dictionary["delete_party"]
    delete_party_output = None
    error = None 

    # check if partyID is integer 
    if ApiFunctions.check_is_integer(partyID) == False:
        error = delete_party_error_statements["ID_HAS_TO_BE_NUMBER"]
    
    elif ApiFunctions.check_if_number_is_zero_or_negative(int(partyID)):
        error = delete_party_error_statements["ID_HAS_TO_BE_POSITIVE"]

    # deletePartyOutput = PartyModel.delete_party(int(partyID))
    elif PartyModel.delete_party(int(partyID)) == False:
        error = delete_party_error_statements["UNABLE_TO_FIND_PARTY"].format(partyID)
    
    if error != None:
        return ApiFunctions.return_406_response(error)

    return ApiFunctions.return_200_response("successfully deleted")
    

@party_blueprint_v2.route("/<partyID>", strict_slashes=False)
def get_single_party(partyID):
    get_party_output = PartyModel.get_single_party(int(partyID))

    if get_party_output == None:
        return ApiFunctions.return_406_response("unable to find party with ID {}".format(partyID))

    return ApiFunctions.return_200_response([get_party_output]) 

@party_blueprint_v2.route("/", methods=['POST'], strict_slashes=False)
def create_party():
    json_data = request.get_json(force=True)

    # dictionary of the mandatory fields together with the datatypes that they are required to be of
    create_party_required = mandatory_fields["create_party"]
    
    for field in create_party_required:

        # checks if any of the mandatory field is absent in the JSON data which will lead to a 404 error
        if field not in json_data:
            return ApiFunctions.return_406_response("'{}' is a mandatory field".format(field))

        # testing for the data type of the fields based on the corresponding value in required_fields dictionary
        elif type(json_data[field]) != create_party_required[field]:
            return ApiFunctions.return_406_response("'{}' field must be a '{}'".format(field, create_party_required[field]))

    # initialize a party using the PartyModel
    party = PartyModel(json_data)
    created_party_output = party.createParty()
    return ApiFunctions.return_200_response([created_party_output])
