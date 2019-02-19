from functools import wraps
from flask import request, make_response, jsonify
import jwt
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = request.args.get('token')
        # app = kwargs["app_name"]
        json_data = request.get_json()

        # if "token" not in json_data:
        #     return make_response(jsonify({'message': 'token is missing'}), 403)
        
        header_data = request.headers["Authorization"].split(" ")

        if len(header_data) < 2:
            return make_response(jsonify({"message": "token is missing"}), 403)
        elif header_data[0] != "Bearer":
            return make_response(jsonify({"message": "Authorization to be structured 'Bearer [token]'"}), 403)

        token = header_data[1]
        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'))
            print(data)
        except Exception as e:
            return make_response(jsonify({"message": "token is invalid"}), 403)
            
        return f(*args, **kwargs) 
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = request.args.get('token')
        # app = kwargs["app_name"]
        json_data = request.get_json()

        # if "token" not in json_data:
        #     return make_response(jsonify({'message': 'token is missing'}), 403)
        
        header_data = request.headers["Authorization"].split(" ")

        if len(header_data) < 2:
            return make_response(jsonify({"message": "token is missing"}), 403)
        elif header_data[0] != "Bearer":
            return make_response(jsonify({"message": "Authorization to be structured 'Bearer [token]'"}), 403)

        token = header_data[1]
        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'))
            # print(data)
            if data['admin'] != True:
                return make_response(jsonify({"message": "admin token required"}), 403)
        except Exception as e:
            return make_response(jsonify({"message": "token is invalid"}), 403)
            
        return f(*args, **kwargs) 
    return decorated