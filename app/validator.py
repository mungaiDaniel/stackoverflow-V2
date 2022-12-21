import re
from app.database import MY_DATABASE
from app.answers.model import Answer

cursor = MY_DATABASE.connect_to_db()

class Validate:

    @staticmethod
    def validate_length_username(username):
        if len(username) < 4:
            return False
        return True

    @staticmethod
    def validate_password_length(password):
        if len(password) < 6:
            return False
        return True

    @staticmethod
    def is_question_exist(body):
        '''check if question exists'''
        query = ("""SELECT * FROM questions where body = '{}'""".format(body))
        cursor.execute(query)
        body = cursor.fetchone()
        if body:
            return True
        return False