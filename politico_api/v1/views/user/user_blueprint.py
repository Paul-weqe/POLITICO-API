from flask import Blueprint, request, make_response, jsonify
from politico_api.v1.models.user import UserModel

user_blueprint_v1 = Blueprint('user_blueprint_v1', __name__, url_prefix="/api/v1/users")

@user_blueprint_v1.route("/", strict_slashes=False)
def get_all_users():
    user = UserModel()
    return make_response(jsonify({
        "status": 200,
        "data": user.get_all_users()
    }), 200)

# get information of a single user
@user_blueprint_v1.route("/<userID>", strict_slashes=False)
def get_single_user(userID):
    error = None 
    user = UserModel()

    try:
        userID = int(userID)
    except ValueError:
        error = [400, "the userID must be an integer"]
    
    user_info = user.get_single_user(userID)
    if user_info != None and error == None:
        return make_response(jsonify({
            "status": 200,
            "data": [user_info]
        }), 200)
    elif user_info == None and error == None:
        error = "user with ID {} not found".format(userID)
        
    return make_response(jsonify({
        "status": 400,
        "error": error 
    }), 400)

@user_blueprint_v1.route("/signup", methods=["POST"], strict_slashes=False)
def create_user():
    required_fields = {
        "username": str, "email": str, "password": str
    }
    error = None
    json_data = request.get_json()

    for field in required_fields:

        # checks for presence of required fields
        if field not in json_data:
            error = [400, "{} is a mandatory field".format(field)]
            break 
        
        # checks if the data type is correct
        elif type(json_data[field]) != required_fields[field]:
            error = [400, "{} must be a {}".format(field, required_fields[field])]
            break

    user = UserModel(json_data)

    # returns a list of items if the user has been registered
    # otherwise, it returns an error message
    
    if error == None:
        user_info = user.create_user()
        if user_info == "the email is already in use":
            error = [404, "the email address is already in use"]
        elif user_info != None:
            return make_response(jsonify({
                "status": 201,
                "message": "user {} has been successfully registered".format(json_data["username"])
            }), 201)
    
    elif error == None:
        error = user.create_user()

    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])

# logins the user
@user_blueprint_v1.route("/login", methods=["POST"], strict_slashes=False)
def login_user():
    required_fields = {
        "email": str, "password": str
    }
    json_data = request.get_json()
    error = None  
    user = UserModel()

    for field in required_fields:
        if field not in json_data:
            error = [400, "{} is a mandatory field".format(field)]
            break 

        elif type(json_data[field]) != required_fields[field]:
            error = [400, "{} must be a {}".format(field, required_fields[field])]
            break
    
    
    if error == None:
        user_info = user.get_user_by_email_and_password(json_data["email"], json_data["password"])
        if user_info == None:
            error = [404, "could not find specified user"]
    

    if error == None:
        return make_response(jsonify({
            "status": 200,
            "data": [user_info]
        }), 200)
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])

# delete user route
@user_blueprint_v1.route("/<userID>", methods=["DELETE"], strict_slashes=False)
def delete_user(userID):
    error = None 

    # tests if partyID is an integer
    try:
        userID = int(userID)
    except ValueError:
        error = [400, "partyID must be a number"]
    
    if error == None and userID < 1:
        error = [400, "partyID cannot be zero or a negative number"]
    

    user = UserModel()
    if error == None:
        is_deleted = user.delete_user(userID)
        # when is_deleted == None, the 
        if is_deleted == None:
            error = [404, "could not find user with ID {}".format(userID)]
        else:
            return make_response(jsonify({
                "status": 200,
                "data": is_deleted
            }), 200)
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])


