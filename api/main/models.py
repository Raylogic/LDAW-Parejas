from main import db, login_manager, marsh
from datetime import datetime
from flask_login import UserMixin
from marshmallow import fields

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Evento(db.Model):
    idEvento = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Siglas = db.Column(db.String(30), nullable=False)
    Descripcion = db.Column(db.String(500), nullable=False)
    Duracion = db.Column(db.String(50), nullable=False)
    Cupo = db.Column(db.Integer, nullable=False)
    Costo = db.Column(db.Integer, nullable=False)
    Lugar = db.Column(db.String(100), nullable=False)
    Fecha = db.Column(db.DateTime,nullable=False)
    imagen = db.Column(db.String(50), nullable=False, default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    
    def __repr__(self):
        return f"Evento('{self.Nombre}','{self.Descripcion}','{self.Lugar}')"

class EventoSchema(marsh.Schema):
    class Meta:
        fields=('idEvento','Nombre','Siglas','Descripcion','Duracion','Cupo','Costo','Lugar','Fecha','imagen','user_id')

eventoSchema = EventoSchema()
eventosSchema = EventoSchema(many=True)

#------------------------------------------------------------------------------------------

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(30), unique=True, nullable=False)
    mail= db.Column(db.String(100), unique=True, nullable=False)
    nombre = db.Column(db.String(150))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(10))
    edad = db.Column(db.Integer)
    estado = db.Column(db.String(50))
    trabajo = db.Column(db.String(100))
    eventos = db.relationship('Evento', backref='empleado', lazy =True)

    def __repr__(self):
        return f"Usuario('{self.username}','{self.mail}','{self.image_file}',{self.id})"

class UserSchema(marsh.Schema):
    id = fields.Integer()
    username = fields.String()
    mail = fields.String()
    nombre = fields.String()
    image_file = fields.String()
    password = fields.String()
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
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    idEvento = db.Column(db.Integer, db.ForeignKey('evento.idEvento'))
    Fecha = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    cantidad = db.Column(db.Integer)
    imagen = db.Column(db.String(50), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Boleto('{self.folio}','{self.Fecha}','{self.cantidad}'"

class BoletoSchema(marsh.Schema):
    class Meta:
        fields = ('folio','user_id','idEvento','Fecha','cantidad','imagen')

boletoSchema = BoletoSchema()
boletosSchema = BoletoSchema(many=True)