
from flask import Flask

def create_app(config_object):
    

    from politico_api.v1.views.office.office_blueprint import office_blueprint_v1
    from politico_api.v1.views.party.party_blueprint import party_blueprint_v1
    v1_app = Flask(__name__)

    v1_app.config.from_object(config_object)
    v1_app.register_blueprint(office_blueprint_v1)
    v1_app.register_blueprint(party_blueprint_v1)

    return v1_app
