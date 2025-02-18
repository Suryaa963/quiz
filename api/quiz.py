from flask import Blueprint,jsonify,request
from models import db, Quiz,Question,QuizAttempt,Option,AnswerRecord
from sqlalchemy.orm import load_only
from flask_jwt_extended import jwt_required,get_jwt

bp_quizzes = Blueprint('quiz', __name__)

# fetching only quiz titles and id;

@bp_quizzes.route('/',methods = ['GET'])
@jwt_required()

def fetchAllQuiz():
    try:
        print('hiii')
        quizz_titles =  Quiz.query.with_entities(Quiz.id, Quiz.title).all()
        print('quizzes',quizz_titles)
        return jsonify({
            "result": [{"id": quiz.id,"title": quiz.title} for quiz in quizz_titles]
        }),200
    except Exception as e:
        return jsonify({
            "error":"An unexpected Error occurred"
        }),501
   

# fetching complete answer and options for a particular quiz id

@bp_quizzes.route('/<int:quizid>',methods = ['GET'])
@jwt_required()

def fetchQuizQuestions(quizid):
    try:
        print('hello',quizid )
        quizz =  Quiz.query.get(quizid)
        quiz_questions = quizz.questions
        print('quizzes',quizz)
        return jsonify({
            "result": [question.toDict() for question in quiz_questions]
        }),200
    except Exception as e:
         return jsonify({
            "error":"An unexpected Error occurred"
        }),501
   
    
    
   

# post requst:

# {
#   "userdetail_id": "user123",
#   "quiz_id": 101,
#   "response": [
#     {  "question_id": 1, "selected_option_id": 102 },
#     { "question_id": 2, "selected_option_id": 107 },
#     { "question_id": 3, "selected_option_id": 113}
    
#   ]
# }

@bp_quizzes.route('/',methods = ['POST'])
@jwt_required()

def submitQuiz():
   try:
       
        data = request.get_json()
        payload = {}
        totalscore = 0;
        answers = []
        print('payl', data)
        # extracting datas
        userdetail_id = data.get('userdetail_id')
        quiz_id = data.get('quiz_id')
        response = data.get('response')
        
       
        for resp in response:
            print('resp',resp)
            iscorrect = False
            question_id = resp.get('question_id')
            selected_option_id = resp.get('selected_option_id')

            # retrieve question;
            #    question = Question.query.filter_by(id=question_id, quiz_id=quiz_id).first()
            #    if not question:
            #        return jsonify({
            #            "message": "Question not exist"
            #        }),401
       
            correct_option = Option.query.filter_by(question_id = question_id,is_correct = True).first()
            print('questionid',question_id,selected_option_id)
            print('coreect option',correct_option)
            if correct_option and (correct_option.id == selected_option_id):
                totalscore+=1;
                iscorrect = True
        
            answerRecord = AnswerRecord(
                question_id = question_id,
                selected_option = selected_option_id,
                is_correct = iscorrect
            )
            answers.append(answerRecord)
           
        quizAttempt = QuizAttempt(
            userdetail_id = userdetail_id,
            quiz_id = quiz_id,
            score = totalscore,
            answers = answers
        )
        db.session.add(quizAttempt)
        db.session.commit()
        return jsonify({
            "result": {"id":quizAttempt.id,
                        "score":quizAttempt.score,
                        "time":quizAttempt.timestamp}
        }), 201           


   except Exception as e:
        return jsonify({
            "error":"Unexpected error occurred!"
        }),501
   
@bp_quizzes.route('/<int:quizid>/<int:userid>/status',methods = ['GET'])
def userquizstatus(quizid,userid):
   # payload = request.get_json();
   # userid = payload.get('userid')
   # quizid = payload.get('quizid');

    UserQuizStatus = QuizAttempt.query.filter_by(userdetail_id = userid, quiz_id = quizid).first();
    if(UserQuizStatus):
        return jsonify({
            "status": True,
            "score": UserQuizStatus.score
        }),200
    return jsonify({
            "status": False
        }),200
    