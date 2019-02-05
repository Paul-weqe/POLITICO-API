from flask import Blueprint, make_response, jsonify
from politico_data import offices 

office_blueprint = Blueprint('office_blueprint', __name__)

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
