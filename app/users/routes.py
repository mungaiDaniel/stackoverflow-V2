from flask import Blueprint, make_response, jsonify, request
from app.users.model import User
from datetime import datetime

user_v2 = Blueprint('user-v2', __name__, url_prefix='/api/v2')

@user_v2.route('/user', methods=['POST'])
def post():
    data = request.get_json()
    
    username = data['username']
    email = data['email']
    password = data['password']
    
    new_user = User(id=None, username=username, email=email, password=User.generate_hash(password), date_created=datetime.now(), date_modified=datetime.now() )
    
    new_user.save(username, password, email, datetime.now(), datetime.now())
    
    return make_response(jsonify({
        "status": 201,
        "data": new_user.json_dumps()
    }), 201)