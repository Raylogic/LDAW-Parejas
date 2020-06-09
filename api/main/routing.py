import os, secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from main import app, db, bcrypt
from main.model import *
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

@app.route('/users', methods=['GET'])
#def get_all_users():
def all_users():
    users = Usuario.query.all()
    result = users_schema.dump(users)
    return jsonify(result)

@app.route('/events', methods=['GET'])
#def get_all_events():
def all_events():
    events = Evento.query.all()
    result = eventosSchema.dump(events)
    return jsonify(result)

#@app.route("/register", methods=['POST'])
@app.route("/registrarse", methods=['POST'])
def register():
    username = request.json['username']
    nombre = request.json['nombres']
    mail = request.json['mail']
    contrasena = request.json['contrasena']
    hashed_password = bcrypt.generate_password_hash(contrasena).decode('utf-8')
    telefono = request.json['telefono']
    edad = request.json['edad']
    estado = request.json['estado']
    trabajo = request.json['trabajo']
 
    user = Usuario(
        username=username, 
        nombre=nombre,
        mail=mail, 
        contrasena=hashed_password, 
        telefono=telefono, 
        edad=edad, 
        estado=estado, 
        trabajo=trabajo
    )
    db.session.add(user)
    db.session.commit()
       
    return jsonify({'message':'¡El usuario se ha registrado con éxito!'},200)

@app.route('/evento/registrar', methods=['POST'])
#def new_event():
def crear_evento():
    nombre = request.json['nombre']
    siglas = request.json['siglas']
    descripcion = request.json['descripcion']
    duracion = request.json['duracion']
    asistentes = request.json['asistentes']
    fechahora = request.json['fechahora']
    costo = request.json['costo']
    lugar = request.json['lugar']
    imagen = request.json['imagen']

    format = '%Y-%m-%d %H:%M:%S' 
    fechaoficial = datetime.strptime(fechahora, format) 
    
    event = Evento(
        nombre=nombre, 
        siglas=siglas, 
        descripcion=descripcion, 
        duracion=duracion, 
        asistentes=asistentes, 
        fechahora=fechaoficial, 
        costo=costo, 
        lugar=lugar, 
        imagen=imagen
    )
    db.session.add(event)
    db.session.commit()

    return jsonify({'message':'¡El evento se ha registrado exitosamente!'},200)

@app.route('/evento/<int:evento_id>/detalles',methods=['GET'])
#def evento(evento_id):
def ver_evento(evento_id):
    event = Evento.query.get_or_404(evento_id)
    result = eventoSchema.dump(event)
    return jsonify(result)

@app.route("/evento/<int:evento_id>/archivar", methods=['POST'])
def archivar_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)
    userID = request.json['userID']
    usuario = Usuario.query.get_or_404(user_id)

    if evento.userID != usuario.userID:
        abort(403)
    db.session.delete(evento)
    db.session.commit()

    return jsonify({'message':'¡El evento se ha archivado con éxito'},200)

@app.route('/evento/<int:evento_id>/comprar', methods=['POST'])
def comprar_evento(evento_id):
    event = Evento.query.get_or_404(evento_id)
    if(event):
        userID = request.json['userID']
        eventID = evento_id
        boleto = Boleto(userID=userID, eventID=evento_id)
        event.asistentes=(asistentes.Cupo - 1)

        db.session.add(boleto)
        db.session.commit()
        return jsonify({'message':'¡Te has registrado al evento!'},200)

#@app.route("/boletos", methods=['GET'])
@app.route("/boleto", methods=['GET'])
def boletos():
    userID = request.json['userID']
    boleto = Boleto.query.filter_by(userID=int(userID)).all()
    evento = Evento.query.all()

    result_tickets = boletosSchema.dump(boleto)
    result_events = eventosSchema.dump(evento)
    return jsonify(result_tickets)


@app.route("/login", methods=['POST'])
def login():
    mail = request.json['mail']
    contrasena = request.json['contrasena']
    usuario = Usuario.query.filter_by(mail=mail).first()
    if usuario and bcrypt.check_password_hash(usuario.password,password):
        return {
            'message': 'Acceso permitido',
                'Mail':str(mail), 
                'ID':int(usuario.id), 
                'Username':str(usuario.username)
        }, 200

#@app.route("/account", methods=['POST'])
@app.route("/cuenta", methods=['POST'])
def account():
    username = request.json['username']
    mail = request.json['mail']
    userID = request.json['userID']
  
    user = Usuario.query.get_or_404(user_id)
    user.username = username
    user.mail = mail
    db.session.commit()

    return {
        'message': 'Successful updated','email':str(email), 'username':str(user.username)
    }, 200

    
@app.route('/user/delete', methods=['GET', 'POST'])
def borrar_usuario():
    Usuario.query.filter_by(id=2).delete()
    db.session.commit()
    flash('¡La cuenta se ha eliminado con éxito!', 'success')
    return redirect(url_for('home'))
