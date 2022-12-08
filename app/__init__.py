from flask import Flask, jsonify
from app.users.routes import user_v2
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig

app = Flask(__name__)
CORS(app)
app.config.from_object(DevelopmentConfig)
app.config['JWT_SECRET_KEY'] = 'BLAH'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)
app.register_blueprint(user_v2)
app.debug = True


from app.users import routes, model


