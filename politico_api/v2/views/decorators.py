from functools import wraps
from flask import request, make_response, jsonify
import jwt
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        if "Authorization" in request.headers:
            header_data = request.headers["Authorization"].split(" ")
        else:
            return make_response(jsonify({"message": "Enter a valid token"}), 403)

        if len(header_data) < 2:
            return make_response(jsonify({"message": "token is missing"}), 403)
        elif header_data[0] != "Bearer":
            return make_response(jsonify({"message": "Authorization to be structured 'Bearer [token]'"}), 403)

        token = header_data[1]
        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except Exception as e:
            return make_response(jsonify({"message": "token is invalid"}), 403)
            
        return f(*args, **kwargs) 
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        json_data = request.get_json()
        
        if "Authorization" not in request.headers:
            return make_response(jsonify({"error": "Authorization key mist be part of the request header"}), 403)
        
        header_data = request.headers["Authorization"].split(" ")
        
        if len(header_data) < 2:
            return make_response(jsonify({"message": "token is missing"}), 403)
        elif header_data[0] != "Bearer":
            return make_response(jsonify({"message": "Authorization to be structured 'Bearer [token]'"}), 401)

        token = header_data[1]
        
        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            if data['admin'] != True:
                return make_response(jsonify({"message": "admin token required"}), 401)
        except Exception as e:
            return make_response(jsonify({"message": "token is invalid"}), 403)
            
        return f(*args, **kwargs) 
    return decorated

def json_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if request.content_type != "application/json":
            return make_response(jsonify({"error": "the content type used must be 'application/json'"}), 406)

        return f(*args, **kwargs)

    return decorated
