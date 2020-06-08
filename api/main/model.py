from main import db, login_manager, marsh
from datetime import datetime
from marshmallow import fields
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Evento(db.Model):
    __tablename__ = 'Evento'
    eventID = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    siglas = db.Column(db.String(10), nullable=False)
    descripcion = db.Column(db.String(1000), nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    asistentes = db.Column(db.Integer, nullable=False)
    fechahora = db.Column(db.DateTime,nullable=False)
    costo = db.Column(db.Integer, nullable=False)
    lugar = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(100), nullable=False, default='default.jpg')
    activo = db.Column(db.Integer, default=1)

    registra = db.relationship('Usuario', secondary='Registra')
    boleto = db.relationship('Usuario', secondary='Boleto')
    
    def __repr__(self):
        return '<Evento: {}>'.format(self.nombre)

class EventoSchema(marsh.Schema):
    class Meta:
        fields=('eventID','nombre','siglas','descripcion','duracion','asistentes','fechahora','costo','lugar','imagen','activo','userID')

eventoSchema = EventoSchema()
eventosSchema = EventoSchema(many=True)

#-------------------------------------------------------------------------#

class Usuario(db.Model, UserMixin):
    __tablename__ = 'Usuario'
    userID = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(30), unique=True, nullable=False)
    nombre= db.Column(db.String(150), unique=True, nullable=False)
    mail= db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    trabajo = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Integer, default=1)
    
    registra = db.relationship('Evento', secondary='Registra')
    boleto = db.relationship('Evento', secondary='Boleto')
    rol = db.relationship('Rol', secondary='Rol')

    def __repr__(self):
        return '<Usuario: {}>'.format(self.username)

class UsuarioSchema(marsh.Schema):
    userID = fields.Integer()
    username = fields.String()
    nombre = fields.String()
    mail = fields.String()
    contrasena = fields.String()
    telefono = fields.String()
    edad = fields.Integer()
    estado = fields.String()
    trabajo = fields.String()
    activo = fields.Integer()
    eventos = fields.Nested(EventoSchema)

user_schema = UsuarioSchema()
users_schema = UsuarioSchema(many=True)

#-------------------------------------------------------------------------#

class Boleto(db.Model):
    __tablename__ = 'Boleto'
    folio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('Usuario.userID'))
    eventID = db.Column(db.Integer, db.ForeignKey('Evento.eventID'))
    expedicion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    imagen = db.Column(db.String(100), nullable=False, default='default.jpg')

    def __repr__(self):
        return '<Boleto: {}>'.format(self.folio)

class BoletoSchema(marsh.Schema):
    class Meta:
        fields = ('folio','userID','eventID','expedicion','imagen')

boletoSchema = BoletoSchema()
boletosSchema = BoletoSchema()

#-------------------------------------------------------------------------#

class Registra(db.Model):
    __tablename__ = 'Registra'
    registroID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('Usuario.userID'))
    eventID = db.Column(db.Integer, db.ForeignKey('Evento.eventID'))

    def __repr__(self):
        return '<Registra: {}>'.format(self.registroID)

class RegistraSchema(marsh.Schema):
    class Meta:
        fields = ('registroID','userID','eventID')

#-------------------------------------------------------------------------#

class Rol(db.Model):
    __tablename__ = 'Rol'
    rolID = db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Rol: {}>'.format(self.Nombre)

