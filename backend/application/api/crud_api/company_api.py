import datetime

from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user, utils, auth_token_required, roles_required

from ...user_datastore import user_datastore
from ...database import db
from ...models import *


class CreateDrive(Resource):

    @auth_token_required
    @roles_required("company")
    def post(self):
        post_cred = request.get_json()

        if not(post_cred['job_title'] or post_cred['job_description'] or post_cred['eligibility_criteria'] or post_cred['deadline']):
            result = {
                'message': "Fields job_title, job_description, eligibility_criteria and deadline are required."
            }
            return make_response(
                jsonify(result),
                400
            )
        d = post_cred['deadline'].split('-')
        Drive = PlacementDrive(company_id=Company.query.filter_by(user_id=current_user.id).first().id, job_title=post_cred['job_title'], job_description=post_cred['job_description'], eligibility_criteria=post_cred['eligibility_criteria'], deadline=datetime.datetime(int(d[0]),int(d[1]),int(d[2])), status="pending")
        db.session.add(Drive)
        db.session.commit()

        result = {
            'message': 'Drive created successfully.'
        }
        return make_response(
            jsonify(result),
            200
        )


class ManageApplications(Resource):
    
    @auth_token_required
    @roles_required("company")
    def get(self):
        user_id = current_user.id
        drives = PlacementDrive.query.filter_by(company_id=Company.query.filter_by(user_id=user_id).first().id)
        applications = [] # a list of lists of applications
        for drive in drives:
            applications.append(Application.query.filter_by(drive_id=drive.id))

        result = []
        for appList in applications:
            for app in appList:
                result.append({
                    "application_id": app.id,
                    "drive_id": app.drive_id,
                    "job_title": PlacementDrive.query.get(app.drive_id).job_title,
                    "student_id": Student.query.get(app.student_id).id,
                    "student_name": Student.query.get(app.student_id).name,
                    "application_date": app.application_date,
                    "status": app.status
                })
        return make_response(
            jsonify(result),
            200
        )

   
    @auth_token_required
    @roles_required("company")
    def post(self):
        post_cred = request.get_json()
        application_id = post_cred['application_id']
        new_status = post_cred['new_status']

        application = Application.query.get(application_id)
        if not application:
            result = {
                'message': f'No application with id {application_id} exists.'
            }
            return make_response(
                jsonify(result),
                404
            )

        if new_status not in ('applied','shortlisted','selected','rejected'):
            result = {
                'message': "Only values 'applied','shortlisted','selected','rejected' are allowed for status"
            }
            return make_response(
                jsonify(result),
                403
            )

        if application.status == new_status:
            result = {
                'message': 'Application status is already set to {new_status}'
            }
            return make_response(
                jsonify(result),
                200
            )
        
        application.status = new_status
        db.session.commit()
        result = {
            'message': f'Status successfully set to {new_status}'
        }
        return make_response(
            jsonify(result),
            200
        )       


class ScheduleInterview(Resource):
   
    @auth_token_required
    @roles_required("company")
    def get(self):
        company_id=Company.query.filter_by(user_id=current_user.id).first().id
        interviews = ScheduledInterview.query.filter_by(company_id=company_id).all()
        result = []
        for interview in interviews:
            result.append({
                'id': interview.id,
                'student_id': interview.student_id,
                'company_message': interview.company_message
            }) 

        return make_response(
            jsonify(result),
            200
        )

 
    @auth_token_required
    @roles_required("company")
    def post(self):
        post_cred = request.get_json()
        if not (post_cred['student_id'] or post_cred['message']):
            result = {
                'message': "'student_id' and 'message' are required."
            }
            return make_response(
                jsonify(appList),
                403
            )

        old_interview = ScheduledInterview.query.filter_by(student_id=post_cred['student_id']).first()
        if old_interview:
            result = {
                'message': f"An interview with student {post_cred['student_id']} is already scheduled."
            }
            return make_response(
                jsonify(result),    
                200
            )

        new_interview = ScheduledInterview(company_id=Company.query.filter_by(user_id=current_user.id).first().id , student_id=post_cred['student_id'], company_message = post_cred['message'])

        db.session.add(new_interview)
        db.session.commit()
        result = {
            'message': f"Interview with student {post_cred['student_id']} scheduled."
        }
        return make_response(
            jsonify(result),
            200
        )


class Recruit(Resource):
    
    @auth_token_required
    @roles_required("company")
    def get(self):
        company = Company.query.filter_by(user_id=current_user.id).first()
        recruitments = Recruitment.query.filter_by(company_id=company.id).all()
        recList = []
        for rec in recruitments:
            recList.append({
                'rec_id': rec.id,
                'recruitment_date': rec.recruitment_date,
                'drive_id': rec.drive_id,
                'job_title': PlacementDrive.query.get(rec.drive_id).first().job_title,
                'student_id': rec.student_id,
                'student_name': Student.query.get(rec.student_id).first().name 
            })
        return make_response(
            jsonify(recList),
            200
        )

    @auth_token_required
    @roles_required("company")
    def post(self):
        post_cred = request.get_json()
        company_id = Company.query.filter_by(user_id=current_user.id).first().id
        student_id = post_cred['student_id']
        drive_id = post_cred['drive_id']
        if not(student_id or drive_id):
            result = {
                'message': 'Fields student_id and drive_id are required.'
            }
            return make_response(
                jsonify(result),
                404
            )
        
        student = Student.query.get(student_id)
        drive = PlacementDrive.query.get(drive_id)
        if not(student or drive):
            result = {
                'message': f'Student with id {student_id} or Drive with id {drive_id} do not exist.'
            }    
            return make_response(
                jsonify(result),
                404
            )

        old_recruitment = Recruitment.query.filter_by(student_id=student_id).first()
        if (old_recruitment) or (student.available==False):
            result = {
                'message': f'The student with id {student_id} is not available for recruitment for now.'
            }
            return make_response(
                jsonify(result),
                403
            )

        new_recruitment = Recruitment(drive_id=drive_id, student_id=student_id, company_id=company_id, recruitment_date=datetime.datetime.now())
        db.session.add(new_recruitment)
        student.available = False
        db.session.commit()
        result = {
            'message': 'New recruitment added successfully.'
        } 
        return make_response(
            jsonify(result),
            200
        )
