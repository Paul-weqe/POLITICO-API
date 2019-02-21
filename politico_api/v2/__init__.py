from flask import Flask, make_response, jsonify

def create_app(config_object=None):
    from politico_api.v2.views.users.users_blueprint import users_blueprint_v2
    from politico_api.v2.views.votes.votes_blueprint import votes_blueprint_v2
    from politico_api.v2.views.office.office_blueprint import office_blueprint_v2
    from politico_api.v2.views.petition.petition_blueprint import peition_blueprint_v2
    from politico_api.v2.views.party.party_blueprint import party_blueprint_v2
    
    v2_app = Flask(__name__)
    
    if config_object != None:
        v2_app.config.from_object(config_object)
    
    v2_app.register_blueprint(users_blueprint_v2)
    v2_app.register_blueprint(votes_blueprint_v2)
    v2_app.register_blueprint(office_blueprint_v2)
    v2_app.register_blueprint(peition_blueprint_v2)
    v2_app.register_blueprint(party_blueprint_v2)

    @v2_app.errorhandler(405)
    def error_405(e):
        return make_response(jsonify({
            "status": 405,
            "error": "That method cannot be used for this page"
        }), 405)

    @v2_app.errorhandler(500)
    def error_500(e):
        return make_response(jsonify({
            "status": 500,
            "error": "The problem is on our side"
        }), 500)

    return v2_app
