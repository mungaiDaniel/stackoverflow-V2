import json
import unittest
import datetime

from app.app import app
from app.database import MY_DATABASE
from app.users.model import User
from config import TestingConfig
from app.helper_function import register_user, login_user, post_answer

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
        self.new_user = User(id=2, username="username",
                            email="username@gmail.com", password="User.generate_hash(password)",
                            date_created=datetime.datetime.now(), date_modified=datetime.datetime.now())

        self.client = self.app.test_client()
        self.app.testing = True

    def test_init(self):
        # test that a user is initialized
        self.new_user = User(id=1, username="username3",
                             email="danitomonga@gmail.com", password="password",
                             date_created=datetime.datetime.now(), date_modified=datetime.datetime.now())
        self.assertTrue(type(self.new_user.id), int)
        self.assertEqual(type(self.new_user), User)

    def test_register(self):
        # Test can register a user
        new_user = {'username': 'username3', 'email': 'danitomonga@gmail', 'password': 'password'}
        response = self.client.post('api/v2/signup',
                                    data=json.dumps(new_user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
    def test_register_username_twice(self):
        # Test can register a username twice
        new_user1 = {'username': 'username3', 'email': 'danitomonga@gmail.com', 'password': 'password'}
        response = self.client.post('api/v2/signup',
                                    data=json.dumps(new_user1), content_type='application/json')
        new_user = {'username': 'username3', 'email': 'danitomonga@gmail.com', 'password': 'password'}
        response = self.client.post('api/v2/signup',
                                    data=json.dumps(new_user), content_type='application/json')
        self.assertEqual(response.status_code, 409)
        
    def test_register_email_twice(self):
        # Test can register a user an email  twice
        new_user1 = {'username': 'username3', 'email': 'danitomonga@gmail.com', 'password': 'password'}
        response1 = self.client.post('api/v2/signup',
                                    data=json.dumps(new_user1), content_type='application/json')
        new_user = {'username': 'username3', 'email': 'danitomonga@gmail.com', 'password': 'password'}
        response = self.client.post('api/v2/signup',
                                    data=json.dumps(new_user), content_type='application/json')
        self.assertEqual(response.status_code, 409)
        
    def test_user_not_found(self):
        # test cant login a non user
        response = self.client.post('api/v2/login',
                                    data=json.dumps(
                                        {'username': 'agnes', 'email': 'wanjiruamungi@gmail.com','password': 'password'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)