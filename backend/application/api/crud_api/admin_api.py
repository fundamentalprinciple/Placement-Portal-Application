import datetime

from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user, utils, auth_token_required, roles_required

from ...user_datastore import user_datastore
from ...database import db
from ...models import *

class ManageStudentProfiles(Resource):
    
    @auth_token_required
    @roles_required("admin")
    def get(self):
        students = Student.query.all()
        studentList = []
        for stu in students:
            studentList.append({
                'id': stu.id,
                'user_id': stu.user_id,
                'name': stu.name,
                'degree': stu.degree,
                'cgpa': stu.cgpa,
                'year': stu.year,
                'available': stu.available,
                'account_status': User.query.get(stu.user_id).active
            })
        return make_response(
            jsonify(studentList),
            200
        )
    
    @auth_token_required
    @roles_required("admin")
    def post(self):
        post_cred = request.get_json()
        if not(post_cred['id'] or post_cred['new_status']):
            result = {
                'message': "Fields id and new_status are required."
            }
            return make_response(
                jsonify(result),
                400
            )
        
        student = Student.query.get(post_cred['id'])
        
        if not student:
            result = {
                'message': f"No student with the id exists."
            }
            return make_response(
                jsonify(result),
                404
            ) 
        
        user = User.query.get(student.user_id) 
        if post_cred['new_status'] not in ('activate','deactivate'):
            result = {
                'message': "Invalid status, valid values are 'activate','deactivate'."
            }
            return make_response(
                jsonify(result),
                400
            )
        
        if post_cred['new_status'] == 'activate':
            user_datastore.activate_user(user)
        else:
            user_datastore.deactivate_user(user)
        db.session.commit()
        result = {
            'message': f"Student account set to {post_cred['new_status']}d."
        }
        return make_response(
            jsonify(result),
            200
        )



class ManageCompanyProfiles(Resource):

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
                'email': User.query.get(comp.user_id).email,
                'website': comp.website,
                'approval_status': comp.approval_status,
                'pending_name': comp.pending_name,
                'pending_hr_contact': comp.pending_hr_contact,
                'pending_website': comp.pending_website
            })
        return make_response(jsonify(companyList), 200)

    @auth_token_required
    @roles_required("admin")
    def post(self):
        post_cred = request.get_json()
        comp_id = post_cred.get('id')
        action = post_cred.get('action', 'status')  # 'status' or 'approve_profile'

        if not comp_id:
            result = {'message': "Field 'id' is required."}
            return make_response(jsonify(result), 400)

        company = Company.query.get(comp_id)
        if not company:
            result = {'message': f"No company with id={comp_id} exists."}
            return make_response(jsonify(result), 404)

        if action == 'status':
            new_status = post_cred.get('new_status')
            if not new_status:
                result = {'message': "Field 'new_status' is required for status action."}
                return make_response(jsonify(result), 400)
            
            user = User.query.get(company.user_id)
            if new_status not in ('approved','pending','rejected'):
                result = {'message': "Invalid status, valid values are 'approved','pending' and 'rejected'."}
                return make_response(jsonify(result), 400)

            if company.approval_status == new_status:
                result = {'message': f"Company approval status is already set to {new_status}."}
                return make_response(jsonify(result), 200)

            if new_status == 'approved':
                user_datastore.activate_user(user)
            else:
                user_datastore.deactivate_user(user)

            company.approval_status = new_status
            db.session.commit()
            result = {'message': f'Company status set to {new_status}.'}
            return make_response(jsonify(result), 200)

        elif action == 'approve_profile':
            if company.pending_name:
                company.name = company.pending_name
                company.pending_name = None
            if company.pending_hr_contact:
                company.hr_contact = company.pending_hr_contact
                company.pending_hr_contact = None
            if company.pending_website:
                company.website = company.pending_website
                company.pending_website = None
            db.session.commit()
            result = {'message': 'Company profile changes approved and applied.'}
            return make_response(jsonify(result), 200)

        else:
            result = {'message': "Invalid action. Use 'status' or 'approve_profile'."}
            return make_response(jsonify(result), 400)


