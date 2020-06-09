import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify,session
import requests,json
from main import app
from main.forms import RegistrationForm, LoginForm, UpdateAccountForm, EventoForm
from datetime import datetime

@app.route("/")
@app.route("/inicio")
def inicio():
    events = requests.get("http://127.0.0.1:5000/events")
    return render_template('inicio.html')

@app.route("/registrarse", methods=['GET', 'POST'])
def register():
    if "mail" in session:
        return redirect(url_for('inicio'))

    form = RegistrationForm()
    if form.validate_on_submit():
        post_data = {
        'username':form.username.data,
        'nombre':form.nombre.data,
        'mail':form.mail.data,
        'contrasena':form.contrasena.data,
        'telefono':form.telefono.data,
        'edad':form.edad.data,
        'estado':form.estado.data,
        'trabajo':form.trabajo.data,
        }
        response = requests.post("http://127.0.0.1:5000/registrarse",json=post_data)
        if response.status_code == 200:
            return redirect(url_for('login'))
    return render_template('registrarse.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        post_data = {
            'mail':form.mail.data,
            'contrasena':form.contrasena.data
        }
        response = requests.post("http://127.0.0.1:5000/login",json=post_data)
        
        if response.status_code == 200:
            session['mail'] = response.json()['mail']
            session['userID'] = response.json()['userID']
            session['username'] = response.json()['username']
            session['logged_in'] = True
            return redirect(url_for('inicio'))
        else:
            flash('El mail o la contraseña son incorrectos', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session.clear()
    flash('Fin de sesión', 'success')
    return redirect(url_for('inicio'))

#Revisar la integración de S3
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/cuenta", methods=['GET', 'POST'])
def account():
    if "mail" in session:
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
            post_data={
                'username': form.username.data,
                'mail': form.mail.data,
                'userID':session['userID']
            }
            response = requests.post("http://127.0.0.1:5000/cuenta",json=post_data)
            if response.status_code==200:
                session['mail'] = response.json()['mail']
                session['username'] = response.json()['username']
                flash('¡Tus datos se han actualizado con éxito!', 'success')
                return redirect(url_for('cuenta'))
        elif request.method == 'GET':
            form.username.data = session['username']
            form.mail.data = session['mail']
        image_file = url_for('static', filename='profile_pics/default.jpg')
        return render_template('cuenta.html', title='Mi cuenta', image_file=image_file, form=form)
    else:
        return redirect(url_for('login'))

@app.route('/evento/registrar', methods=['GET', 'POST'])
#def new_event():
def crear_evento():
    if "mail" in session:
        form = EventoForm()
        if form.validate_on_submit():
            post_data = {
                'nombre':form.nombre.data,
                'siglas':form.siglas.data,
                'descripcion':form.descripcion.data,
                'duracion':form.duracion.data,
                'asistentes':form.asistentes.data,
                'fechahora':str(form.fechahora.data),
                'costo':form.costo.data,
                'lugar':form.lugar.data,
                'imagen':form.imagen.data,
                'empleado':session['userID']
            }
            response = requests.post("http://127.0.0.1:5000/evento/registrar",json=post_data)
            if response.status_code == 200:
                flash('¡El evento se ha creado con éxito!', 'success')
                return redirect(url_for('inicio'))
        return render_template('registrarEvento.html', title='Registrar evento', form=form)
    else:
        return redirect(url_for('login'))

@app.route('/evento/<int:evento_id>')
def evento(evento_id):
    event = requests.get("http://127.0.0.1:5000/evento/"+str(evento_id)+"/detalles")
    return render_template('evento.html', event=event.json())
    

@app.route('/evento/<int:evento_id>/comprar', methods=['GET', 'POST'])
def comprar_evento(evento_id):
    if "mail" in session:
        response = requests.post("http://127.0.0.1:5000/evento/"+str(evento_id)+"/comprar",json=post_data)
        if response.status_code == 200:
            flash('¡Has conprado tu boleto!', 'success')
            return redirect(url_for('inicio'))
    else:
        return redirect(url_for('login'))

@app.route("/Boletos")
def about():
    if 'mail' in session:
        post_data={
            'userID':session['userID']
        }
        tickets = requests.get("http://127.0.0.1:5000/boleto",json=post_data)
        events = requests.get("http://127.0.0.1:5000/events")

        return render_template('listaBoletos.html', title='Mis Boletos', tickets=tickets.json(), events=events.json())
    return render_template('login.html', title='Login', form=form)

 
@app.route("/evento/<int:evento_id>/archivar", methods=['POST'])
def borrar_evento(evento_id):
    if "mail" in session:
        post_data={
            'userID':session['userID']
        }
        response = requests.post("http://127.0.0.1:5000/evento/"+str(evento_id)+"/archivar",json=post_data)
        if response.status_code ==200:
            flash('¡El evento se ha archivado con éxito!', 'success')
            return redirect(url_for('inicio'))
    else:
        return redirect(url_for('login'))
