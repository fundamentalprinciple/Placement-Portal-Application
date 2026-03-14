from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import utils, auth_token_required

from ..database import db
from ..user_datastore import user_datastore
from ..models import *

class LoginUser(Resource):
    def post(self):

        login_cred = request.get_json()

        if not login_cred or not login_cred.get('username') or not login_cred.get('password'):
            result = {
                'message': 'Username and password are required.'
            }

            return make_response(
                jsonify(result),
                400
            )
        
        username = login_cred['username']
        password = login_cred['password']

        # Data validation
        user = user_datastore.find_user(username=username)
        if not user:
            return make_response(
                jsonify({'message': 'User not found.'}),
                404
            )

        if not user.active:
            return make_response(
                jsonify({'message': 'Account inactive, await Admin approval.'}),
                403
            )
                
        
        if not utils.verify_password(password, user.password):
            return make_response(
                jsonify({'message': 'Invalid password.'}),
                401
            )
        
        auth_token = user.get_auth_token()

        utils.login_user(user)

        result = {
            'message': 'Login successful.',
            'auth_token': auth_token,
            'user': {
                'username': user.username,
                'email': user.email,
                'roles': [role.name for role in user.roles]
            }
        }

        return make_response(
            jsonify(result),
            200
        )


class RegisterUser(Resource):
    def post(self):
         
        user_cred = request.get_json()
        print(user_cred)
    
        # Data validation
        if not user_cred or not user_cred.get('username') or not user_cred.get('email') or not user_cred.get('password') or not user_cred.get('role'):
            result = {
                'message': 'Username, email, password and role are required.'
            }

            return make_response(
                jsonify(result),
                400
            )
        
        user = user_datastore.find_user(username = user_cred['username'])
        if user:
            result = {
                'message': 'Username already exists.'
            }

            return make_response(
                jsonify(result),
                400
            )

        user = user_datastore.find_user(email = user_cred['email'])
        if user:
            result = {
                'message': 'Email already exists.'
            }

            return make_response(
                jsonify(result),
                400
            )
        
        username = user_cred['username']
        email = user_cred['email']
        password = user_cred['password']
        role = user_cred['role']

        if len(password) < 6:
            result = {
                'message': 'Password must be at least 6 characters long.'
            }

            return make_response(
                jsonify(result),
                400
            )
        
      
        user_role = user_datastore.find_role(role)
        
        if user_role == 'admin' or not(user_role):
            result = {
                'message': 'Invalid role for register.'
            }
            
            return make_response(
                jsonify(result),
                400
            )
        
        if user_role == 'student':
            if not (user_cred['name'] or user_cred['gender'] or user_cred['degree'] or user_cred['cgpa'] or user_cred['year']):
                result = {
                    'message': "Fields name, gender, degree, cgpa and year are required."
                }
                return make_response(
                    jsonify(result),
                    400
                )
            user_datastore.create_user(
                username=username,
                email=email,
                password=password,
                roles = [user_role]
            )

            db.session.commit()
            student = user_datastore.find_user(username=username)
            new_student = Student(user_id=student.id, name=user_cred['name'], gender=user_cred['gender'], degree=user_cred['degree'],cgpa=user_cred['cgpa'],year=user_cred['year'])
            db.session.add(new_student)
            db.session.commit()

            result = {
                'message': 'User registered successfully.',
                'user': {
                    'username': username,
                    'email': email
                }
            }
            return make_response(
                jsonify(result),
                201
            )
        elif user_role == 'company':
            if not(user_cred['name'] or user_cred.get('hr_contact') or user_cred.get('website')):
                result = {
                    'message': 'name, hr_contact and website are required for applying a company registertion.'
                }

                return make_response(
                    jsonify(result),
                    400
                ) 

            user_datastore.create_user(
                username=username,
                email=email,
                password=password,
                roles = [user_role]
            )
            db.session.commit()

            new_user = user_datastore.find_user(username=username)
            user_datastore.deactivate_user(new_user)
            db.session.commit()

            new_company = Company(user_id=new_user.id, name=user_cred['name'], hr_contact=user_cred['hr_contact'] , website=user_cred['website'] , approval_status="pending")
            db.session.add(new_company)
            db.session.commit()

            result = {
                'message': 'Application for company registeration successful, awaiting an admin review.',
                'user': {
                    'username': username,
                    'email': email
                }
            }
        
            return make_response(
                jsonify(result),
                201                                                                      )
    

class LogoutUser(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        result = {
            'message': 'Logout successful.'
        }

        return make_response(
            jsonify(result),
            200
        )



