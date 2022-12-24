import datetime
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, create_access_token
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from app.database import MY_DATABASE

cursor = MY_DATABASE.connect_to_db()

MY_DATABASE.create_users_table()


class User(MY_DATABASE):
    '''Class to model a user'''

    def __init__(self,id, username, email, password, date_created, date_modified):
        '''method to initialize User class'''
        self.id = id    
        self.username = username
        self.email = email
        self.password = password
        self.date_created = date_created
        self.date_modified = date_modified


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
    
    @classmethod
    def get_all(cls):
        
        ''' method to get all users'''
        cursor.execute(
            f"SELECT * FROM public.users"
        )
        rows = cursor.fetchall()
        
        output = []
        
        for row in rows:
            new = User(id=row[0], username=row[1], email=row[2], password=row[3], date_created=row[4], date_modified=row[5])
            
            output.append(new.json_dumps())
            
        return output