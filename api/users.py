from flask import Blueprint, request,jsonify
from models import db,UserDetail
from flask_jwt_extended import create_access_token

usersbp = Blueprint('users',__name__)


@usersbp.route('/signup',methods = ['POST'])
def signup():
   data =  request.get_json();
   print('signup-payload',data)
   username = data.get('username')
   email = data.get('email')
   password = data.get('password')
   role = data.get('role','user')
   print('username,email,password,role', username,email,role,password)
   if(not username or not email or not password):
      return jsonify({
         "message":"Missing credentials, pls check!"
      }), 401
   
   isUserExists = UserDetail.query.filter_by(email = email).first();
   if(isUserExists):
      return jsonify({
         "message":"Hey, the User was already registered.Pls login"
      }), 401
   
   newUser =  UserDetail(username = username, email = email,role = role)
   print('new user',newUser)
   newUser.setPassword(password);
   db.session.add(newUser)
   db.session.commit()

   return jsonify({
      "message":"User Created Succesfuly",
      "user": newUser.toDict()
   }), 201


@usersbp.route('/login',methods = ['POST'])
def login():
   data = request.json
   email = data['email']
   password = data['password']

   if(not email or not password):
      return jsonify({
         "message":" Missing Fields. Email Id and Password required"
      }), 401
   
   user = UserDetail.query.filter_by(email = email).first();
   checkpwdUser = user.checkPassword(password)
   if(not user or not checkpwdUser):
      return jsonify({
         "message":"Invalid Credentials - Emailid and Password"
      }), 401
   
   accesstoken = create_access_token(identity=user.email,additional_claims={"role": user.role})
   return jsonify({
      "message":"Login Successfully - User Authenticated",
      "token": accesstoken,
      "user":user.toDict()
   }),200