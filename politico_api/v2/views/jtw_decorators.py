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

        if "token" not in json_data:
            return make_response(jsonify({'message': 'token is missing'}), 403)
        
        token = json_data["token"]
        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'))
        
        except Exception as e:
            return make_request(jsonify({'message': 'Token is invalid'}), 403)
            
        return f(*args, **kwargs) 
    return decorated

