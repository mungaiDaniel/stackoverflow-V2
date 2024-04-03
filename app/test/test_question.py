import json
import unittest
import datetime

from app.app import app

from app.database import MY_DATABASE
from config import TestingConfig
from app.helper_function import post_quiz, register_user, login_user, post_answer
from app.questions.model import Question
  
class TestQuestion(unittest.TestCase):
    '''class to test a question'''

    def tearDown(self):
        MY_DATABASE.drop_users_table()
        MY_DATABASE.drop_questions_table()
        MY_DATABASE.drop_answers_table()
        MY_DATABASE.create_users_table()
        MY_DATABASE.create_questions_table()
        MY_DATABASE.create_answers_table()

    def setUp(self):
        # setting up configurations for testing
        self.app = app
        self.app.config.from_object(TestingConfig)
        self.new_question = Question(id=4, title="how to init python",
                                     body="how to init python how to init python how to init python", user_id=1,
                                     date_created=datetime.datetime.now(), date_modified=datetime.datetime.now())
        self.client = self.app.test_client()
        self.app.testing = True
        register_user(self)
        response = login_user(self)
        self.token = json.loads(response.data.decode())['access_token']
        
    def test_init(self):
        # test that a question is initialized
        self.new_question = Question(id=4, title="how to init python",
                                     body="how to init python how to init python how to init python", user_id=1,
                                     date_created=datetime.datetime.now(), date_modified=datetime.datetime.now())
        self.assertTrue(type(self.new_question.id), int)
        self.assertEqual(type(self.new_question), Question)
        
    def test_question_posted(self):
        # method to test a question can be posted
        response = post_quiz(self)
        self.assertEqual(response.status_code, 201)
        
    def test__post_invalid_title(self):
        # test cant post a  invalid title
        response = login_user(self)
        result = json.loads(response.data)
        self.assertIn("access_token", result)
        new_question = {'tite': 'sh',
                        'body': 'error sit voluptatem accusantium doloremque laudantiumerror sit volupta', 'user_id': 1}
        response = self.client.post('api/v2/question', data=json.dumps(new_question),
                                    headers={'Authorization': f'Bearer {result["access_token"]}',
                                             'Content-Type': 'application' '/json'})
        self.assertEqual(response.status_code, 400)
        
    def test__post_invalid_body(self):
        # test cant post a  invalid title
        response = login_user(self)
        result = json.loads(response.data)
        self.assertIn("access_token", result)
        new_question = {'title': 'sh',
                        'bod': 'error sit voluptatem accusantium doloremque laudantiumerror sit volupta', 'user_id': 1}
        response = self.client.post('api/v2/question', data=json.dumps(new_question),
                                    headers={'Authorization': f'Bearer {result["access_token"]}',
                                             'Content-Type': 'application' '/json'})
        self.assertEqual(response.status_code, 400)
        
    def test_get_a_single_question(self):
        # test can get a single question
        post_quiz(self)
        response = self.client.get(f'api/v2/question/1', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        
    def test_get_non_existing_question(self):
        # test can get a none existing question
        response = self.client.get(f'api/v2/question/145678', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        
    def test_get_all_questions(self):
        # test can get all questions
        response = self.client.get('/api/v2/question', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(response), list)