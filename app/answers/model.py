import os  

import psycopg2
import datetime
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, create_access_token
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from app.users.model import User
from app.database import MY_DATABASE


        
cursor = MY_DATABASE.connect_to_db()
MY_DATABASE.create_questions_table()
MY_DATABASE.create_answers_table()
        
class Answer(MY_DATABASE):
    '''Class to model an answer'''

    def __init__(self, id, body, question_id, user_id, date_created, date_modified, accept):
        '''method to initialize Answer class'''
        self.id = id
        self.body = body
        self.question_id = question_id
        self.user_id = user_id
        self.date_created = date_created
        self.date_modified = date_modified
        self.accept = accept

    def save(self, body, question_id, user_id, date_created, date_modified, accept):
        '''method to save an answer'''
        format_str = f"""INSERT INTO public.answers (body, question_id, user_id, date_created, date_modified)
                 VALUES ('{body}', {question_id}, {user_id},' {str(datetime.datetime.now())}', '{str(datetime.datetime.now())}');
                 """
        cursor.execute(format_str)
        return {
            "body": body,
            "question_id": question_id,
            "user_id": user_id,
            "accept": accept,
            "date_created": str(date_created),
            "date_modified": str(date_modified),
        }
        
    def json_dumps(self):
        '''method to return a json object from the answer details'''
        
        obj = {
            "id": self.id,
            "body": self.body,
            "user_id": self.user_id,
            "question_id": self.question_id,
            "datecreated": self.date_created,
            "datemodified": self.date_modified
            
        }
        return obj

    @classmethod
    def get_all_question_answers(cls, question_id):
        '''method to get all answers of a given question'''
        cursor.execute(
            f"SELECT * FROM public.answers")
        rows = cursor.fetchall()
        answers_retrieved_dict = []
        for answer in rows:
            if answer[2] == (question_id):
                answer_question = Answer(id=answer[0], body=answer[1], question_id=answer[2], user_id=answer[3],
                                         date_created=answer[4],
                                         date_modified=answer[5], accept=answer[6])
                answers_retrieved_dict.append(answer_question.json_dumps())
        return answers_retrieved_dict

    @classmethod
    def get_by_id(cls, id):
        '''method to get an answer by id'''
        cursor.execute('SELECT * FROM "public"."answers" WHERE id=%s', (id,))
        row = cursor.fetchone()
        if row == None:
            return None
        answer = {
            "id": row[0],
            "body": row[1],
            "question_id": row[2],
            "user_id": row[3],
            "date_created": row[4],
            "date_modified": row[5]
        }
        retrieved_answer = answer
        return retrieved_answer

    @classmethod
    def update(cls, body, user_id, accept, id):
        """Method to update an answer"""
        format_str = f"""
         UPDATE public.answers SET body = '{body}', date_modified = '{str(datetime.now())}' WHERE id = {id};
         """

        cursor.execute(format_str)

        return {
            "id": id,
            "body": body,
            "user_id": user_id,
            "accept": accept,
            "date_modified": str(datetime.now())
        }

    @classmethod
    def accept(cls, id):
        '''method to accept an answer'''
        format_str = f"""UPDATE public.answers SET accept=true WHERE id = id;"""
        cursor.execute(format_str)

    