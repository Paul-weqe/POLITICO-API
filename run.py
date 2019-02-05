
from flask import Flask 
from views.party.party_blueprint import party_blueprint
from views.office.office_blueprint import office_blueprint

app = Flask(__name__)

app.register_blueprint(party_blueprint)
app.register_blueprint(office_blueprint)
