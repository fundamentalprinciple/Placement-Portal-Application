import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/resumes'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        department = Department.query.get(student.degree)
        result = {
            'name': student.name,
            'degree': department.name if department else student.degree,
            'cgpa': student.cgpa,
            'year': student.year,
            'resume_filename': student.resume_filename
        }
        return make_response(
            jsonify(result),
            200
        )
    
    @auth_token_required
    @roles_required("student")
    def post(self):
        user = current_user
        student = Student.query.filter_by(user_id=user.id).first()
        
        if request.form:
            if request.form.get('name'):
                student.name = request.form.get('name')
            if request.form.get('degree'):
                student.degree = request.form.get('degree')
            if request.form.get('cgpa'):
                student.cgpa = float(request.form.get('cgpa'))
            if request.form.get('year'):
                student.year = request.form.get('year')
            
            if 'resume' in request.files:
                file = request.files['resume']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(f"{student.id}_{user.username}_{file.filename}")
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    student.resume_filename = filename
                elif file and file.filename:
                    result = {
                        'message': 'Invalid file type. Only PDF, DOC, and DOCX files are allowed.'
                    }
                    return make_response(jsonify(result), 400)
            
            db.session.commit()
            result = {
                'message': 'Profile updated successfully.'
            }
            return make_response(jsonify(result), 200)
        
        else:
            result = {
                'message': 'No data provided.'
            }
            return make_response(jsonify(result), 400)


class DownloadResume(Resource):
    
    @auth_token_required
    @roles_required("student")
    def get(self):
        user = current_user
        student = Student.query.filter_by(user_id=user.id).first()
        
        if not student or not student.resume_filename:
            result = {'message': 'No resume found.'}
            return make_response(jsonify(result), 404)
        
        file_path = os.path.join(UPLOAD_FOLDER, student.resume_filename)
        if not os.path.exists(file_path):
            result = {'message': 'Resume file not found.'}
            return make_response(jsonify(result), 404)
        
        from flask import send_file
        return send_file(file_path, as_attachment=True)        



