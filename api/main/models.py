from main import db, login_manager, marsh
from datetime import datetime
from flask_login import UserMixin
from marshmallow import fields

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Evento(db.Model):
    eventID = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    siglas = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    duracion = db.Column(db.String(50), nullable=False)
    asistentes = db.Column(db.Integer, nullable=False)
    costo = db.Column(db.Integer, nullable=False)
    lugar = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime,nullable=False)
    imagen = db.Column(db.String(50), nullable=False, default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.userID'))
    
    def __repr__(self):
        return f"Evento('{self.nombre}','{self.descripcion}','{self.lugar}')"

class EventoSchema(marsh.Schema):
    class Meta:
        fields=('eventID','nombre','siglas','descripcion','duracion','asistentes','costo','lugar','fecha','imagen','user_id')

eventoSchema = EventoSchema()
eventosSchema = EventoSchema(many=True)

#------------------------------------------------------------------------------------------

class Usuario(db.Model, UserMixin):
    userID = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(30), unique=True, nullable=False)
    mail= db.Column(db.String(100), unique=True, nullable=False)
    nombre = db.Column(db.String(150))
    contrasena = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(10))
    edad = db.Column(db.Integer)
    estado = db.Column(db.String(50))
    trabajo = db.Column(db.String(100))
    eventos = db.relationship('Evento', backref='empleado', lazy =True)

    def __repr__(self):
        return f"Usuario('{self.username}','{self.mail}','{self.foto}',{self.userID})"

class UserSchema(marsh.Schema):
    userID = fields.Integer()
    username = fields.String()
    mail = fields.String()
    nombre = fields.String()
    foto = fields.String()
    contrasena = fields.String()
    telefono = fields.String()
    edad = fields.Integer()
    estado = fields.String()
    trabajo = fields.String()
    eventos = fields.Nested(EventoSchema)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

#------------------------------------------------------------------------------------------

class Boleto(db.Model):
    folio = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.userID'))
    eventID = db.Column(db.Integer, db.ForeignKey('evento.eventID'))
    Fecha = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    cantidad = db.Column(db.Integer)
    imagen = db.Column(db.String(50), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Boleto('{self.folio}','{self.Fecha}','{self.cantidad}'"

class BoletoSchema(marsh.Schema):
    class Meta:
        fields = ('folio','user_id','eventID','Fecha','cantidad','imagen')

boletoSchema = BoletoSchema()
boletosSchema = BoletoSchema(many=True)