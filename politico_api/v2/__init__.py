from flask import Flask 


def create_app(config_object=None):
    from politico_api.v2.views.users.users_blueprint import users_blueprint_v2
    from politico_api.v2.views.votes.votes_blueprint import votes_blueprint_v2
    from politico_api.v2.views.office.office_blueprint import office_blueprint_v2

    v2_app = Flask(__name__)

    if config_object != None:
        v2_app.config.from_object(config_object)
    
    v2_app.register_blueprint(users_blueprint_v2)
    v2_app.register_blueprint(votes_blueprint_v2)
    v2_app.register_blueprint(office_blueprint_v2)
    
    return v2_app
