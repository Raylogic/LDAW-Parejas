import os
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from main import app, db, bcrypt
from main.models import *
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result)

@app.route('/events', methods=['GET'])
def get_all_events():
    events = Evento.query.all()
    result = eventosSchema.dump(events)
    return jsonify(result)


@app.route("/register", methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    nombreCompleto = request.json['nombreCompleto']
    numTelefono = request.json['numTelefono']
    edad = request.json['edad']
    residencia = request.json['residencia']
    empresa = request.json['empresa']

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    user = User(username=username, email=email,password=hashed_password, nombreCompleto=nombreCompleto, numTelefono=numTelefono, edad=edad, residencia=residencia, empresa=empresa)
    db.session.add(user)
    db.session.commit()
       
    return jsonify({'message':'The user has been registered!'},200)

@app.route('/evento/registrar', methods=['POST'])
def new_event():

    Nombre = request.json['Nombre']
    Siglas = request.json['Siglas']
    Decripcion = request.json['Descripcion']
    Duracion = request.json['Duracion']
    Cupo = request.json['Cupo']
    Costo = request.json['Costo']
    Lugar = request.json['Lugar']
    Fecha = request.json['Fecha']
    imagen = request.json['imagen']
    user_id = request.json['empleado']

    format = '%Y-%m-%d' 
    datetime_str = datetime.strptime(Fecha, format) 
    
    event = Evento(Nombre=Nombre, Siglas=Siglas, Decripcion=Decripcion, Duracion=Duracion, Cupo=Cupo, Costo=Costo, Lugar=Lugar, Fecha=datetime_str, imagen=imagen, user_id=user_id)
    db.session.add(event)
    db.session.commit()

    return jsonify({'message':'The event has been registered!'},200)

@app.route('/evento/<int:evento_id>',methods=['GET'])
def evento(evento_id):
    event = Evento.query.get_or_404(evento_id)
    result = eventoSchema.dump(event)
    return jsonify(result)

@app.route('/evento/comprar/<int:evento_id>', methods=['POST'])
def comprar_evento(evento_id):
    event = Evento.query.get_or_404(evento_id)
    if(event):
        cantidad = request.json['cantidad']
        user_id = request.json['user_id']
        idEvento=evento_id

        boleto = Boleto(cantidad=cantidad, user_id=user_id, idEvento=evento_id)
        
        event.Cupo=(event.Cupo - cantidad)
        db.session.add(boleto)
        db.session.commit()
        return jsonify({'message':'The event has been bought!'},200)

@app.route("/boletos", methods=['GET'])
def boletos():
    user_id = request.json['user_id']
    tickets = Boleto.query.filter_by(user_id=int(user_id)).all()
    events = Evento.query.all()

    result_tickets = boletosSchema.dump(tickets)
    result_events = eventosSchema.dump(events)


    return jsonify(result_tickets)

@app.route("/evento/<int:evento_id>/borrar", methods=['POST'])
def borrar_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)

    user_id = request.json['user_id']
    user = User.query.get_or_404(user_id)

    if evento.user_id != user.id:
        abort(403)
    db.session.delete(evento)
    db.session.commit()

    return jsonify({'message':'The event has been deleted!'},200)

@app.route("/login", methods=['POST'])
def login():

    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password,password):

        return {
                'message': 'Successful logged in','email':str(email), 'id':int(user.id), 'username':str(user.username)
            }, 200

    
@app.route("/account", methods=['POST'])
def account():
    username = request.json['username']
    email = request.json['email']
    user_id = request.json['user_id']
  
    user = User.query.get_or_404(user_id)
    user.username = username
    user.email = email
    db.session.commit()

    return {
                'message': 'Successful updated','email':str(email), 'username':str(user.username)
            }, 200

    
@app.route('/user/delete', methods=['GET', 'POST'])
def borrar_usuario():
    User.query.filter_by(id=2).delete()
    db.session.commit()
    flash('Cuenta borrada exitosamente', 'success')
    return redirect(url_for('home'))













