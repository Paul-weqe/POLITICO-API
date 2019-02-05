from flask import Flask 
from views.party.party_blueprint import party_blueprint

app = Flask(__name__)

app.register_blueprint(party_blueprint)
