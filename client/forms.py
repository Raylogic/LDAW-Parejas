from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DateTimeField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, URL, Regexp
from main.models import User

class RegistrationForm(FlaskForm):
    nombre = StringField('Nombre completo',
        validators=[DataRequired(message="El estado es obligatorio"), 
                    Length(0,150,message="El nombre no puede superar los 150 caracteres")])
    telefono = IntegerField('Teléfono',
        validators=[DataRequired(message="El teléfono es obligatorio"), 
                    Length(10,10,message="El número de teléfono debe ser de 10 dígitos")])
    edad = IntegerField('Edad', 
        validators=[DataRequired(message="La edad es obligatoria"), 
                    NumberRange(1,120,message="Inserta una edad válida")])
    estado = StringField('Estado de procedencia',
        validators=[DataRequired(message="El estado de procedencia es obligatorio"),
                    Length(0,50,message="El estado no puede superar los 50 caracteres")])
    trabajo = StringField('Lugar de trabajo', 
        validators=[DataRequired(message="El lugar de trabajo es obligatorio"),
                    Length(0,100,message="El estado no puede superar los 100 caracteres")])

    username = StringField('Usuario', 
        validators=[DataRequired(message="El nombre de usuario es obligatorio"), 
                    Length(0,30,message="El nombre de usuario no puede superar los 30 caracteres")])
    email = StringField('Correo',
        validators=[DataRequired(message="El mail es obligatorio"), 
                    Email("El mail no es válido"),
                    Length(0,100,message="El nombre de usuario no puede superar los 100 caracteres")])
    password = PasswordField('Contraseña', 
        validators=[DataRequired(message="La contraseña es obligatoria")
                    Regexp('^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[*.!@$%^&()[]:;<>,.?/~_+-=|\]).{8,20}$',message="La contraseña debe tener 8-20 caracteres y al menos una letra minúscula, mayúscula, número y caracter especial.")])
    confirm_password = PasswordField('Confirmar contraseña', 
        validators=[DataRequired(message=), 
                    EqualTo('password',message="Las contraseñas no coinciden")])

    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ya existe una cuenta con ese nombre de usuario. Intenta con otro')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ya existe una cuenta con ese correo. Intenta con otro')

class LoginForm(FlaskForm):
    email = StringField('Mail',
        validators=[DataRequired(message=), Email()])
    password = PasswordField('Contraseña', 
        validators=[DataRequired(message=)])
    remember = BooleanField('Recuérdame')
    
    submit = SubmitField('Ingresar')

class UpdateAccountForm(FlaskForm):
    username = StringField('Usuario', 
        validators=[DataRequired(message="El nombre de usuario es obligatorio"), 
                    Length(0,30,message="El nombre de usuario no puede superar los 30 caracteres")])
    email = StringField('Correo',
        validators=[DataRequired(message="El mail es obligatorio"), 
                    Email("El mail no es válido"),
                    Length(0,100,message="El nombre de usuario no puede superar los 100 caracteres")])
    picture = FileField('Foto de Perfil', 
        validators=[FileAllowed(['jpg','png'])])

    submit = SubmitField('Actualizar')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Ya existe una cuenta con ese nombre de usuario. Intenta con otro')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Ya existe una cuenta con ese correo. Intenta con otro')

class EventoForm(FlaskForm):
    nombre = StringField('Nombre del evento', 
        validators=[DataRequired(message="El nombre es obligatorio"),
                    Length(0,50,message="El nombre del evento no puede superar los 50 caracteres")])
    siglas = StringField('Siglas', 
        validators=[DataRequired(message="Las siglas son obligatorias"),
                    Length(0,10,message="Las siglas no puede superar los 10 caracteres")])
    descripcion = TextAreaField('Descripción', 
        validators=[DataRequired(message="La descripción es obligatoria"),
                    Length(0,1000,message="La descripción no puede superar los 1000 caracteres")])
    duracion = IntegerField('Duración (minutos)', 
        validators=[DataRequired(message="La duración es obligatoria"),
                    NumberRange(1,1440,message="Inserta una duración válida")])
    asistentes = IntegerField('Numero de asistentes', 
        validators=[DataRequired(message=),
                    NumberRange(1,200,message="Inserta un número de asistentes válido")])
    fechahora = DateTimeField('Fecha-Hora', 
        validators=[DataRequired(message="La fecha es obligatoria")],format='%Y-%m-%d %H:%M:%S')
    costo = IntegerField('Costo', 
        validators=[DataRequired(message="El costo es obligatorio"),
                    NumberRange(1,1000000,message="Inserta un costo válido")])
    lugar= StringField('Lugar', 
        validators=[DataRequired(message="El lugar de trabajo es obligatorio"),
                    Length(0,100,message="El lugar no puede superar los 100 caracteres")])
    imagen = StringField('Imagen', 
        validators=[DataRequired(message="La imagen es obligatoria"), 
                    URL(require_tld=True,message="Ingresa una URL válida")])

    submit = SubmitField('Registrar Evento')

