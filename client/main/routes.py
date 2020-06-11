import os
from flask import render_template, url_for, flash, redirect, request, abort, jsonify,session
import requests,json
from main import app
from main.forms import RegistrationForm, LoginForm, UpdateAccountForm, EventoForm, BoletoForm
from datetime import datetime

@app.route("/")
@app.route("/home")
def home():
    events = requests.get("http://127.0.0.1:5000/events")
    return render_template('home.html', events=events.json())

@app.route("/register", methods=['GET', 'POST'])
def register():
    if "mail" in session:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        post_data = {
        'username': form.username.data,
        'mail':form.mail.data,
        'contrasena':form.contrasena.data,
        'nombre':form.nombre.data,
        'telefono':form.telefono.data,
        'edad':form.edad.data,
        'estado':form.estado.data,
        'trabajo':form.trabajo.data,
        }
        response = requests.post("http://127.0.0.1:5000/register",json=post_data)
        if response.status_code == 200:
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


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
            session['user_id'] = response.json()['userID']
            session['username'] = response.json()['username']
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('El mail o la contraseña son incorrectos', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    session.clear()
    flash('¡Fuera del sistema!', 'success')
    return redirect(url_for('home'))

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

@app.route("/account", methods=['GET', 'POST'])
def account():
    if "mail" in session:
        
        form = UpdateAccountForm()
        if form.validate_on_submit():

            post_data={
                'username': form.username.data,
                'mail': form.mail.data,
                'user_id':session['user_id']
            }
            response = requests.post("http://127.0.0.1:5000/account",json=post_data)
            if response.status_code==200:
                session['mail'] = response.json()['mail']
                session['username'] = response.json()['username']
                flash('¡Tu cuenta se ha actualizado!', 'success')
                return redirect(url_for('account'))
        elif request.method == 'GET':
            form.username.data = session['username']
            form.mail.data = session['mail']
        return render_template('account.html', title='Account', form=form)
    else:
        return redirect(url_for('login'))

@app.route('/evento/registar', methods=['GET', 'POST'])
def new_event():
    if "mail" in session:
        form = EventoForm()
        if form.validate_on_submit():
            post_data = {
                'nombre':form.nombre.data,
                'siglas':form.siglas.data,
                'descripcion':form.descripcion.data,
                'duracion':form.duracion.data,
                'asistentes':form.asistentes.data,
                'costo':form.costo.data,
                'lugar':form.lugar.data,
                'fecha':str(form.fecha.data),
                'imagen':form.imagen.data,
                'empleado':session['user_id']
            }
            response = requests.post("http://127.0.0.1:5000/evento/registrar",json=post_data)
            if response.status_code == 200:
                flash('¡Se ha creado el evento!', 'success')
                return redirect(url_for('home'))
        return render_template('registrar_evento.html', title='Registrar Nuevo Evento', form=form)
    else:
        return redirect(url_for('login'))

@app.route('/evento/<int:evento_id>')
def evento(evento_id):
    event = requests.get("http://127.0.0.1:5000/evento/"+str(evento_id))
    return render_template('evento.html', event=event.json())

@app.route('/evento/comprar/<int:evento_id>', methods=['GET', 'POST'])
def comprar_evento(evento_id):
    if "mail" in session:
        form = BoletoForm()
        if form.validate_on_submit():
            post_data={
                'cantidad':form.cantidad.data,
                'user_id': session['user_id'],
            }
            response = requests.post("http://127.0.0.1:5000/evento/comprar/"+str(evento_id),json=post_data)
            if response.status_code == 200:
                flash('¡Has comprado un boleto!', 'success')
                return redirect(url_for('home'))
        else:
            event = requests.get("http://127.0.0.1:5000/evento/"+str(evento_id))
            return render_template('boleto.html', event=event.json(),form=form)
    else:
        return redirect(url_for('login'))

@app.route("/Boletos")
def about():
    if 'mail' in session:
        post_data={
            'user_id':session['user_id']
        }
        tickets =  requests.get("http://127.0.0.1:5000/boletos",json=post_data)
        events = requests.get("http://127.0.0.1:5000/events")

        return render_template('about.html', title='Mis Boletos', tickets=tickets.json(), events=events.json())
    return render_template('login.html', title='Login', form=form)

 
@app.route("/evento/<int:evento_id>/borrar", methods=['POST'])
def borrar_evento(evento_id):
    if "mail" in session:
        post_data={
            'user_id': session['user_id']
        }
        response = requests.post("http://127.0.0.1:5000/evento/"+str(evento_id)+"/borrar",json=post_data)
        if response.status_code ==200:
            flash('¡El evento se ha eliminado con éxito!', 'success')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
