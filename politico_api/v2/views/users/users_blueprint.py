from flask import Blueprint, make_response, jsonify, request
from politico_api.v2.models.models import User
from politico_api.v2.views.api_response_data import mandatory_fields
from politico_api.v2.views.api_functions import ApiFunctions
from politico_api.v2.views.jtw_decorators import token_required
from functools import wraps
import datetime
import jwt
import os


users_blueprint_v2 = Blueprint('user_blueprint_v2', __name__, url_prefix="/api/v2/users")



@users_blueprint_v2.route("/signup", methods=['POST'])
def create_user():
    required_fields = {
        "first_name": str, "last_name": str, "other_name": str, "email": str, "phone_number": str, "passport_url": str, "password": str
    }
    optional_fields = {
        "is_admin": bool, "is_politician": bool
    }
    json_data = request.get_json(force=True)
    error = None 

    # checks for the presence of the required fields and their data types
    for field in required_fields:
        if field not in json_data:
            error = [400, "{} is a mandatory field".format(field)]
            break 
        elif required_fields[field] != type(json_data[field]):
            error = [400, "{} is supposed to be a {}".format(field, required_fields[field])]
            print(type(json_data[field]))
            break
    
    # looks for if the optional fields are present and makes sure the daya types used in them are correct
    for field in optional_fields:
        if (field in json_data) and (optional_fields[field] != type(json_data[field])) and (error==None):
            error = [400, "{} has to be a {}".format(field, optional_fields[field])]
            break
    

    if error == None:
        user_obj = User(**json_data)
        new_user = user_obj.create_user()

        ## create_user() returns None if the user already exists
        if new_user == None:
            error = [404, "a user with the email already exists"]

        elif new_user != False:
            return make_response(jsonify({
                "status": 200,
                "data": new_user
            }), 200)
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])

@users_blueprint_v2.route("/change-password", methods=["PATCH"])
def change_password():

    required_fields = {
        "email": str, "old_password": str, "new_password": str
    }
    json_data = request.get_json()

    ## 
    print("###")
    print(json_data)
    error = None 
    changed_password = None

    for field in required_fields:
        if field not in json_data:
            error = [400, "{} is a mandatory field".format(field)]
            break
        elif required_fields[field] != type(json_data[field]):
            error = [400, "{} must be a {}".format(field, required_fields[field])]
            break
    
    if error == None:
        user = User()
        changed_password = user.change_password(json_data["email"], json_data["old_password"], json_data["new_password"])
    
    ## When change password returns true. Meaning the password has been changed successfully
    if changed_password == True and error == None:
        return make_response(jsonify({
            "status": 200,
            "data": "Password for {} has been changed successfully".format(json_data["email"])
        }), 200)
    
    if error == None:
        error = [404, "The user could not be found" if changed_password == None else changed_password]
    
    return make_response(jsonify({
        "status": error[0], "error": error[1]
    }), error[0])

@users_blueprint_v2.route("/login", methods=["POST"], strict_slashes=False)
def user_login():
    json_data = request.get_json()
    required_fields = {
        "email": str, "password": str
    }
    error = None 
    response = None

    for field in required_fields:
        if field not in json_data:
            error = [400, "{} is a mandatory field".format(field)]
        elif required_fields[field] != type(json_data[field]):
            error = [400, "{} must be a {}".format(field, required_fields[field])]
    

    user = User()
    
    if error == None:
        response = user.get_user_by_email_and_password(json_data["email"], json_data["password"])
        if response == None:
            error = [404, "could not find the user specified"]
    
    if error == None:
        token = jwt.encode({'email': json_data["email"], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            os.getenv('SECRET_KEY'))
        return make_response(jsonify({
            "token": token.decode('UTF-8'),
            "status": 200,
            "data": response
        }), 200)
    
    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])


