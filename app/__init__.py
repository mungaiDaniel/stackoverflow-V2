from flask import Flask
from app.users.routes import user_v2


app = Flask(__name__)
app.register_blueprint(user_v2)
app.debug = True





