# from flask_cors import cross_origin
from flask import Blueprint, make_response, jsonify, request
from app.database import MY_DATABASE
from app.users.model import User
from datetime import datetime
# from flask_cors import CORS, cross_origin
from app.validator import Validate
from flask_jwt_extended import create_access_token, jwt_required, \
    get_jwt_identity

user_v2 = Blueprint('user-v2', __name__, url_prefix='/api/v2')

@user_v2.route('/signup', methods=['POST'])
# @cross_origin(origin='localhost', headers=['Content-type', 'Authorization'], supports_credentials=True)
def post():
    data = request.get_json()
    
    
    username = data['username']
    if User.find_by_username(data['username']):
            return {'message': 'This username is already taken,kindly try another username'}, 409
        
    if User.find_by_email(data['email']):
            return {'message': 'This email is already taken'}, 409
    email = data['email']
    password = data['password']
    password=User.generate_hash(data['password'])
    new_user = User(id=None, username=username, email=email, password=password, date_created=datetime.now(), date_modified=datetime.now() )
    
    format_str = f"""
                 INSERT INTO public.users (username,email,password,date_created,date_modified)
                 VALUES ('{username}','{email}','{password}','{str(datetime.now())}','{str(datetime.now())}');
                 
                 """
    
    new_user.save(format_str)
    
    return make_response(jsonify({
        "status": 201,
        "data": new_user.json_dumps()
    }), 201)
    
@user_v2.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    
    current_user = User.find_by_username(data['username'])
    if current_user == False:
            return {'message': 'User {} doesnt exist'.format(
                data['username'])}, 404
            
    password = data['password']
    
    hash = current_user[3]
    
    if not User.verify_hash(password,hash):
        return {
            "messgae":"Incorect username or password"
        }, 401
    
            
    
    if User.find_by_username(data['username']):
            access_token = create_access_token(current_user[0])
            return dict(message='Logged in as {}'.format(current_user[1]),
                        access_token=access_token), 200
            
    return {
        'message': 'wrong credentials'
    }, 403
    
@user_v2.route('/user', methods=['GET'])
def get_all():
    users = User.get_all()
    
    return make_response(jsonify({
        "status": 200,
        "data": users
    }), 200)

@user_v2.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):
      user = User.find_by_id(id)

      return make_response(jsonify({
        "status": 200,
        "data": user
    }), 200)
