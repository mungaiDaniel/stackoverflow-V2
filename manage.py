from app import app
from app.users.model import User
from app.questions.model import Question
from app.answers.model import Answer
from app.database import MY_DATABASE

if __name__ == '__main__':
    app.run(debug=True)
    


