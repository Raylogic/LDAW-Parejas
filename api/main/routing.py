import os, secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from main import app, db, bcrypt
from main.model import *

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
    
    user = User(username, email,hashed_password, nombreCompleto, numTelefono, edad, residencia, empresa)
    db.session.add(user)
    db.session.commit()
       
    return jsonify({'message':'The user has been registered!'},200)

@app.route('/evento/registar', methods=['POST'])
def new_event():

    Nombre = request.json['nombre']
    Siglas = request.json['siglas']
    Decripcion = request.json['descripcion']
    Duracion = request.json['duracion']
    Cupo = request.json['asistentes']
    Costo = request.json['costo']
    Lugar = request.json['lugar']
    Fecha = request.json['fecha']
    imagen = request.json['imagen']
    empleado = request.json['user_id']
    
    event = Evento(Nombre, Siglas, Decripcion, Duracion, Cupo, Costo, Lugar, Fecha, imagen, empleado)
    db.session.add(event)
    db.session.commit()

    return jsonify({'message':'The event has been registered!'})

@app.route('/evento/<int:evento_id>',methods=['GET'])
def evento(evento_id):
    #evento_id = request.json['evento_id']
    event = Evento.query.get_or_404(evento_id)
    return jsonify(event)

@app.route('/evento/comprar/<int:evento_id>', methods=['POST'])
def comprar_evento(evento_id):
    #evento_id = request.json['evento_id']
    event = Evento.query.get_or_404(evento_id)

    asiento = request.json['asiento']
    cantidad = request.json['cantidad']
    user_id = request.json['user_id']

    boleto = Boleto(asiento,cantidad,user_id,idEvento=evento_id)
    
    event.Cupo=(event.Cupo - cantidad)
    db.session.add(boleto)
    db.session.commit()
    return jsonify({'message':'The event has been registered!'})

@app.route("/boletos", methods=['GET'])
def boletos():
    user_id = request.json['user_id']
    tickets = Boleto.query.filter_by(user_id=user_id).all()
    events = Evento.query.all()

    result_tickets = boletosSchema.dump(tickets)
    result_events = eventosSchema.dump(events)

    return jsonify({"tickets":result_tickets, "events":result_events})

@app.route("/evento/<int:evento_id>/borrar", methods=['POST'])
def borrar_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)

    user_id = request.json['user_id']
    user = User.query.filter_by(user_id).all()

    if evento.empleado != user:
        abort(403)
    db.session.delete(evento)
    db.session.commit()

    return jsonify({'message':'The event has been deleted!'})

@app.route("/login", methods=['POST'])
def login():

    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password,password):

        return {
                'message': 'Successful logged in','email':str(email), 'id':int(user.id)
            }, 200

    

 
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', title='Login', form=form)


# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('home'))

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
    users = User.query.all()
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form,users=users)

@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='Registrar Nuevo Evento', form=form, legend='Registrar Nuevo Evento')



@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Editar Evento', form=form, legend='Editar Evento')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/user/delete', methods=['GET', 'POST'])
def borrar_usuario():
    User.query.filter_by(id=2).delete()
    db.session.commit()
    flash('Cuenta borrada exitosamente', 'success')
    return redirect(url_for('home'))