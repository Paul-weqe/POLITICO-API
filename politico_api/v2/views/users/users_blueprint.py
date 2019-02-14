from flask import Blueprint, make_response, jsonify, request
from politico_api.v2.models.models import User
from politico_api.v2.views.api_response_data import mandatory_fields
from politico_api.v2.views.api_functions import ApiFunctions

users_blueprint_v2 = Blueprint('user_blueprint_v2', __name__, url_prefix="/api/v2/users")

@users_blueprint_v2.route("/signup", methods=['POST'])
def create_user():
    
    required_fields = {
        "first_name": str, "last_name": str, "other_name": str, "email": str, "phone_number": str, "passport_url": str
    }
    optional_fields = {
        "is_admin": bool, "is_politician": bool
    }
    json_data = request.get_json(force=True)
    error = None 

    # checks for the presence of the required fields and their data types
    for field in required_fields:
        if field not in json_data:
            error = [406, "{} is a mandatory field".format(field)]
            break 
        elif required_fields[field] != type(json_data[field]):
            error = [406, "{} is supposed to be a {}".format(field, required_fields[field])]
            print(type(json_data[field]))
            break
    
    # looks for if the optional fields are present and makes sure the daya types used in them are correct
    for field in optional_fields:
        if (field in json_data) and (optional_fields[field] != type(json_data[field])) and (error==None):
            error = [406, "{} has to be a {}".format(field, optional_fields[field])]
            break

    if error == None:
        new_user = User.create_user(**json_data)
        if new_user != False:
            return make_response(jsonify({
                "status": 200,
                "data": new_user
            }), 200)
        error = [406, "unable to create user"]
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])


        
