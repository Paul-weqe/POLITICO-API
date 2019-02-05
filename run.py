from flask import Flask 
from politico_app.views.office.office_blueprint import office_blueprint
from politico_app.views.party.party_blueprint import party_blueprint
from politico_app.politico_data import offices, political_parties

app = Flask(__name__)

app.register_blueprint(party_blueprint)
app.register_blueprint(office_blueprint)
