from flask import Blueprint, make_response, jsonify, request
from politico_api.v2.models.user import UserModel
from politico_api.v2.views.api_response_data import mandatory_fields
from politico_api.v2.views.api_functions import ApiFunctions

users_blueprint_v2 = Blueprint('user_blueprint_v2', __name__, url_prefix="/api/v2/users")

@users_blueprint_v2.route("/create-user", methods=['POST'])
def create_user():
    return None 
