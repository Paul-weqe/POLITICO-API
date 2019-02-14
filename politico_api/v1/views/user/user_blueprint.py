from flask import Blueprint, request, make_response, jsonify
from politico_api.v1.models.user import UserModel

user_blueprint_v1 = Blueprint('user_blueprint_v1', __name__, url_prefix="/api/v1/users")


@user_blueprint_v1.route("/signup", methods=["POST"], strict_slashes=False)
def create_user():
    required_fields = {
        "username": str, "email": str, "password": str
    }
    error = None

    json_data = request.get_json()

    for field in required_fields:
        if field not in json_data:
            error = "{} is a mandatory field".format(field)
            break 

        elif type(json_data[field]) != required_fields[field]:
            error = "{} must be a {}".format(field, required_fields[field])
            break

    user = UserModel(json_data)

    # returns a list of items if the user has been registered
    # otherwise, it returns an error message
    if error == None and type(user.create_user()) == list:
        return make_response(jsonify({
            "status": 200,
            "data": user.create_user()
        }), 200)
    
    elif error == None:
        error = user.create_user()

    return make_response(jsonify({
        "status": 400,
        "error": error
    }), 400)

