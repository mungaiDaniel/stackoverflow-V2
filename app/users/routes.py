from flask import Blueprint, make_response, jsonify, request

user_v2 = Blueprint('user-v2', __name__, url_prefix='/api/v2')

@user_v2.route('/user', methods=['GET'])
def get():
    user = {
        'username': 'daniel',
        'email': 'danitomonga@gmail.com'
    }
    
    return {'data': user}
    