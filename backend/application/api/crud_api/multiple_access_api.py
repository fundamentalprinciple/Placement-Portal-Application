import datetime

from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user, utils, auth_token_required, roles_required

from ...user_datastore import user_datastore
from ...database import db
from ...models import *

class ViewApprovedDrives(Resource):

    @auth_token_required
    def get(self):
        drives = PlacementDrive.query.all()
        DriveList = []
        for drive in drives:
            if drive.status != "approved":
                continue
            DriveList.append({
                'id': drive.id,
                'company_id': drive.company_id,
                'job_title': drive.job_title,
                'job_description': drive.job_description,
                'eligibility_criteria': drive.eligibility_criteria,
                'deadline': drive.deadline
            })
        return make_response(
            jsonify(DriveList),
            200
        )

class ViewPlacementHistory(Resource):

    @auth_token_required
    def get(self):
        placements = Recruitment.query.all()
        placementList = []
        for rec in placements:
            placementList.append({
                'recruitment_date': rec.recruitment_date,
                'job_title': PlacementDrive.query.get(rec.drive_id).first().job_title,
                'student_name': Student.query.get(rec.student_id).first().name,
                'annual_salary': rec.annual_salary
            })
        return make_response(
            jsonify(placementList),
            200
        )
