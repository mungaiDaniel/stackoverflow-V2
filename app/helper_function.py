import json

def register_user(self):
    '''register user'''
    return self.client.post(
        'api/v2/signup',
        data=json.dumps(dict(
            username='username254',
            email='username254@gmail.com',
            password='password'
        )),
        content_type='application/json'
    )

def register_user2(self):
    '''register user'''
    return self.client.post(
        'api/v2/signup',
        data=json.dumps(dict(
            username='username2542',
            email='username2542@gmail.com',
            password='password'
        )),
        content_type='application/json'
    )
    
def login_user(self):
    '''login the registered user'''
    return self.client.post(
        'api/v2/login',
        data=json.dumps(dict(
            username='username254',
            password='password'
        )),
        content_type='application/json'
    )
    
def post_quiz(self):
    '''loginthe registered user'''
    response = login_user(self)
    result = json.loads(response.data)
    self.assertIn("access_token", result)
    new_question = {'title': 'error sit voluptatem accusantium doloremque laudantium',
                    'body': 'error sit voluptatem accusantium doloremque laudantiumerror sit volupta', 'user_id': 1}
    response = self.client.post('api/v2/question', data=json.dumps(new_question),
                                headers={'Authorization': f'Bearer {result["access_token"]}',
                                         'Content-Type': 'application' '/json'})
    return response

def post_answer(self):
    '''login the registered user'''
    response = login_user(self)
    result = json.loads(response.data)
    self.assertIn("access_token", result)
    new_answer = {'body': 'error sit voluptatem accusantium doloremque laudantiumerror sit volupta'}
    response = self.client.post('/api/v2/answer/4', data=json.dumps(new_answer),
                                headers={'Authorization': f'Bearer {result["access_token"]}',
                                         'Content-Type': 'application' '/json'})
    return response