from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app.models import user


class Court:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.address1 = data['address1']
        self.address2 = data['address2']
        self.lat = data['lat']
        self.lng = data['lng']
        self.ct_number = data['ct_number']
        self.descript = data['descript']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.users = []

    @classmethod
    def get_all_courts(cls):
        query = "SELECT * FROM courts;"
        results = connectToMySQL("tennis_app").query_db(query)
        all_courts = []
        for row in results:
            one_court = cls(row)
            all_courts.append(one_court) 
        return all_courts


    @classmethod
    def get_court_with_users(cls, data):
        query = "SELECT * FROM courts LEFT JOIN fav_courts on (courts.id=fav_courts.court_id) LEFT JOIN users on (users.id=fav_courts.user_id) WHERE courts.id=%(court_id)s;"
        results = connectToMySQL("tennis_app").query_db(query, data)

        one_court = cls( results[0] )
        for row in results:
            user_data = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "birthday" : row['birthday'],
                "level" : row['level'],
                "gender" : row['gender'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
            }
            one_court.users.append( user.User( user_data ))
        return one_court

