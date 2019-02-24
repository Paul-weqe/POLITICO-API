from flask import Blueprint, request, make_response, jsonify
from politico_api.v2.validators import Validate, RegularExpressions
from politico_api.v2.models.models import Party
from politico_api.v2.views.decorators import admin_required

party_blueprint_v2 = Blueprint('party_blueprint_v2', __name__, url_prefix="/api/v2/party")


@party_blueprint_v2.route("/", methods=["POST"], strict_slashes=False)
@admin_required
def create_party():
    db = request.args.get('db')
    json_data = request.get_json()
    required_fields = {
        "party_name": str, "party_hq": str, "party_logo": str
    }
    error = None 

    for field in required_fields:
        if field not in json_data:
            error = [400, "Field {} is a mandatory field".format(field)]
            break
        
        elif type(json_data[field]) != required_fields[field]:
            error = [400, "Field {} has to be a {}".format(field, required_fields[field])]
            break
        
        elif required_fields[field] == str and Validate.validate_field(json_data[field]) != True:
            validate_message = Validate.validate_field(json_data[field])
            error = [400, validate_message.format(field)]
            break
    
    if error==None and RegularExpressions.is_http_input(json_data["party_logo"]) is not True:
        error = [400, "the party_logo field has to be a url"]
    
    if error == None:
        party = Party(party_name=json_data["party_name"], party_hq=json_data["party_hq"], party_logo=json_data["party_logo"], db=db)
        make_party = party.create_party()

        if make_party == True:
            return make_response(jsonify({
                "status": 201,
                "party information": [
                    {
                        "party_name": json_data["party_name"],
                        "party_hq": json_data["party_hq"]
                    }
                ]
            }), 201)
        
        error = [400, make_party]
    
    print(error)
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])


@party_blueprint_v2.route("/", strict_slashes=False)
def get_all_parties():
    party = Party()
    all_parties = party.get_all_parties()
    final_dict = []
    for p in all_parties:
        final_dict.append({
            "id": p[0],
            "name": p[1],
            "hq": p[2]
        })

    return make_response(jsonify({
        "status": 200,
        "data": final_dict
    })) 