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
from application.models import seed_departments

from celery_app import celery
from flask_mail import Mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Security(app, user_datastore)

    mail = Mail()
    mail.init_app(app)
    celery.conf.update(app.config)

    api = Api(app)
    
    app.app_context().push()
    return app, api
app, api = create_app()
frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
CORS(app, resources={r'/api/*': {'origins': frontend_url}})

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
        seed_departments()
    return

#auth apis
from application.api.auth_api import LoginUser, LogoutUser, RegisterUser, Authenticate
api.add_resource(RegisterUser, '/api/register')
api.add_resource(LoginUser, '/api/login')
api.add_resource(LogoutUser, '/api/logout')
api.add_resource(Authenticate, '/api/authenticate')

#crud apis
#Multiple roles access
from application.api.crud_api.multiple_access_api import *
api.add_resource(ViewApprovedDrives, '/api/view-approved-drives')
api.add_resource(ViewPlacementHistory, '/api/view-placement-history')
api.add_resource(DownloadStudentResume, '/api/student-resume/<int:student_id>')
api.add_resource(GetStudentProfile, '/api/student-profile/<int:id>')

#Admin access
from application.api.crud_api.admin_api import *
api.add_resource(ManageStudentProfiles, '/api/manage-student-profiles') 
api.add_resource(ManageCompanyProfiles, '/api/manage-company-profiles')
api.add_resource(ManageDrives, '/api/manage-drives')
api.add_resource(ViewPlacementStatistics, '/api/view-placement-statistics')
api.add_resource(SearchUsers, '/api/search-user')
api.add_resource(GetCompanyProfile, '/api/company-profile/<int:id>')
api.add_resource(GetPlacementStatistics, '/api/get-placement-statistics')

#Company access
from application.api.crud_api.company_api import *
api.add_resource(CreateDrive, '/api/create-drive')
api.add_resource(ManageApplications, '/api/manage-applications')
api.add_resource(ScheduleInterview, '/api/schedule-interview')
api.add_resource(CompanyProfile, '/api/company-profile')
api.add_resource(SearchApplications, '/api/search-applications')
api.add_resource(Recruit, '/api/recruit')


#Student access
from application.api.crud_api.student_api import *
api.add_resource(SelfManageStudentProfile, '/api/self-manage-student-profile')
api.add_resource(ApplyPlacementDrive, '/api/apply-placement-drive')
api.add_resource(ViewApplicationStatus, '/api/view-application-status')
api.add_resource(ManageInterviewRequest, '/api/manage-interview-request')
api.add_resource(SearchDrives, '/api/search-drives')
api.add_resource(DownloadResume, '/api/download-resume')
api.add_resource(ManageRecruitmentRequest, '/api/manage-recruitment-request')
api.add_resource(GetPlacementHistory, '/api/get-placement-history')


if __name__ == '__main__':
    init_db(app) 
    app.run(debug = True, host="127.0.0.1", port=3000)

