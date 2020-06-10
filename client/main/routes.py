import os
from flask import render_template, url_for, flash, redirect, request, abort, jsonify,session
import requests,json
from main import app
from main.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, EventoForm, BoletoForm
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    events = requests.get("http://127.0.0.1:5000/events")
    return render_template('home.html', events=events.json())

@app.route("/register", methods=['GET', 'POST'])
def register():
    if "email" in session:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        post_data = {
        'username': form.username.data,
        'email':form.email.data,
        'password':form.password.data,
        'nombreCompleto':form.nombreCompleto.data,
        'numTelefono':form.numTelefono.data,
        'edad':form.edad.data,
        'residencia':form.residencia.data,
        'empresa':form.empresa.data,
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
            'email':form.email.data,
            'password':form.password.data
        }
        response = requests.post("http://127.0.0.1:5000/login",json=post_data)
        
        if response.status_code == 200:
         
            session['email'] = response.json()['email']
            session['user_id'] = response.json()['id']
            session['username'] = response.json()['username']
            session['logged_in'] = True
            

            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    session.clear()
    flash('Ha cerrado sesion exitosamente', 'success')
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
    if "email" in session:
        
        form = UpdateAccountForm()
        if form.validate_on_submit():

            if form.picture.data:
                picture_file = save_picture(form.picture.data)

            post_data={
                'username': form.username.data,
                'email': form.email.data,
                'user_id':session['user_id']
            }
            response = requests.post("http://127.0.0.1:5000/account",json=post_data)
            if response.status_code==200:
                session['email'] = response.json()['email']
                session['username'] = response.json()['username']
                flash('Your account has been updated!', 'success')
                return redirect(url_for('account'))
        elif request.method == 'GET':
            form.username.data = session['username']
            form.email.data = session['email']
        image_file = url_for('static', filename='profile_pics/default.jpg')
        return render_template('account.html', title='Account',
                            image_file=image_file, form=form)
    else:
        return redirect(url_for('login'))

@app.route('/evento/registar', methods=['GET', 'POST'])
def new_event():
    if "email" in session:
        form = EventoForm()
        if form.validate_on_submit():
            post_data = {
                'Nombre':form.nombre.data,
                'Siglas':form.siglas.data,
                'Descripcion':form.descripcion.data,
                'Duracion':form.duracion.data,
                'Cupo':form.asistentes.data,
                'Costo':form.costo.data,
                'Lugar':form.lugar.data,
                'Fecha':str(form.fecha.data),
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
    if "email" in session:
        form = BoletoForm()
        if form.validate_on_submit():
            post_data={
                'cantidad':form.cantidad.data,
                'user_id': session['user_id'],
            }
            response = requests.post("http://127.0.0.1:5000/evento/comprar/"+str(evento_id),json=post_data)
            if response.status_code == 200:
                flash('¡Se ha realizado la compra!', 'success')
                return redirect(url_for('home'))
        else:
            event = requests.get("http://127.0.0.1:5000/evento/"+str(evento_id))
            return render_template('boleto.html', event=event.json(),form=form)
    else:
        return redirect(url_for('login'))

@app.route("/Boletos")
def about():
    if 'email' in session:
        post_data={
            'user_id':session['user_id']
        }
        tickets =  requests.get("http://127.0.0.1:5000/boletos",json=post_data)
        events = requests.get("http://127.0.0.1:5000/events")

        return render_template('about.html', title='Mis Boletos', tickets=tickets.json(), events=events.json())
    return render_template('login.html', title='Login', form=form)

 
@app.route("/evento/<int:evento_id>/borrar", methods=['POST'])
def borrar_evento(evento_id):
    if "email" in session:
        post_data={
            'user_id': session['user_id']
        }
        response = requests.post("http://127.0.0.1:5000/evento/"+str(evento_id)+"/borrar",json=post_data)
        if response.status_code ==200:
            flash('¡El evento ha sido eliminado con éxito!', 'success')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))














