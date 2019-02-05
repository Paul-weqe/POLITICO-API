
from flask import Blueprint, jsonify, request, make_response
from politico_data import political_parties, users, offices, candidates, votes
from random import randint

office_blueprint = Blueprint('office_blueprint', __name__)

@office_blueprint.route("/offices", methods=['POST'])
def createOffice():
    json_data = request.get_json(force=True)

    required_fields = ["office_type", "office_name"]
    for field in required_fields:
        if field not in json_data:
            return make_response(jsonify({
                "status": 404, 
                "error": "Field {} is mandatory in the request body".format(field)
            }), 404)

    office_type = json_data["office_type"]
    office_name = json_data["office_name"]
    office_id = randint(1, 100)
    new_office = {
        "id": office_id, "name": office_name, "type": office_type
    }
    offices.append(new_office)

    return make_response(jsonify({
        "status": 200,
        "data": [
            new_office
        ]
    }), 200)
    
@office_blueprint.route("/offices")
def getAllOffices():
    return make_response(jsonify(offices), 200)

@office_blueprint.route("/offices/<officeID>")
def getSingleOffice(officeID):
    
    for office in offices:
        if int(officeID) == office["id"]:
            return make_response(jsonify({
                "status": 200,
                "data": [
                    office
                ]
            }), 200)
    
    return make_response(jsonify({
        "status": 404, 
        "error": "cannot find political office with ID {}".format(officeID)
    }))

