from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash,generate_password_hash

db = SQLAlchemy()

class UserDetail(db.Model):
    __tablename__ = 'userdetail'
    id = db.Column(db.Integer, primary_key=True, nullable = False, autoincrement=True)
    username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(200), unique=True, nullable = False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(100), default = 'user')

    def setPassword(self,password):
        self.password_hash = generate_password_hash(password);

    def checkPassword(self,password):
        return check_password_hash(self.password_hash,password);


    def toDict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email":self.email,
            "role":self.role
        }


class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer,primary_key = True, nullable = False,unique = True, autoincrement=True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text)
    questions = db.relationship('Question',backref = 'quiz',lazy = False)

    def toDict(self):
        return {
            "quiz_id": self.id,
            "title": self.title,
            "description": self.description,
            "questions": [question.toDict() for question in self.questions]
        }


class Question(db.Model):
    __tablename__= 'questions'

    id = db.Column(db.Integer,primary_key = True, nullable = False, unique = True, autoincrement=True)
    quiz_id = db.Column(db.Integer,db.ForeignKey('quizzes.id'))
    text = db.Column(db.Text)
    options = db.relationship('Option', backref = 'question', lazy = False)

    def toDict(self):
        return {
            "question_id": self.id,
            "quiz_id": self.quiz_id,
            "question_text": self.text,
            "options": [option.toDict() for option in self.options]
        }

class Option(db.Model):
    __tablename__ = 'options'
    
    id = db.Column(db.Integer, primary_key = True,nullable = False, unique = True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    text = db.Column(db.String(200))
    is_correct = db.Column(db.Boolean, default = False)

    def toDict(self):
        return {
            "option_id": self.id,
            "question_id": self.question_id,
            "option_text": self.text,
            "is_correct": self.is_correct
        }


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempt'

    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    userdetail_id = db.Column(db.Integer, db.ForeignKey('userdetail.id'))
    quiz_id = db.Column(db.Integer,db.ForeignKey('quizzes.id'))
    score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    answers = db.relationship('AnswerRecord', backref = 'quizattempt', lazy = False)

    def toDict(self):
        return {
            "id": self.id,
            "userdetail_id": self.userdetail_id,
            "quiz_id": self.quiz_id,
            "score": self.score,
            "timestamp": self.timestamp,
            "answers": [answer.toDict() for answer in  self.answers]
        }


class AnswerRecord(db.Model):
    __tablename__ = 'answer_records'

    id = db.Column(db.Integer,primary_key = True, nullable = False, autoincrement=True)
    quiz_attempt_id = db.Column(db.Integer,db.ForeignKey('quiz_attempt.id')) 
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    selected_option = db.Column(db.Integer)
    is_correct = db.Column(db.Boolean)

    def toDict(self):
        return {
            "id": self.id,
            "quiz_attempt_id": self.quiz_attempt_id,
            "question_id": self.question_id,
            "selected_option": self.selected_option,
            "is_correct": self.is_correct
        }

