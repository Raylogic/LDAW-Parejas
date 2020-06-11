from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateTimeField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, URL, Regexp


class RegistrationForm(FlaskForm):
    username = StringField('Usuario', 
        validators=[DataRequired(message="El nombre de usuario es obligatorio"), 
                    Length(0,30,message="El nombre de usuario no puede superar los 30 caracteres")])
    mail = StringField('Correo',
        validators=[DataRequired(message="El mail es obligatorio"), 
                    Email("El mail no es válido"),
                    Length(0,100,message="El nombre de usuario no puede superar los 100 caracteres")])
    nombre = StringField('Nombre completo',
        validators=[DataRequired(message="El estado es obligatorio"), 
                    Length(0,150,message="El nombre no puede superar los 150 caracteres")])
    telefono = StringField('Teléfono',
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
    contrasena = PasswordField('Contraseña', 
        validators=[DataRequired(message="La contraseña es obligatoria")])
    confirm_password = PasswordField('Confirmar contraseña', 
        validators=[DataRequired(message="La contraseña es obligatoria"), 
                    EqualTo('contrasena',message="Las contraseñas no coinciden")])
    
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    mail = StringField('Mail',
        validators=[DataRequired(message="El mail es obligatorio"), 
                    Email("El mail no es válido")])
    contrasena = PasswordField('Contraseña', 
        validators=[DataRequired(message="La contraseña es obligatoria")])
    remember = BooleanField('Recuerdame')
    
    submit = SubmitField('Ingresar')

class UpdateAccountForm(FlaskForm):
    username = StringField('Usuario', 
        validators=[DataRequired(message="El nombre de usuario es obligatorio"), 
                    Length(0,30,message="El nombre de usuario no puede superar los 30 caracteres")])
    mail = StringField('Correo',
        validators=[DataRequired(message="El mail es obligatorio"), 
                    Email("El mail no es válido"),
                    Length(0,100,message="El nombre de usuario no puede superar los 100 caracteres")])
    submit = SubmitField('Actualizar')

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
        validators=[DataRequired(message="El número de asistentes es obligatorio"),
                    NumberRange(1,200,message="Inserta un número de asistentes válido")])
    costo = IntegerField('Costo', 
        validators=[DataRequired(message="El costo es obligatorio"),
                    NumberRange(1,1000000,message="Inserta un costo válido")])
    lugar = StringField('Lugar', 
        validators=[DataRequired(message="El lugar de trabajo es obligatorio"),
                    Length(0,100,message="El lugar no puede superar los 100 caracteres")])
    fecha = DateField('Fecha-Hora', 
        validators=[DataRequired(message="La fecha es obligatoria")],format='%Y-%m-%d')
    imagen = StringField('Imagen', 
        validators=[DataRequired(message="La imagen es obligatoria"), 
                    URL(require_tld=True,message="Ingresa una URL válida")])
    submit = SubmitField('Registrar Evento')

class BoletoForm(FlaskForm):
    asiento = StringField('Asiento(s)', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad de Boletos (Max. 5)', validators=[DataRequired(), NumberRange(max=8, min=1)])
    submit = SubmitField('Comprar Boleto(s)')






