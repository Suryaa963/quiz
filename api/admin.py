from flask import Blueprint,jsonify,request
from models import db, Quiz,Question,QuizAttempt,Option,AnswerRecord
from sqlalchemy.orm import load_only
from flask_jwt_extended import jwt_required,get_jwt

bp_admin_quizzes = Blueprint('adminquiz', __name__)

@bp_admin_quizzes.route('/',methods = ['POST'])
@jwt_required()

def addQuestions():
    try:
        print('request');
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        questions = data.get('questions');
        checkRole = get_jwt()
        print('checkrole',checkRole,checkRole['role'])
        if(checkRole['role'] != 'admin'):
            return jsonify({
                "message":"User not permitted to create a Quiz. only Admins are allowed"
            }),401
        
        if(not title or  len(questions)==0):
            return jsonify({
                "message":"Missing fields!"
            }),401
        questionslist = []
    # add in options;
        for question in questions:
            
            print('question',question,question['question_text'])
            question_text = question.get('question_text')
            options = question.get('options')

            optionsList = []
            for option in options:
                option_text = option.get('option_text')
                is_correct_str = option.get('is_correct')
                is_correct = str(is_correct_str).lower() == 'true'
                optionIns = Option(text = option_text,is_correct = is_correct);
                optionsList.append(optionIns)
            
            questionIns = Question(text = question_text,options = optionsList)
            questionslist.append(questionIns)

        quizIns = Quiz(title = title, description = description, questions = questionslist)
        db.session.add(quizIns);
        db.session.commit()

        return jsonify({
            "result": quizIns.toDict()
        }),201
    
    except Exception as e:
        return jsonify({
            "error":"Unexpected error occurred!"
        }), 501