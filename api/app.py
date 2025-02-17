from flask import Flask, request,jsonify
from models import db;
from quiz import bp_quizzes
from flask_cors import CORS
from admin import bp_admin_quizzes
from users import usersbp
from flask_jwt_extended import JWTManager

app = Flask(__name__)
cors = CORS(app, origins = '*', supports_credentials=True)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/quiz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'suryaprakash'

app.register_blueprint(usersbp,url_prefix = '/users')
app.register_blueprint(bp_quizzes,url_prefix = '/user/quiz')
app.register_blueprint(bp_admin_quizzes,url_prefix = '/admin/quiz')

db.init_app(app)
jwt = JWTManager(app)

if __name__ =='__main__':
    with app.app_context():
        db.create_all()

    app.run(debug  = True)