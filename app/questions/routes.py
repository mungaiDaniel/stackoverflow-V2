from flask import Blueprint, make_response, jsonify, request
from app.questions.model import Question
import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

question_v2 = Blueprint('question_v2', __name__, url_prefix='/api/v2')

@question_v2.route('/question', methods=['POST'])
@jwt_required()
def post():
    data = request.get_json()
    user_id = get_jwt_identity()
    if not request.json or not 'title' in request.json or not 'body' in request.json:
        return make_response(jsonify({
            "status": 400,
            "error": "details name is required"
        }), 400)

    title = data['title']
    body = data['body']
    new_question = Question(id=None,title=title, body=body, user_id=user_id, date_created=datetime.datetime.now(), date_modified=datetime.datetime.now())
    new_question.save(title=title, body=body, user_id=user_id,date_created=datetime.datetime.now(),date_modified=datetime.datetime.now() )
    
    return make_response(jsonify({
        "status": 201,
        "data": new_question.json_dumps(),
        "msg": "question posted succesfully"
    }), 201)
    
@question_v2.route('/question', methods=['GET'])
def get_all():
    
    question = Question.get_all()
    
    return make_response(jsonify({
        "status": 200,
        "data": question
    }), 200)
    
    
@question_v2.route('/question/<int:id>', methods=['GET'])
def get_one(id):
    
    question = Question.get_by_id(id=id)
    
    if question:
        return make_response(jsonify({
            "status": 200,
            "data": question
        }), 200)
    return make_response(jsonify({
        "status": 404,
        "data": "No question was found by that id"
    }), 404)
    
@question_v2.route('/question/<int:id>', methods=['DELETE'])
def delete(id):
    question_to_delete = Question.get_by_id(id=id)
    
    if question_to_delete:
        
        Question.delete_question(id=id)
        
        return make_response(jsonify({
            "status": 204,
            "message": "deleted successful"
        }), 204)
        
    return make_response(jsonify({
        "status": 404,
        "error": "No question found with that id"
     }), 404)
    
@question_v2.route('/questions', methods=['GET'])
def search():
    data = request.get_json()
    
    if "search" in data:
        question = Question.search_questions(body=data['search'], title=data['search'])
        
        if question:
            return {"message": "search result", "data": question}, 200
    return {
        "message": "No question found"
    }
    
        