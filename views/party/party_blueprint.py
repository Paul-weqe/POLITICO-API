from flask import Flask, Blueprint, jsonify, make_response 
from politico_data import political_parties

party_blueprint = Blueprint('party_blueprint', __name__)

@party_blueprint.route("/parties/")
def getAllParties():
    return make_response(jsonify({
        "status": 200,
        "data": [
            political_parties
        ]
    }), 200)


