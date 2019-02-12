from flask import Blueprint, make_response, jsonify, request
from politico_api.v2.models.user import UserModel
from politico_api.v2.views.api_response_data import mandatory_fields
from politico_api.v2.views.api_functions import ApiFunctions

users_blueprint_v2 = Blueprint('user_blueprint_v2', __name__, url_prefix="/api/v2/users")


# enables the creation of a specific user in the system
@users_blueprint_v2.route("/signup", strict_slashes=False, methods=["POST"])
def create_new_user():

    required_fields = mandatory_fields["create_user"]

    json_data = request.get_json(force=True)
    error = None
    
    if not ApiFunctions.check_valid_fields(required_fields, json_data):
        error = ApiFunctions.check_valid_fields(required_fields, json_data)
    new_user = None 
    data = None

    new_user = UserModel.create_user(json_data["username"], json_data["email"], json_data["password"])

    if new_user:
        data = "user {} created successfully".format(json_data["username"])
    elif new_user == "email exists":
        error = "Unable to create user. Email already in use"
    else:
        error = "unable to create user. Look at log for details"

    if error != None:
        return ApiFunctions.return_406_response(error)
    return ApiFunctions.return_200_response(data)


@users_blueprint_v2.route("/login", strict_slashes=False, methods=["POST"])
def login_user():
    required_fields = mandatory_fields["login_user"]

    error = None 
    data = None 

    json_data = request.get_json()
    
    if not ApiFunctions.check_valid_fields(required_fields, json_data):
        error = ApiFunctions.check_valid_fields(required_fields, json_data)

    login_user = UserModel.find_user_by_email_and_password(json_data["email"], json_data["password"])
    print(login_user)
    if type(login_user) == tuple and error == None:
        return ApiFunctions.return_200_response("logged in {} successfully".format(login_user[1]))
    
    return ApiFunctions.return_406_response("Cannot find user. Try again")


