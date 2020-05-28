from flask import Flask
from flask_restful import Api
from basedatos.database import initialize_db
from recursos.routing import initialize_routes
import os, json

class Config():
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY = os.urandom(24)

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app, prefix="/api/v1")

initialize_db(app)
initialize_routes(api)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=6000)