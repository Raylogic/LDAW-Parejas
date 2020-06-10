from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, URL, Regexp


class RegistrationForm(FlaskForm):
    username = StringField('Usuario', 
                            validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Correo',
                            validators=[DataRequired(), Email()])
    nombreCompleto = StringField('Nombre Completo',validators=[DataRequired()] )
    numTelefono = StringField('Telefono',validators=[DataRequired(), Regexp('\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',message="Ingresa un telefono válido")])
    edad = IntegerField('Edad', validators=[DataRequired()])
    residencia = StringField('Lugar de Residencia',validators=[DataRequired()] )
    empresa = StringField('Empresa', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', 
                            validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Registrarse')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('Ya existe una cuenta con ese nombre de usuario. Intenta con otro')
    
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('Ya existe una cuenta con ese correo. Intenta con otro')

class LoginForm(FlaskForm):
    email = StringField('Correo Electronico',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuerdame')
    
    submit = SubmitField('Ingresar')

class UpdateAccountForm(FlaskForm):
    username = StringField('Usuario', 
                            validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Correo Electronico',
                            validators=[DataRequired(), Email()])

    picture = FileField('Actualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Actualizar')

    # def validate_username(self, username):
    #     if username.data != current_user.username:
    #         user = User.query.filter_by(username=username.data).first()
    #         if user:
    #             raise ValidationError('Ya existe una cuenta con ese nombre de usuario. Intenta con otro')
    
    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         user = User.query.filter_by(email=email.data).first()
    #         if user:
    #             raise ValidationError('Ya existe una cuenta con ese correo. Intenta con otro')

class PostForm(FlaskForm):
    title= StringField('Nombre', validators=[DataRequired()])
    content = TextAreaField('Descripcion', validators=[DataRequired()])
    submit = SubmitField('Registrar Evento')

class EventoForm(FlaskForm):
    nombre= StringField('Nombre del evento', validators=[DataRequired()])
    siglas= StringField('Siglas', validators=[DataRequired()])
    descripcion= TextAreaField('Descripción', validators=[DataRequired()])
    duracion= StringField('Duración (minutos)', validators=[DataRequired()])
    asistentes= IntegerField('Numero de asistentes', validators=[DataRequired()])
    costo= IntegerField('Costo (número entero)', validators=[DataRequired()])
    lugar= StringField('Lugar', validators=[DataRequired()])
    fecha = DateField('Fecha', validators=[DataRequired()],format='%Y-%m-%d')
    imagen = StringField('Imagen', validators=[DataRequired(), URL(require_tld=True, message="Ingresa una URL valida.")])
    submit = SubmitField('Registrar Evento')

class BoletoForm(FlaskForm):
    asiento = StringField('Asiento(s)', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad de Boletos (Max. 5)', validators=[DataRequired(), NumberRange(max=8, min=1)])
    #cantidad = SelectField('cantidad', choices = [(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')])
    submit = SubmitField('Comprar Boleto(s)')






