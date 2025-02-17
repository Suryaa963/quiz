from flask import Blueprint,jsonify,request
from models import db, UserDetail,Quiz,Question,QuizAttempt,Option,AnswerRecord
from sqlalchemy.orm import load_only
from flask_jwt_extended import jwt_required,get_jwt

bp_leaderboard = Blueprint('leaderboard', __name__)

# fetching only quiz titles and id;

@bp_leaderboard.route('/',methods = ['GET'])
@jwt_required()

def fetchAllLeaders():
    print('hiii')
    quizz_titles =  Quiz.query.with_entities(Quiz.id, Quiz.title).all()
    print('quizzes',quizz_titles)
    return jsonify({
        "result": [{"id": quiz.id,"title": quiz.title} for quiz in quizz_titles]
    }),200

# fetching complete answer and options for a particular quiz id

@bp_leaderboard.route('/<int:quizid>',methods = ['GET'])
@jwt_required()
def fetchQuizQuestions(quizid):
    print('hello',quizid )
    quizz =  Quiz.query.get(quizid)
    quiz_questions = quizz.questions
    print('quizzes',quizz)
    return jsonify({
        "result": [question.toDict() for question in quiz_questions]
    }),200
 