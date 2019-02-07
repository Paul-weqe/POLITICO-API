from politico_api.v1.views.office.office_blueprint import office_blueprint_v1
from politico_api.v1.views.party.party_blueprint import party_blueprint_v1
from flask import Flask, make_response, jsonify

app = Flask(__name__)

app.register_blueprint(office_blueprint_v1)
app.register_blueprint(party_blueprint_v1)


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({
        "status": 404,
        "error": "The page you are looking for could not be found"
    }), 404)


@app.errorhandler(405)
def method_not_allowed(e):
    return make_response(jsonify({
        "status": 405,
        "error": "That method cannot be used on this route"
    }), 405)
