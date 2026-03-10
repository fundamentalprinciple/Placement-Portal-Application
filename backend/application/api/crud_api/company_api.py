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
                    "drive_id": app.drive_id,
                    "job_title": PlacementDrive.query.get(app.drive_id).job_title,
                    "student_name": Student.query.get(app.student_id).name,
                    "application_date": app.application_date,
                    "status": app.status
                })
        return make_response(
            jsonify(result),
            200
        )
