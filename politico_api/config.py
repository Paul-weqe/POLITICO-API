# importing v1 blueprints
from politico_api.v1.views.office.office_blueprint import office_blueprint_v1
from politico_api.v1.views.party.party_blueprint import party_blueprint_v1

# importing v2 blueprints
# from politico_api.v2.views.users.users_blueprint import users_blueprint_v2

from flask import Flask, make_response, jsonify

app = Flask(__name__)

# register v1 blueprints
app.register_blueprint(office_blueprint_v1)
app.register_blueprint(party_blueprint_v1)

# register v2 blueprints
# app.register_blueprint(users_blueprint_v2)

def handle_error(error_number, error_message):
    @app.errorhandler(error_number)
    def page_not_found(e):
        return make_response(jsonify({
            "status": error_number,
            "error": error_message
        }), error_number)


handle_error(404, "The page you are looking for could not be found")
handle_error(405, "That method cannot be used in this route")
handle_error(500, "The problem is on our side. It will be fixed shortly")
