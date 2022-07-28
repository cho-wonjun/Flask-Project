from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class User:
    db = "login_and_registration_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        user = connectToMySQL(cls.db).query_db(query, data)
        return user

    @classmethod
    def find_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def find_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return cls(results[0])

    @classmethod
    def find_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_registration(user):
        is_valid = True
        results = User.find_by_email(user)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 2 characters", "register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 2 characters", "register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match", "register")
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        results = User.find_by_email(user)
        if not results:
            flash("Email is not found", "login")
            is_valid = False
        if len(user['password']) < 8:
                flash("Password must be at least 8 characters", "login")
                is_valid = False
        return is_valid 