from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required

from flask import current_app as app
from flask_bcrypt import Bcrypt

from .models import User
from .database import db

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class UserRegisteration(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')       
 
        if not (username and email and password and role):
            return {'message': "Missing username or password"}, 400
        if User.query.filter_by(username=username).first():
            return {'message': "Username already taken"}, 400

        new_user = User(username=username, email=data['email'], password=bcrypt.generate_password_hash(password).decode('utf-8'), role=role)
        db.session.add(new_user)
        db.session.commit()
        return {'message': "User created successfully"}, 200

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        #print('password check: ',bcrypt.check_password_hash(user.password,password))
        if user:
            if (bcrypt.check_password_hash(user.password,password)):
                print(user, password)
                access_token = create_access_token(identity=str(user.id))
                return {'access_token': access_token} , 200
        return {'message': "invalid credentials"}, 401        

class Secure(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return {'message': f"Hello user {current_user_id}, you just accessed the protected resource, test successful bro."}, 200