class GetCompanyProfile(Resource):

    @auth_token_required
    @roles_required("admin")
    def get(self, id):
        company = Company.query.get(id)
        if not company:
            return make_response(jsonify({'message': 'Company not found.'}), 404)

        user = User.query.get(company.user_id)
        result = {
            'id': company.id,
            'user_id': company.user_id,
            'name': company.name,
            'hr_contact': company.hr_contact,
            'website': company.website,
            'approval_status': company.approval_status,
            'email': user.email if user else None,
            'account_status': user.active if user else None
        }
        return make_response(jsonify(result), 200)



class ManageDrives(Resource):

    @auth_token_required
    def get(self):
        drives = PlacementDrive.query.all()
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

        if new_status not in ('approved','pending','closed'):
            result = {
                'message': "Invalid status, valid values are 'approved','pending' and 'rejected'."
            }
            return make_response(
                jsonify(result),
                400
            )

        if drive.status == new_status:
            result = {
                'message': f"Drive approval status is already set to {new_status}."
            }
            return make_response(
                jsonify(result),
                200
            )

        drive.status = new_status
        db.session.commit()
        result = {
            'message': f'Drive status set to {new_status}.'
        }
        return make_response(
            jsonify(result),
            200
        )

class SearchUsers(Resource):

    @auth_token_required
    @roles_required("admin")
    def post(self):
        post_cred = request.get_json() or {}
        username = (post_cred.get('username') or '').strip()
        if not username:
            return make_response(jsonify([]), 200)

        pattern = f"%{username}%"
        seen = set()
        results = []

        students = Student.query.filter(Student.name.ilike(pattern)).all()
        for stu in students:
            key = ('student', stu.id)
            if key in seen:
                continue
            seen.add(key)
            results.append({
                'id': stu.id,
                'role': 'student',
                'label': f"{stu.name} (student)"
            })

        companies = Company.query.filter(Company.name.ilike(pattern)).all()
        for comp in companies:
            key = ('company', comp.id)
            if key in seen:
                continue
            seen.add(key)
            results.append({
                'id': comp.id,
                'role': 'company',
                'label': f"{comp.name} (company)"
            })

        users = User.query.filter(User.username.ilike(pattern)).all()
        for user in users:
            if not user.roles:
                continue
            role_name = user.roles[0].name
            if role_name == 'student':
                stu = Student.query.filter_by(user_id=user.id).first()
                if stu:
                    key = ('student', stu.id)
                    if key in seen:
                        continue
                    seen.add(key)
                    results.append({
                        'id': stu.id,
                        'role': 'student',
                        'label': f"{stu.name} (student)"
                    })
            elif role_name == 'company':
                comp = Company.query.filter_by(user_id=user.id).first()
                if comp:
                    key = ('company', comp.id)
                    if key in seen:
                        continue
                    seen.add(key)
                    results.append({
                        'id': comp.id,
                        'role': 'company',
                        'label': f"{comp.name} (company)"
                    })

        results.sort(key=lambda item: item['label'].lower())
        return make_response(jsonify(results), 200)


import statistics
class ViewPlacementStatistics(Resource):
    
    @auth_token_required
    @roles_required("admin")
    def get(self):
        placement_rate = (Recruitment.query.count() / Student.query.filter_by(available=True).all().count())*100 

        total_salary = 0
        salaryList = []
        for rec in Recruitment.query:
            total_salary+=rec.annual_salary
            salaryList.append(rec.annual_salary)
        avg_salary = total_salary / Recruitment.query.count()
        
        salaryList.sort() 
        median_salary = statistics.median(salaryList)

        highest_salary = max(salaryList)
        lowest_salary = min(salaryList)
        
        #will see to these later
        #salary_distribution_histogram = 
        #department_wise_placement_piechart = 
        #gender_wise_placement_piechart =
        
        result = {
            'placement_rate': placement_rate,
            'avg_salary': avg_salary,
            'median_salary': median_salary,
            'highest_salary': highest_salary,
            'lowest_salary': lowest_salary
        }
        return make_response(
            jsonify(result),
            200
        ) 
