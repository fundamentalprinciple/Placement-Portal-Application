import datetime

from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user, utils, auth_token_required, roles_required

from ...user_datastore import user_datastore
from ...database import db
from ...models import *


from flask import send_file
import os

class DownloadStudentResume(Resource):

    @auth_token_required
    def get(self, student_id):
        student = Student.query.get(student_id)
        if not student or not student.resume_filename:
            return make_response(jsonify({'message': 'Resume not found.'}), 404)

        if current_user.has_role('student'):
            if student.user_id != current_user.id:
                return make_response(jsonify({'message': 'Not authorized.'}), 403)

        elif current_user.has_role('company'):
            company = Company.query.filter_by(user_id=current_user.id).first()
            if not company:
                return make_response(jsonify({'message': 'Not authorized.'}), 403)

            has_application = Application.query.join(PlacementDrive).filter(
                Application.student_id == student_id,
                PlacementDrive.company_id == company.id
            ).first()

            has_interview = ScheduledInterview.query.filter_by(
                student_id=student_id,
                company_id=company.id
            ).first()

            if not has_application and not has_interview:
                return make_response(jsonify({'message': 'Not authorized.'}), 403)

        elif not current_user.has_role('admin'):
            return make_response(jsonify({'message': 'Not authorized.'}), 403)

        file_path = os.path.join('uploads/resumes', student.resume_filename)
        if not os.path.exists(file_path):
            return make_response(jsonify({'message': 'Resume file not found.'}), 404)

        return send_file(file_path, as_attachment=True)


class GetStudentProfile(Resource):

    @auth_token_required
    def get(self, id):
        student = Student.query.get(id)
        if not student:
            return make_response(jsonify({'message': 'Student not found.'}), 404)

        user = User.query.get(student.user_id)
        department = Department.query.get(student.degree)

        result = {
            'id': student.id,
            'user_id': student.user_id,
            'name': student.name,
            'gender': student.gender,
            'degree': department.name if department else student.degree,
            'cgpa': student.cgpa,
            'year': student.year,
            'available': student.available,
            'account_status': user.active if user else None,
            'resume_filename': student.resume_filename
        }
        return make_response(jsonify(result), 200)




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
