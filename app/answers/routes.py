from flask import Blueprint, make_response, jsonify, request
import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.answers.model import Answer
from app.questions.model import Question

answer_V2 = Blueprint('answer_v2', __name__, url_prefix='/api/v2')

@answer_V2.route('/answers/<int:id>', methods=['GET'])
def get(id):
    all_answers = Answer.get_all_question_answers(question_id=id)
    
    return make_response(jsonify({
        "status": 200,
        "data": all_answers
    }), 200)
@answer_V2.route('/answer/<int:id>', methods=['POST'])  
@jwt_required()  
def post(id):
    ques = Question.get_by_id(id=id)
    if ques == None:
        return make_response(jsonify({
            "status": 404,
            "msg": "No question found"
        }), 404)
        
    data = request.get_json()
    body = data['body']
    
    if len(data['body']) < 6:
            return {'message': 'Ops!,the answer is too short,kindly provide an answer of more than 15 characters'}, 400

    used_id = get_jwt_identity()
    new_answer = Answer(id=id, body=body, question_id=id, user_id=used_id, date_created=datetime.datetime.now(), date_modified=datetime.datetime.now(), accept=False )
    
    new_answer.save(body, id, used_id,datetime.datetime.now(), datetime.datetime.now(), False)
    
    return make_response(jsonify({
        "status": 201,
        "msg": "the answer posted succesful",
        "data": new_answer.json_dumps()
    }), 201)
@answer_V2.route('/answer/<int:id>', methods=['GET'])
def get_by_id(id):
    answer = Answer.get_by_id(id=id)
    if answer:
        return make_response(jsonify({
            "status": 200,
            "data": answer
        }), 200)
    return make_response(jsonify({
        "status": 404,
        "data": "No answer found by that id"
    }), 404)

@answer_V2.route('/answer/<int:id>', methods=['PUT'])
def update(id):
    update_data = request.get_json()
    
    answer_to_edit = Answer.get_by_id(id=id)
    answer_to_edit = Answer.update(update_data=update_data['body'], id=id)

    return make_response(jsonify({
        "status": 200,
        "data": answer_to_edit
    }), 201)