import datetime

from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user, utils, auth_token_required, roles_required

from ...user_datastore import user_datastore
from ...database import db
from ...models import *


class CompanyProfile(Resource):
    
    @auth_token_required
    @roles_required("company")
    def get(self):
        company = Company.query.filter_by(user_id=current_user.id).first()
        user = User.query.get(company.user_id)
        result = {
            'name': company.name,
            'hr_contact': company.hr_contact,
            'website': company.website,
            'email': user.email if user else None,
            'approval_status': company.approval_status,
            'pending_name': company.pending_name,
            'pending_hr_contact': company.pending_hr_contact,
            'pending_website': company.pending_website
        }
        return make_response(jsonify(result), 200)
    
    @auth_token_required
    @roles_required("company")
    def post(self):
        post_cred = request.get_json() or {}
        company = Company.query.filter_by(user_id=current_user.id).first()
        
        if 'name' in post_cred and post_cred['name'].strip():
            company.pending_name = post_cred['name'].strip()
        if 'hr_contact' in post_cred and post_cred['hr_contact'].strip():
            company.pending_hr_contact = post_cred['hr_contact'].strip()
        if 'website' in post_cred and post_cred['website'].strip():
            company.pending_website = post_cred['website'].strip()
        
        db.session.commit()
        result = {
            'message': 'Profile changes submitted for admin approval. Your current profile remains active.'
        }
        return make_response(jsonify(result), 200)


