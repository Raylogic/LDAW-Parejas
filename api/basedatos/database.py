
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
marsh = Marshmallow()
bcrypt = Bcrypt()
def initialize_db(app):
    db.init_app(app)
    Migrate(app, db,compare_type=True)
    marsh.init_app(app)
    bcrypt.init_app(app)