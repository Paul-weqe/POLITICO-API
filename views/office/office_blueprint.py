from flask import Blueprint, request, make_response, jsonify
from politico_data import offices

office_blueprint = Blueprint('office_blueprint', __name__)

@office_blueprint.route("/offices")
def getAllOffices():
    return make_response(jsonify(offices), 200)
