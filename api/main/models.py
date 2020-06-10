from main import db, login_manager, marsh
from datetime import datetime
from flask_login import UserMixin
from marshmallow import fields

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class EventoSchema(marsh.Schema):
    class Meta:
        fields=('idEvento','Nombre','Siglas','Descripcion','Duracion','Cupo','Costo','Lugar','Fecha','imagen','user_id')

eventoSchema = EventoSchema()
eventosSchema = EventoSchema(many=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), unique=True, nullable=False)
    email= db.Column(db.String(120), unique=True, nullable=False)
    nombreCompleto = db.Column(db.String(150))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    numTelefono = db.Column(db.String(20))
    edad = db.Column(db.Integer)
    residencia = db.Column(db.String(70))
    empresa = db.Column(db.String(20))
    posts = db.relationship('Post', backref='author', lazy=True)
    eventos = db.relationship('Evento', backref='empleado', lazy =True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}',{self.id})"

# class UserSchema(marsh.Schema):
#     class Meta:
#         model:User
#         fields = ('id','username','email','nombreCompleto','image_file','password','numTelefono','edad','residencia','empresa','eventos')
#         eventos = marsh.Nested(EventoSchema)

class UserSchema(marsh.Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    nombreCompleto = fields.String()
    image_file = fields.String()
    password = fields.String()
    numTelefono = fields.String()
    edad = fields.Integer()
    residencia = fields.String()
    empresa = fields.String()
    eventos = fields.Nested(EventoSchema)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

class PostSchema(marsh.Schema):
    class Meta:
        fields = ('id','title','date_posted','content','user_id')

class Evento(db.Model):
    idEvento = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Siglas = db.Column(db.String(30), nullable=False)
    Decripcion = db.Column(db.String(500), nullable=False)
    Duracion = db.Column(db.String(50), nullable=False)
    Cupo = db.Column(db.Integer, nullable=False)
    Costo = db.Column(db.Integer, nullable=False)
    Lugar = db.Column(db.String(100), nullable=False)
    Fecha = db.Column(db.DateTime,nullable=False)
    imagen = db.Column(db.String(50), nullable=False, default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"Evento('{self.Nombre}','{self.Descripcion}','{self.Lugar}')"



class Boleto(db.Model):
    folio = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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