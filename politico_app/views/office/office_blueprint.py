
from flask import Blueprint, jsonify, request, make_response
from random import randint
from politico_app.models.office import Office

office_blueprint = Blueprint('office_blueprint', __name__)

@office_blueprint.route("/offices/", strict_slashes=False, methods=['POST'])
def createOffice():
    json_data = request.get_json(force=True)
    
    required_fields = {
        "office_type": str, 
        "office_name": str
        }
    
    for field in required_fields:
        if field not in json_data:
            return make_response(jsonify({
                "status": 404, 
                "error": "Field '{}' is mandatory in the request body".format(field)
            }), 404)
        
        #check if field in json_data is of the right data type
        elif type(json_data[field]) != required_fields[field]:
            return make_response(jsonify({
                "status": 404,
                "error": "Field '{}' has to be a '{}'".format(field, required_fields[field])
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
    
@office_blueprint.route("/offices", strict_slashes=False)
def getAllOffices():
    office = Office.getAllOffices()
    return make_response(jsonify({
        "status": 200,
        "data": office
    }), 200)

@office_blueprint.route("/offices/<officeID>", strict_slashes=False)
def getSingleOffice(officeID):
    
    # make sure only real numbers are accepted as the officeID
    # fails if officeID is not a real number e.g a String
    try:
        officeID = int(officeID)

    except ValueError:
        return make_response(jsonify({
            "status": 404,
            "error": "you must enter a real number at officeID in '/offices/<officeID>'"
        }), 404)

    office = Office.getOffice(officeID)

    # makes sure the officeID is not less than 1
    if int(officeID) < 1:
        return make_response(jsonify({
            "status": 404,
            "error": "entering a negative number as officeID is not acceptable"
        }), 404)
    
        
    if office == None:
        return make_response(jsonify({
            "status": 404,
            "error": "Could not find the "
        }))
    
    else:
        return make_response(jsonify({
            "status": 200,
            "data": office
        }))
    
