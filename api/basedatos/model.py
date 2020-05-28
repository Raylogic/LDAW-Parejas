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
class Usuario(db.Model, UserMixin, Base):
    __tablename__ = 'Usuario'
    UserID = db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(100), unique=True, nullable=False)
    mail= db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    trabajo = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Integer, default=1)
    
    registra = db.relationship('Evento', secondary='Registra')
    boleto = db.relationship('Evento', secondary='Boleto')

    def __repr__(self):
        return '<Usuario: {}>'.format(self.Nombre)


class Evento(db.Model, Base):
    __tablename__ = 'Evento'
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
    activo = db.Column(db.Integer, default=1)

    registra = db.relationship('Usuario', secondary='Registra')
    boleto = db.relationship('Usuario', secondary='Boleto')
    
    def __repr__(self):
        return '<Evento: {}>'.format(self.Nombre)

class Boleto(db.Model, Base):
    __tablename__ = 'Boleto'
    Folio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Usuario.UserID'))
    EventID = db.Column(db.Integer, db.ForeignKey('Evento.EventID'))
    Expedicion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    imagen = db.Column(db.String(100), nullable=False, default='default.jpg')

    def __repr__(self):
        return '<Boleto: {}>'.format(self.Folio)

class Registra(db.Model, Base):
    __tablename__ = 'Registra'
    RegistroID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Usuario.UserID'))
    EventID = db.Column(db.Integer, db.ForeignKey('Evento.EventID'))

    def __repr__(self):
        return '<Registra: {}>'.format(self.RegistroID)