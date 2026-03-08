import datetime

from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user, utils, auth_token_required, roles_required

from .user_datastore import user_datastore
from .database import db
from .models import *

#Multiple access
class Drives(Resource):

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

#Admin access
class CompanyApplication(Resource):
    
    @auth_token_required
    @roles_required("admin")
    def get(self):
        companies = Company.query.all()
        companyList = []
        for comp in companies:
            companyList.append({
                'id': comp.id,
                'user_id': comp.user_id,
                'name': comp.name,
                'hr_contact': comp.hr_contact,
                'website': comp.website,
                'approval_status': comp.approval_status
            })
        return make_response(
            jsonify(companyList),
            200
        )

    @auth_token_required
    @roles_required("admin")
    def post(self):
        post_cred = request.get_json()
        comp_id = post_cred['id']
        new_status = post_cred['new_status']

        if not (comp_id or new_status):
            result = {
                'message': "Fields id and new_status are required."
            }
            return make_response(
                jsonify(result),
                400
            )

        company = Company.query.get(comp_id)

        if not company:
            result = {
                'message': f"No company with id={comp_id} exists."
            }
            return make_response(
                jsonify(result),
                404
            )

        user = User.query.get(company.user_id)
        if new_status not in ('approved','pending','rejected'):
            result = {
                'message': "Invalid status, valid values are 'approved','pending' and 'rejected'."
            }
            return make_response(
                jsonify(result),
                400
            )

        if company.approval_status == new_status:
            result = {
                'message': f"Company approval status is already set to {new_status}."
            }
            return make_response(
                jsonify(result),
                200
            )
        
        if new_status == 'approved':
            user_datastore.activate_user(user)
        else:
            user_datastore.deactivate_user(user)

        company.approval_status = new_status
        db.session.commit()
        result = {
            'message': f'Company status set to {new_status}.'
        }              
        return make_response(
            jsonify(result),
            200
        )

class ManageDrives(Resource):
        
    @auth_token_required
    @roles_required("admin")
    def get(self):
        drives = PlacementDrive.query.all()
        DriveList = []
        for drive in drives:
            DriveList.append({
                'id': drive.id,
                'company_id': drive.company_id,
                'job_title': drive.job_title,
                'job_description': drive.job_description,
                'eligibility_criteria': drive.eligibility_criteria,
                'deadline': drive.deadline,
                'status': drive.status
            })
        return make_response(
            jsonify(DriveList),
            200
        )

    @auth_token_required
    @roles_required("admin")
    def post(self):
        post_cred = request.get_json()
        drive_id = post_cred['id']
        new_status = post_cred['new_status']

        if not (drive_id or new_status):
            result = {
                'message': "Fields id and new_status are required."
            }
            return make_response(
                jsonify(result),
                400
            )

        drive = PlacementDrive.query.get(drive_id)

        if not drive:
            result = {
                'message': f"No drive with id={drive_id} exists."
            }
            return make_response(
                jsonify(result),
                404
            )

        if new_status not in ('approved','pending','rejected'):
            result = {
                'message': "Invalid status, valid values are 'approved','pending' and 'rejected'."
            }
            return make_response(
                jsonify(result),
                400
            )

        if drive.status == new_status:
            result = {
                'message': f"Company approval status is already set to {new_status}."
            }
            return make_response(
                jsonify(result),
                200
            )

        drive.status = new_status
        db.session.commit()
        result = {
            'message': f'Company status set to {new_status}.'
        }
        return make_response(
            jsonify(result),
            200
        )
         

#Company access

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
        Drive = PlacementDrive(company_id=current_user.id, job_title=post_cred['job_title'], job_description=post_cred['job_description'], eligibility_criteria=post_cred['eligibility_criteria'], deadline=datetime.datetime(int(d[0]),int(d[1]),int(d[2])), status="pending") 
        db.session.add(Drive)
        db.session.commit()
        
        result = {
            'message': 'Drive created successfully.'
        }
        return make_response(
            jsonify(result),
            200
        )
        

#Student access





