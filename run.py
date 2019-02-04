from flask import Flask
from views.office.office_blueprint import office_blueprint

app = Flask(__name__)

app.register_blueprint(office_blueprint)

