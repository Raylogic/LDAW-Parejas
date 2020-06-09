from main import db, login_manager, marsh
from datetime import datetime
from marshmallow import fields
from flask_login import UserMixin

@login_manager.user_loader
def cargar_usuario(userID):
    return Usuario.query.get(int(userID))

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
    userID = db.Column(db.Integer, db.ForeignKey('Usuario.userID'))

    boleto = db.relationship('Usuario', secondary='Boleto')
    
    def __repr__(self):
        return f"Evento('{self.nombre}')"

class EventoSchema(marsh.Schema):
    class Meta:
        fields=('eventID','nombre','siglas','descripcion','duracion','asistentes','fechahora','costo','lugar','imagen','activo')

eventoSchema = EventoSchema()
eventosSchema = EventoSchema(many=True)

#------------------------------------------------------------------------------#

class Usuario(db.Model, UserMixin):
    __tablename__ = 'Usuario'
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    trabajo = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Integer, default=1)
    #eventos = db.relationship('Evento', backref='empleado', lazy =True)
    
    registra = db.relationship('Evento', secondary='Registra')
    boleto = db.relationship('Evento', secondary='Boleto')

    def __repr__(self):
        return f"Usuario('{self.username}')"

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

#------------------------------------------------------------------------------#

class Boleto(db.Model):
    __tablename__ = 'Boleto'
    folio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('Usuario.userID'))
    eventID = db.Column(db.Integer, db.ForeignKey('Evento.eventID'))
    expedicion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    imagen = db.Column(db.String(100), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Boleto('{self.folio}')"

class BoletoSchema(marsh.Schema):
    class Meta:
        fields = ('folio','userID','eventID','expedicion','imagen')

boletoSchema = BoletoSchema()
boletosSchema = BoletoSchema(many=True)
