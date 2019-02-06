from politico_app.views.office.office_blueprint import office_blueprint
from politico_app.views.party.party_blueprint import party_blueprint
from flask import Flask 

app = Flask(__name__)

app.register_blueprint(office_blueprint)
app.register_blueprint(party_blueprint)
