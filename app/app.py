from flask import Flask, jsonify
from app.users.routes import user_v2
from app.questions.routes import question_v2
from app.answers.routes import answer_V2
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig
from app.database import MY_DATABASE

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(DevelopmentConfig)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

jwt = JWTManager(app)
app.register_blueprint(user_v2)
app.register_blueprint(question_v2)
app.register_blueprint(answer_V2)

MY_DATABASE.connect_to_db()
MY_DATABASE.create_users_table()
MY_DATABASE.create_questions_table()
MY_DATABASE.create_answers_table()

    

from app.users import routes, model
from app.questions import routes, model
from app.answers import routes, model
from app import database

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)