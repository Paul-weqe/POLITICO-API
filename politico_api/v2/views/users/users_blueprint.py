from flask import Blueprint, make_response, jsonify, request
from politico_api.v2.models.user import UserModel

users_blueprint_v2 = Blueprint('user_blueprint_v2', __name__, url_prefix="/api/v2/users")


# enables the creation of a specific user in the system
@users_blueprint_v2.route("/", strict_slashes=False, methods=["POST"])
def create_new_user():

    required_fields = {
        "username": str, 
        "email": str,
        "password": str,
        }

    json_data = request.get_json(force=True)

    print(json_data)
    for field in required_fields:
        if field not in json_data:
            return make_response(jsonify({
                "status": 406,
                "error": "{} is a mandatory field".format(field)
            }), 406)
        elif required_fields[field] != type(json_data[field]):
            return make_response(jsonify({
                "status": 406,
                "error": "{} has to be a {}".format(field, required_fields[field])
            }), 406)
    
    new_user = UserModel.create_user(json_data["username"], json_data["email"], json_data["password"])
    if new_user:
        return make_response(jsonify({
            "status": 200,
            "data": "user {} created successfully".format(json_data["username"])
        }), 200)
    
    elif new_user == "email exists":
        return make_response(jsonify({
            "status": 406,
            "error": "Unable to create user. Email exists"
        }))

    else:
        return make_response(jsonify({
            "status": 406,
            "error": "unable to create user. Look at log for details"
            }), 406)
