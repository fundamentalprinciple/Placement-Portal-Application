import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS

from flask_security import Security
from flask_restful import Api

from application.config import Config
from application.database import db
from application.user_datastore import user_datastore

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Security(app, user_datastore)

    api = Api(app)
    return app, api

def init_db(app):
    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator role')
        student_role = user_datastore.find_or_create_role(name='student', description='Student role')
        company_role = user_datastore.find_or_create_role(name="company", description="Company role")

        admin_user = user_datastore.find_user(username='admin')
        if not admin_user:
            user_datastore.create_user(
                username='admin',
                email = 'admin@admin.com',
                password = os.getenv('Admin'),
                roles=[admin_role]
            )

        db.session.commit()

app, api = create_app()
CORS(app) 

from application.auth_api import LoginUser, LogoutUser, RegisterUser
from application.crud_api import CompanyApplication

#auth apis
api.add_resource(RegisterUser, '/api/register')
api.add_resource(LoginUser, '/api/login')
api.add_resource(LogoutUser, '/api/logout')

#crud apis
#Admin access
api.add_resource(CompanyApplication,'/api/company-application')

'''
api.add_resource(ManageDrive,'/api/manage-drive')

#Company access
api.add_resource(CreateDrive,'/api/create-drive')
api.add_resource(,)
api.add_resource(,)

#Student access
api.add_resource(,)
api.add_resource(,)
api.add_resource(,)
'''

if __name__ == '__main__':
    init_db(app) 
    app.run(debug = True, host="127.0.0.1", port=3000)

