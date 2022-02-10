from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.court import Court

@app.route("/")
def welcome_page():
    return render_template("index.html")

@app.route("/registration")
def register_login():
    if "user_id" in session:
        return redirect("/logout")
    return render_template("registration.html")

@app.route("/register", methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect("/registration")
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password']),
        "birthday" : request.form['birthday'],
        "level" : request.form['level'],
        "gender" : request.form['gender']
    }
    user_id = User.save_user(data)
    session['user_id'] = user_id
    return redirect("/user_dashboard")

@app.route("/login", methods = ['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect("/registration")
    user_from_db = User.get_by_email(request.form)
    session['user_id'] = user_from_db.id

    return redirect("/user_dashboard")

# @app.route("/user_page")
# def show_user():
#     if "user_id" not in session:
#         flash("Please register/login before continuing!")
#         return redirect("/")
#     data = {
#         "user_id" : session['user_id']
#     }
#     one_user = User.get_user_by_id(data)

#     return render_template("show_user.html", one_user = one_user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/favorite_court/<int:court_id>")
def favorite_court(court_id):
    data = {
        "user_id" : session['user_id'],
        "court_id" : court_id
    }
    fav_court = User.fav_court(data)
    return redirect("/user_dashboard")

@app.route("/user_dashboard")
def show_user_with_courts():
    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/")
    data = {
        "user_id" : session['user_id']
    }
    one_user = User.get_user_by_id_with_courts(data)

    return render_template("show_user.html", one_user = one_user)
