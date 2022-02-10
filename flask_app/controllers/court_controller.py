from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.court import Court

@app.route("/show_court/<int:court_id>")
def show_court(court_id):
    data = {
        "court_id" : court_id
    }

    one_court = Court.get_court_with_users(data)

    return render_template("show_court.html", one_court=one_court)

@app.route("/browse_courts")
def show_courts():
    if "user_id" not in session:
        all_courts = Court.get_all_courts()
        return render_template("show_all_courts.html", all_courts=all_courts)
    else:
        data = {
            "user_id" : session['user_id']
        }
        user = User.get_user_by_id(data)
        all_courts = Court.get_all_courts()
        return render_template("show_all_courts.html", all_courts=all_courts, user=user)

# @app.route("/map")
# def show_map():
#     return render_template("maps_code.html")