
from flask import Blueprint, jsonify, request, make_response
from random import randint
from politico_app.models.office import Office

office_blueprint = Blueprint('office_blueprint', __name__)

@office_blueprint.route("/offices/", methods=['POST'])
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
    
    new_office = Office(office_name, office_type)
    office_info = new_office.createOffice()
    return make_response(jsonify({
        "status": 200,
        "data": [
            office_info
        ]
    }), 200)
    
@office_blueprint.route("/offices/")
def getAllOffices():
    office = Office.getAllOffices()
    return make_response(jsonify({
        "status": 200,
        "data": [
            office
        ]
    }), 200)

@office_blueprint.route("/offices/<officeID>")
def getSingleOffice(officeID):

    office = Office.getOffice(int(officeID))

    if office == None:
        return make_response(jsonify({
            "status": 404,
            "error": "Could not find the "
        }))
    
    else:
        return make_response(jsonify({
            "status": 200,
            "data": [office]
        }))
    

