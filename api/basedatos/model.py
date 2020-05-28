#from main import db #, login_manager
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from .database import db, marsh
from flask_bcrypt import generate_password_hash, check_password_hash
from marshmallow import fields
from datetime import datetime
from flask_login import UserMixin

#Modelo
Base = declarative_base()

"""
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
"""
class Usuario(db.Model, UserMixin):
    UserID = db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(100), unique=True, nullable=False)
    mail= db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    trabajo = db.Column(db.String(100), nullable=False)
    eventos = db.relationship('Evento', backref='empleado', lazy =True)

    def __repr__(self):
        return f"Usuario('{self.nombre}','{self.mail}')"


class Evento(db.Model):
    EventID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    Siglas = db.Column(db.String(10), nullable=False)
    Descripcion = db.Column(db.String(1000), nullable=False)
    Duracion = db.Column(db.Integer, nullable=False)
    Asistentes = db.Column(db.Integer, nullable=False)
    Fecha = db.Column(db.DateTime,nullable=False)
    Hora = db.Column(db.DateTime,nullable=False)
    Costo = db.Column(db.Integer, nullable=False)
    Lugar = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(100), nullable=False, default='default.jpg')
    
    def __repr__(self):
        return f"Evento('{self.Nombre}','{self.Descripcion}','{self.Lugar}')"

class Boleto(db.Model):
    Folio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Usuario.UserID'))
    EventID = db.Column(db.Integer, db.ForeignKey('Evento.EventID'))
    Expedicion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    imagen = db.Column(db.String(100), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Evento('{self.Folio}','{self.Fecha}')"