import datetime

from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user, utils, auth_token_required, roles_required

from ...user_datastore import user_datastore
from ...database import db
from ...models import *


class SelfManageStudentProfile(Resource):
    
    @auth_token_required
    @roles_required("student")
    def get(self):
        user  = current_user
        student = Student.query.filter_by(user_id=user.id).first()
        result = {
            'name': student.name,
            'degree': student.degree,
            'cgpa': student.cgpa,
            'year': student.year,
        }
        return make_response(
            jsonify(result),
            200
        )
    
    @auth_token_required
    @roles_required("student")
    def post(self):
        post_cred = request.get_json()
        if not(post_cred['name'] or post_cred['degree'] or post_cred['cgpa'] or post_cred['year']):
            result = {
                'message': 'All fields required. Leave unwanted fields empty.'
            }
            return make_response(
                jsonify(result),
                403
            )
        
        user  = current_user
        student = Student.query.filter_by(user_id=user.id).first()
        
        if post_cred['name'] !='':
            student.name = post_cred['name']
        if post_cred['degree'] !='':    
            student.degree = post_cred['degree']
        if post_cred['cgpa'] !='':    
            student.cgpa = post_cred['cgpa']
        if post_cred['year'] !='':    
            student.year = post_cred['year']      
        db.session.commit()    
        
        result = {
            'message': 'Changes to profile made successfully.'
        }
        return make_response(
            jsonify(result),
            200
        )
        
class ApplyPlacementDrive(Resource):
    
    @auth_token_required
    @roles_required("student")
    def get(self): # A bug
        user_id = current_user.id
        stu_id = Student.query.filter_by(user_id=user_id).first().id
        applications = Application.query.filter_by(student_id=stu_id).all()
        
        appList=[]
        for app in applications:
            appList.append({
                "drive_id": app.drive_id,
                "company_name": Company.query.get(PlacementDrive.query.get(app.drive_id).company_id).name,
                "job_title": PlacementDrive.query.get(app.drive_id).job_title,
                "application_date": app.application_date,
                "status": app.status
            })
        return make_response(
            jsonify(appList),
            200
        )
        
    @auth_token_required
    @roles_required("student")
    def post(self):
        post_cred = request.get_json()
        drive_id = post_cred['drive_id']
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            result = {
                'message': f'No drive with id {drive_id}'
            }
            return make_response(
                jsonify(result),
                404
            )
        student = Student.query.filter_by(user_id=current_user.id).first()
        new_application = Application(student_id=student.id, drive_id=drive.id, application_date=datetime.datetime.now(), status="applied")
        db.session.add(new_application)
        db.session.commit()

        result = {
            'message': f'Application to drive {drive_id} made.'

        }
        return make_response(
            jsonify(result),
            200
        )
                

class ViewApplicationStatus(Resource):
    
    @auth_token_required
    @roles_required("student")
    def get(self):
        user_id = current_user.id
        stu_id = Student.query.filter_by(user_id=user_id).first().id
        applications = Application.query.filter_by(student_id=stu_id)

        appList=[]
        for app in applications:
            appList.append({
                "drive_id": app.drive_id,
                "company_name": Company.query.get(PlacementDrive.query.get(app.drive_id).company_id).name,
                "job_title": PlacementDrive.query.get(app.drive_id).job_title,
                "application_date": app.application_date,
                "status": app.status
            })
        return make_response(
            jsonify(appList),
            200
        )


class ManageInterviewRequest(Resource):
    
    @auth_token_required
    @roles_required("student")
    def get(self):
        student_id = Student.query.filter_by(user_id=current_user.id).first().id
        interviews = ScheduledInterview.query.filter_by(student_id=student_id).all()
        result = []
        for interview in interviews:
            result.append({
                'id': interview.id,
                'company_id': interview.company_id,
                'company_message': interview.company_message
            })

        return make_response(
            jsonify(result),
            200
        )


    def post(self):
        post_cred = request.get_json()
        if not(post_cred['interview_id']):
            result = {
                'message': 'Specify an interview_id to accept request.'
            }
            return make_request(
                jsonify(result),
                404
            )
        
