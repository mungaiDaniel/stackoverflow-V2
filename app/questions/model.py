from datetime import datetime
import datetime
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, create_access_token
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from app.users.model import User
from app.answers.model import Answer
from app.database import MY_DATABASE
        
cursor = MY_DATABASE.connect_to_db()
MY_DATABASE.create_users_table()
MY_DATABASE.create_questions_table()
        
class Question(MY_DATABASE):
    '''Class to model a question'''

    def __init__(self,id, title, body, user_id, date_created, date_modified):
        '''method to initialize post class'''
        self.id = id
        self.title = title
        self.body = body
        self.user_id = user_id
        self.date_created = date_created
        self.date_modified = date_modified

    def save(self, title, body, user_id, date_created, date_modified):
        '''method to save a post'''
        format_str = f"""
         INSERT INTO public.questions (title,body,user_id,date_created,date_modified)
         VALUES ('{title}','{body}',{user_id},'{str(datetime.datetime.now().date())}','{str(datetime.datetime.now().date())}') ;
         """
        cursor.execute(format_str)
        return {
            "title": title,
            "body": body,
            "user_id": user_id,
            "date_created": str(date_created),
            "date_modified": str(date_modified),
        }

    def json_dumps(self):
        '''method to return a json object from the question details'''
        obj = {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "user": User.find_by_id(self.user_id),
            "date_created": str(self.date_created),
            "date_modified": str(self.date_modified),
            "answers": Answer.get_all_question_answers(self.id)
        }
        return obj

    @classmethod
    def get_by_id(cls, id):
        '''method to get a question by id'''
        cursor.execute('SELECT * FROM "public"."questions" WHERE id=%s', (id,))
        row = cursor.fetchone()
        if row == None:
            return None
        question = Question(id=row[0], title=row[1], body=row[2], user_id=row[3], date_created=row[4],
                            date_modified=row[5])

        retrieved_question = question.json_dumps()
        answers = Answer.get_all_question_answers(question_id=id)
        retrieved_question['answers'] = answers
        return retrieved_question

    @classmethod
    def get_all(cls):
        '''method to get all questions'''
        cursor.execute(
            f"SELECT * FROM public.questions")
        rows = cursor.fetchall()
        list_dict = []

        for item in rows:
            new = Question(id=item[0], title=item[1], body=item[2], user_id=item[3], date_created=item[4],
                           date_modified=item[5])
            list_dict.append(new.json_dumps())
        return list_dict

    @classmethod
    def get_all_user_questions(cls, user):
        '''method to get all questions of a given user'''
        question_owner = User.find_by_id(user)
        if question_owner:
            cursor.execute("SELECT * FROM public.questions WHERE user_id = %s", (user,))
            rows = cursor.fetchall()
            list_dict = []

            for item in rows:
                new = Question(id=item[0], title=item[1], body=item[2], user_id=item[3], date_created=item[4],
                               date_modified=item[5])
                list_dict.append(new.json_dumps())
            return list_dict
        return {"message": "No user with that id"}, 404

    @classmethod
    def delete_question(cls, id):
        '''method to delete a question'''
        try:
            cursor.execute('DELETE FROM public.questions CASCADE WHERE id = %s', (id,))
            return "successfully deleted"
        except Exception:
            return "failed"

    @classmethod
    def search_questions(cls, body, title):
        cursor.execute(f"SELECT * FROM questions WHERE body LIKE '%{body}%' OR title LIKE '%{title}%'")
        rows = cursor.fetchall()
        list_dict = []
        for item in rows:
            new = Question(id=item[0], title=item[1], body=item[2], user_id=item[3], date_created=item[4],
                           date_modified=item[5])
            list_dict.append(new.json_dumps())
        return list_dict

    @classmethod
    def get_top_answered(cls):
        all_questions = Question.get_all()
        for question in all_questions:
            list_length = []
            questions = []
            answers = Answer.get_all_question_answers(question_id=question['id'])
            for ans in answers:
                list_length.append(len(ans))
                questions.append(question)

                list_length.sort()
                top_6_answered = questions[-6:]
            return top_6_answered