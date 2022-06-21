from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app, DATABASE
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)   
# we are creating an object called bcrypt, 
# which is made by invoking the function Bcrypt with our app as an argument
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    ## checking to see if user exists by email
    @classmethod
    def get_one (cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        ## if we get a result it means the email is in the database already
        result = connectToMySQL(DATABASE).query_db(query, data)
        ## checking to see if we get a result > 0 
        if len(result) > 0:
            #returns data as a list, with a dictionary inside - need to access with index
            return cls(result [0] )
        else:
            return False

    @classmethod
    def get_one_by_id (cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        ## if we get a result it means the email is in the database already
        result = connectToMySQL(DATABASE).query_db(query, data)
        ## checking to see if we get a result > 0 
        if len(result) > 0:
            #returns data as a list, with a dictionary inside - need to access with index
            return cls(result [0] )
        else:
            return False

    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


    @staticmethod
    def validate_login(data):
        isValid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) >= 1:
            flash("Email is not found.")
            isValid = False
        return isValid

    @staticmethod
    def validate_session():
        ## only need to validate one of the provided 
        if "user_id" in session:
            return True
        else:
            return False


    @staticmethod
    def validate_registration(data):
        isValid = True

        if not EMAIL_REGEX.match(data['email']):
            flash("Email is invalid.", "error_email")
            isValid = False

        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.", "error_password")
            isValid = False

        if data['password'] != data['confirm_password']:
            flash("Password does not match")
            isValid = False

        if len(data['first_name']) < 2:
            flash("Must be at least 2 characters.", "error_first_name")
            isValid = False

        if len(data['last_name']) < 2:
            flash("Must be at least 2 characters.", "error_last_name")
            isValid = False


        return isValid
