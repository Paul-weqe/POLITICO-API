from flask import Blueprint, jsonify, request, make_response
from politico_api.v2.models.models import Office
# from politico_api.v2.views.jtw_decorators import token_required

office_blueprint_v2 = Blueprint('office_blueprint_v2', __name__, url_prefix="/api/v2/offices")

@office_blueprint_v2.route("/get-office-results", strict_slashes=False)
def get_office_results():

    error = None 
    json_data = request.get_json()
    office_results = None 

    if "office_id" not in json_data:
        error = [400, "office_id is a mandatory field"]
    elif type(json_data["office_id"]) != int:
        error = [400, "office_id must be an integer"]
    
    
    if error == None:
        office_obj = Office()
        office_results = office_obj.count_office_votes(json_data["office_id"])
    
    if error == None and office_results == None:
        error = [404, "office with ID {} does not exist".format(json_data["office_id"])]
        
    if error == None:
        return make_response(jsonify({
            "status": 200,
            "data": office_results
        }), 200)

    return make_response(jsonify({
        "status": error[0],
        "error": error[1]
    }), error[0])
