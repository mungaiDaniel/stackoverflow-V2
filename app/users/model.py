from datetime import datetime
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, create_access_token
from passlib.handlers.pbkdf2 import pbkdf2_sha256

import os
import psycopg2

class Users:
    
    @classmethod
    def connect_to_db(cls):
        
        connect = psycopg2.connect(os.environ['DATABASE_URL'])
        connect.autocommit = True
        cursor = connect.cursor()
        
        return cursor
    
    
    @classmethod
    def create_users_table(cls):

        cursor = Users.connect_to_db()
        sql_command = """CREATE TABLE IF NOT EXISTS "public"."users"  (
        id SERIAL ,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        date_created VARCHAR(80),
        date_modified VARCHAR(80),
        PRIMARY KEY (id)
            )"""
        cursor.execute(sql_command)
        

cursor = Users.connect_to_db()
Users.create_users_table()


class User:
    '''Class to model a user'''

    def __init__(self, id, username, email, password, date_created, date_modified):
        '''method to initialize User class'''
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.date_created = date_created
        self.date_modified = date_modified

    def save(self, username, email, password, date_created, date_modified):
        '''method to save a user'''
        format_str = f"""
                 INSERT INTO public.users (username,email,password,date_created,date_modified)
                 VALUES ('{username}','{email}','{password}','{str(datetime.now())}','{str(datetime.now())}');
                 """
        cursor.execute(format_str)
        return {
            "username": username,
            "email": email,
            "date_created": str(date_created),
            "date_modified": str(date_modified)
        }

    @classmethod
    def find_by_email(cls, email):
        '''This method gets a user using email'''
        try:
            cursor.execute("select * from users where email = %s", (email,))
            user = cursor.fetchone()
            return list(user)
        except Exception:
            return False

    @classmethod
    def find_by_username(cls, username):
        '''method to find a user by username'''
        try:
            cursor.execute("select * from users where username = %s", (username,))
            user = cursor.fetchone()
            return list(user)
        except Exception:
            return False

    @classmethod
    def find_by_id(cls, id):
        '''method to find a user by id'''
        try:
            cursor.execute("select * from users where id = %s", (id,))
            retrieved_user = list(cursor.fetchone())
            user = User(id=retrieved_user[0], username=retrieved_user[1], email=retrieved_user[2],
                        password=retrieved_user[3], date_created=retrieved_user[4], date_modified=retrieved_user[5])

            return user.json_dumps()
        except Exception:
            return False

    @staticmethod
    def generate_hash(password):
        '''method that returns a hash'''
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        '''method to verify password with the hash'''
        return pbkdf2_sha256.verify(password, hash)

    @staticmethod
    def create_token():
        '''method to generate token from username'''
        username = get_jwt_identity()
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5)
        token = create_access_token(username, expires_delta=expires)
        return jsonify({'token': token}), 201

    def json_dumps(self):
        '''method to return a json object from a user'''
        ans = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "datecreated": self.date_created,
            "datemodified": self.date_modified
        }
        return ans