class CreateDrive(Resource):

    @auth_token_required
    @roles_required("company")
    def get(self):
        company = Company.query.filter_by(user_id=current_user.id).first()
        company_id = company.id
        drives = PlacementDrive.query.filter_by(company_id=company_id).all()

        DriveList = []
        for drive in drives:
            DriveList.append({
                'id': drive.id,
                'company_id': drive.company_id,
                'company_name': Company.query.get(drive.company_id).name,
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

    
    @auth_token_required
    @roles_required("company")
    def delete(self):
        drive_id = int(request.get_json()['id'])
        if not(drive_id):
            result = {
                'message': "Drive ID is required."
            }
            return make_response(
                jsonify(result),
                404
            )

        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            result = {
                'message': 'Drive not found.'
            }
            return make_response(
                jsonify(result),
                404
            )

        db.session.delete(drive)
        db.session.commit()
        
        result = {
            'message': 'Drive deleted successfully.'
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
                    "id": app.id,
                    "drive_id": app.drive_id,
                    "job_title": PlacementDrive.query.get(app.drive_id).job_title,
                    "student_id": Student.query.get(app.student_id).id,
                    "student_name": Student.query.get(app.student_id).name,
                    "student_qualifications": f'["{Student.query.get(app.student_id).degree}",{Student.query.get(app.student_id).cgpa},{Student.query.get(app.student_id).year}]',
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
        print("*"*100)
        print(post_cred)
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

class SearchApplications(Resource):

    @auth_token_required
    @roles_required("company")
    def post(self):
        post_cred = request.get_json() or {}
        search_term = (post_cred.get('search') or '').strip().lower()
        
        if not search_term:
            return make_response(jsonify([]), 200)

        company = Company.query.filter_by(user_id=current_user.id).first()
        company_id = company.id
        
        drives = PlacementDrive.query.filter_by(company_id=company_id).all()
        applications = []
        
        for drive in drives:
            drive_apps = Application.query.filter_by(drive_id=drive.id).all()
            for app in drive_apps:
                student = Student.query.get(app.student_id)
                if student and search_term in student.name.lower():
                    applications.append({
                        'id': app.id,
                        'student_id': student.id,
                        'student_name': student.name,
                        'job_title': drive.job_title,
                        'label': f"{student.name} ({drive.job_title})"
                    })
        
        applications.sort(key=lambda x: x['label'].lower())
        return make_response(jsonify(applications), 200)


class ScheduleInterview(Resource):
   
    @auth_token_required
    @roles_required("company")
    def get(self):
        company = Company.query.filter_by(user_id=current_user.id).first()
        company_id = company.id
        interviews = ScheduledInterview.query.filter_by(company_id=company_id).all()

        result = []
        for interview in interviews:
            student = Student.query.get(interview.student_id)
            result.append({
                'id': interview.id,
                'student_id': interview.student_id,
                'student_name': student.name if student else None,
                'company_message': interview.company_message,
                'interview_date': interview.interview_date.isoformat() if interview.interview_date else None,
                'interview_time': interview.interview_time.strftime('%H:%M') if interview.interview_time else None,
                'interview_address': interview.interview_address,
                'accepted': interview.accepted,
                'completed': interview.completed
            })

        return make_response(jsonify(result), 200)
 
    @auth_token_required
    @roles_required("company")
    def post(self):
        post_cred = request.get_json() or {}
        student_id = post_cred.get('student_id')
        message = (post_cred.get('message') or '').strip()
        address = (post_cred.get('address') or '').strip()
        date_str = post_cred.get('date')
        time_str = post_cred.get('time')

        if not student_id or not message or not address or not date_str or not time_str:
            result = {
                'message': "'student_id', 'message', 'address', 'date' and 'time' are required."
            }
            return make_response(jsonify(result), 400)

        student = Student.query.get(student_id)
        if not student:
            result = {
                'message': f'Student with id {student_id} does not exist.'
            }
            return make_response(jsonify(result), 404)

        try:
            interview_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            interview_time = datetime.datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            result = {
                'message': "Date must be YYYY-MM-DD and time must be HH:MM."
            }
            return make_response(jsonify(result), 400)

        old_interview = ScheduledInterview.query.filter_by(student_id=student_id).first()
        if old_interview:
            result = {
                'message': f"An interview with student {student_id} is already scheduled."
            }
            return make_response(jsonify(result), 409)

        new_interview = ScheduledInterview(
            company_id=Company.query.filter_by(user_id=current_user.id).first().id,
            student_id=student_id,
            company_message=message,
            interview_date=interview_date,
            interview_time=interview_time,
            interview_address=address
        )

        db.session.add(new_interview)
        db.session.commit()

        result = {
            'message': f"Interview with student {student_id} scheduled."
        }
        return make_response(jsonify(result), 200)


    @auth_token_required
    @roles_required("company")
    def delete(self):
        post_cred = request.get_json() or {}
        interview_id = post_cred.get('interview_id')
        if not interview_id:
            result = {'message': "'interview_id' is required."}
            return make_response(jsonify(result), 400)

        interview = ScheduledInterview.query.get(interview_id)
        if not interview:
            result = {'message': 'Interview not found.'}
            return make_response(jsonify(result), 404)

        company = Company.query.filter_by(user_id=current_user.id).first()
        if interview.company_id != company.id:
            result = {'message': 'Not authorized to cancel this interview.'}
            return make_response(jsonify(result), 403)

        db.session.delete(interview)
        db.session.commit()

        result = {'message': 'Interview cancelled successfully.'}
        return make_response(jsonify(result), 200)

    @auth_token_required
    @roles_required("company")
    def put(self):
        post_cred = request.get_json() or {}
        interview_id = post_cred.get('interview_id')
        completed = post_cred.get('completed')

        if not interview_id or completed is None:
            result = {'message': "'interview_id' and 'completed' are required."}
            return make_response(jsonify(result), 400)

        interview = ScheduledInterview.query.get(interview_id)
        if not interview:
            result = {'message': 'Interview not found.'}
            return make_response(jsonify(result), 404)

        company = Company.query.filter_by(user_id=current_user.id).first()
        if interview.company_id != company.id:
            result = {'message': 'Not authorized to update this interview.'}
            return make_response(jsonify(result), 403)

        interview.completed = bool(completed)
        db.session.commit()

        result = {'message': 'Interview marked completed.'}
        return make_response(jsonify(result), 200)



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
                'student_name': Student.query.get(rec.student_id).first().name,
                'annual_salary': rec.annual_salary
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
        annual_salary = post_cred['annual_salary']
        if not(student_id or drive_id or annual_salary):
            result = {
                'message': 'Fields student_id, drive_id and annual_salary are required.'
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

        new_recruitment = Recruitment(drive_id=drive_id, student_id=student_id, company_id=company_id, recruitment_date=datetime.datetime.now(), annual_salary=annual_salary)
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
