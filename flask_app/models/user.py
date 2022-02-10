from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash

from flask_app.models import court

from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re
from datetime import date

today = date.today()
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.birthday = data['birthday']
        self.level = data['level']
        self.gender = data['gender']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.courts = []

    @staticmethod
    def validate_register(form_data):
        is_valid = True
        today = str(date.today())
        year = today.split("-")
        bday = str(form_data["birthday"])
        yearb = bday.split("-")

        if len(form_data['first_name']) < 2:
            flash("First name must be at least 2 characters long!")
            is_valid = False

        if len(form_data['last_name']) < 2:
            flash("Last name must be at least 2 characters long!")
            is_valid = False

        if not EMAIL_REGEX.match(form_data['email']):
            flash("Email must be a valid format!")
            is_valid=False

        if len(form_data['password']) < 6:
            flash("Password must be at least 6 characters long!")
            is_valid=False

        if form_data['password'] !=form_data['conf_pass']:
            flash("Password has to match Confirmation Password!")
            is_valid = False

        if form_data['birthday'] == "":
            flash("Please enter valid birthday!")
            is_valid = False

        elif int(year[0]) - int(yearb[0]) < 16:
            flash("User must be at least 16 years old!")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(form_data):
        is_valid = True

        user_from_db = User.get_by_email(form_data)
        if not user_from_db:
            flash("Invalid credentials!")
            is_valid = False

        elif not bcrypt.check_password_hash(user_from_db.password, form_data['password']):
            flash("Invalid credentials!")
            is_valid = False

        return is_valid


    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, level, gender, birthday, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(level)s, %(gender)s, %(birthday)s, NOW(), NOW())"
        results = connectToMySQL('tennis_app').query_db(query, data)
        return results

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("tennis_app").query_db(query, data)

        if len(results) < 1:
            return False
        return cls( results[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        results = connectToMySQL("tennis_app").query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_user_by_id_with_courts(cls, data):
        query = "SELECT * FROM users LEFT JOIN fav_courts on (users.id=fav_courts.user_id) LEFT JOIN courts on (courts.id=fav_courts.court_id) WHERE users.id = %(user_id)s;"
        results = connectToMySQL("tennis_app").query_db(query, data)

        one_user = cls( results[0] )
        for row in results:
            court_data = {
                "id" : row['courts.id'],
                "title" : row['title'],
                "address1" : row['address1'],
                "address2" : row['address2'],
                "lat" : row['lat'],
                "lng" : row['lng'],
                "ct_number" : row['ct_number'],
                "descript" : row['descript'],
                "created_at" : row['courts.created_at'],
                "updated_at" : row['courts.updated_at']
            }
            one_user.courts.append( court.Court( court_data ))
        return one_user

    @classmethod
    def fav_court(cls, data):
        query = "INSERT INTO fav_courts (user_id, court_id) VALUES (%(user_id)s, %(court_id)s)"
        results = connectToMySQL("tennis_app").query_db(query, data)
        return results