class ApplyPlacementDrive(Resource):
    
    @auth_token_required
    @roles_required("student")
    def get(self):
        user_id = current_user.id
        stu_id = Student.query.filter_by(user_id=user_id).first().id
        applications = Application.query.filter_by(student_id=stu_id).all()
        
        appList=[]
        for app in applications:
            appList.append({
                "id": app.id,
                "company_name": Company.query.get(PlacementDrive.query.get(app.drive_id).company_id).name,
                "job_title": PlacementDrive.query.get(app.drive_id).job_title,
                "job_description": PlacementDrive.query.get(app.drive_id).job_description,
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
        if not drive_id:
            result = {
                'message': 'drive_id required'
            }
            return make_response(
                jsonify(result),
            )
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
        try:
            db.session.add(new_application)
            db.session.commit()
        except:
            db.session.rollback()
            return make_response(jsonify({
            'message': 'You have already applied to this drive or a constraint failed.'
            }), 409)

        result = {
            'message': f'Application to drive {drive_id} made.'

        }
        return make_response(
            jsonify(result),
            200
        )

    @auth_token_required
    @roles_required("student")
    def delete(self):
        post_cred = request.get_json()
        app_id = post_cred['app_id']
        if not app_id:
            result = {
                'message': 'drive_id required'
            }
            return make_response(
                jsonify(result),
            )
        app = Application.query.get(app_id)
        if not app:
            result = {
                'message': f'No application with id {app_id}'
            }
            return make_response(
                jsonify(result),
                404
            )
        db.session.delete(app)
        db.session.commit()
    
        result = {
            'message': f'Application deleted.'

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

class SearchDrives(Resource):

    @auth_token_required
    @roles_required("student")
    def post(self):
        post_cred = request.get_json() or {}
        search_term = (post_cred.get('search') or '').strip().lower()
        
        if not search_term:
            return make_response(jsonify([]), 200)

        drives = PlacementDrive.query.filter_by(status='approved').all()
        results = []
        
        for drive in drives:
            company = Company.query.get(drive.company_id)
            if company and search_term in company.name.lower():
                results.append({
                    'id': drive.id,
                    'company_id': company.id,
                    'company_name': company.name,
                    'job_title': drive.job_title,
                    'label': f"{company.name} ({drive.job_title})"
                })
        
        results.sort(key=lambda x: x['label'].lower())
        return make_response(jsonify(results), 200)


class ManageInterviewRequest(Resource):
    
    @auth_token_required
    @roles_required("student")
    def get(self):
        student_id = Student.query.filter_by(user_id=current_user.id).first().id
        interviews = ScheduledInterview.query.filter_by(student_id=student_id).all()
        result = []
        for interview in interviews:
            company = Company.query.get(interview.company_id)
            result.append({
                'id': interview.id,
                'company_name': company.name if company else None,
                'company_message': interview.company_message,
                'interview_date': interview.interview_date.isoformat() if interview.interview_date else None,
                'interview_time': interview.interview_time.strftime('%H:%M') if interview.interview_time else None,
                'interview_address': interview.interview_address,
                'accepted': interview.accepted,
                'completed': interview.completed
            })

        return make_response(jsonify(result), 200)


    @auth_token_required
    @roles_required("student")
    def post(self):
        post_cred = request.get_json() or {}
        interview_id = post_cred.get('interview_id')
        accept = post_cred.get('accept')

        if not interview_id or accept is None:
            result = {'message': "'interview_id' and 'accept' are required."}
            return make_response(jsonify(result), 400)

        interview = ScheduledInterview.query.get(interview_id)
        if not interview:
            result = {'message': 'Interview not found.'}
            return make_response(jsonify(result), 404)

        student = Student.query.filter_by(user_id=current_user.id).first()
        if interview.student_id != student.id:
            result = {'message': 'Not authorized to modify this interview.'}
            return make_response(jsonify(result), 403)

        if accept is True:
            interview.accepted = True
            db.session.commit()
            result = {'message': f'Interview {interview_id} accepted.'}
            return make_response(jsonify(result), 200)

        if accept is False:
            db.session.delete(interview)
            db.session.commit()
            result = {'message': f'Interview {interview_id} cancelled.'}
            return make_response(jsonify(result), 200)

        result = {'message': "Invalid value for 'accept'; use true or false."}
        return make_response(jsonify(result), 400) 


class ManageRecruitmentRequest(Resource):
    
    @auth_token_required
    @roles_required("student")
    def get(self):
        student = Student.query.filter_by(user_id=current_user.id).first()
        requests = RecruitmentRequest.query.filter_by(student_id=student.id).all()
        
        result = []
        for req in requests:
            drive = PlacementDrive.query.get(req.drive_id)
            company = Company.query.get(req.company_id)
            result.append({
                'id': req.id,
                'drive_id': req.drive_id,
                'company_name': company.name,
                'job_title': drive.job_title,
                'status': req.status,
                'created_date': req.created_date
            })
        
        return make_response(jsonify(result), 200)
    
    @auth_token_required
    @roles_required("student")
    def post(self):
        post_cred = request.get_json()
        request_id = post_cred.get('request_id')
        action = post_cred.get('action')  # 'confirm' or 'cancel'
        
        if not request_id or action not in ['confirm', 'cancel']:
            return make_response(jsonify({'message': 'request_id and action (confirm/cancel) are required'}), 400)
        
        recruitment_request = RecruitmentRequest.query.get(request_id)
        if not recruitment_request:
            return make_response(jsonify({'message': 'Request not found'}), 404)
        
        student = Student.query.filter_by(user_id=current_user.id).first()
        if recruitment_request.student_id != student.id:
            return make_response(jsonify({'message': 'Not authorized'}), 403)
        
        if action == 'confirm':
            recruitment_request.status = 'confirmed'
            recruitment_request.response_date = datetime.datetime.now()
            
            student.available = False
            
            recruitment = Recruitment(
                drive_id=recruitment_request.drive_id,
                student_id=student.id,
                company_id=recruitment_request.company_id, 
                recruitment_date=datetime.datetime.now(),
                annual_salary=0  
            )
            db.session.add(recruitment)
        
        elif action == 'cancel':
            recruitment_request.status = 'cancelled'
            recruitment_request.response_date = datetime.datetime.now()
        
        db.session.commit()
        
        return make_response(jsonify({'message': f'Recruitment request {action}ed'}), 200)


class GetPlacementHistory(Resource):
    
    @auth_token_required
    @roles_required("student")
    def get(self):
        student = Student.query.filter_by(user_id=current_user.id).first()
        
        history = []
        
        applications = Application.query.filter_by(student_id=student.id).all()
        for app in applications:
            drive = PlacementDrive.query.get(app.drive_id)
            company = Company.query.get(drive.company_id)
            history.append({
                'type': 'application',
                'status': app.status,
                'date': app.application_date,
                'company_name': company.name,
                'job_title': drive.job_title,
                'description': f'Applied for {drive.job_title} at {company.name}'
            })
        
        recruitment_requests = RecruitmentRequest.query.filter_by(student_id=student.id).all()
        for req in recruitment_requests:
            drive = PlacementDrive.query.get(req.drive_id)
            company = Company.query.get(req.company_id)
            history.append({
                'type': 'recruitment',
                'status': req.status,
                'date': req.created_date,
                'company_name': company.name,
                'job_title': drive.job_title,
                'description': f'Recruitment request from {company.name} for {drive.job_title}'
            })
        
        recruitments = Recruitment.query.filter_by(student_id=student.id).all()
        for rec in recruitments:
            drive = PlacementDrive.query.get(rec.drive_id)
            company = Company.query.get(drive.company_id)
            history.append({
                'type': 'placement',
                'status': 'confirmed',
                'date': rec.recruitment_date,
                'company_name': company.name,
                'job_title': drive.job_title,
                'description': f'Placed at {company.name} for {drive.job_title}'
            })
        
        history.sort(key=lambda x: x['date'], reverse=True)
        
        return make_response(jsonify(history), 200)
