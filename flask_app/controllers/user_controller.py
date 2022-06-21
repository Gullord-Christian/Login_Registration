from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if User.validate_session():
        return redirect ("/dashboard")
    else:
        return render_template("index.html")

@app.route('/register/user', methods=['POST'])
def register_user():
    if  not User.validate_registration(request.form):
        return redirect("/")
    data = {
        "email" : request.form['email']
    }
    ## before creating user we need to validate the email does not exist
    result = User.get_one(data)
    ## if not it will create the user
    if result:
        flash("That email already exists.", "error_email")
        return redirect("/")
    data = {
        "email" : request.form['email'],
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        ## this is storing the password in the database as a hashed password
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    ## calling create method on User
    session ['user_id'] = User.create(data)
    ## storing user email, first name, last name into session

    return redirect("/dashboard")



@app.route('/login', methods=["POST"])
def user_login():
    data = {
        "email" : request.form ['email']
    }
    result = User.get_one (data)
    ## if result is none , email doesnt exist
    if not result:
        flash("Wrong credentials.", "error_login_email")
        return redirect("/")
        ## validating the password being submitted matches the password on file
    if not bcrypt.check_password_hash(result.password, request.form['password']):
        return redirect('/')

    session ['user_id'] = result.id

    return redirect('/dashboard')


@app.route('/dashboard')
def display():
    if User.validate_session():
        data = {
        "id" : session["user_id"]
        }
        return render_template('dashboard.html', user=User.get_one_by_id (data))
    else:
        return redirect ('/')

@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect('/')