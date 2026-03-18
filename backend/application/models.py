from .database import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Enum

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    roles = db.relationship('Roles', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))


class Roles(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)


class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.String(255), nullable=False)
    eligibility_criteria = db.Column(db.String(255), nullable=False) #csv format (branch, cgpa, year)
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column(Enum('approved','pending','closed'), nullable=False)
    
    company = db.relationship("Company", backref="placement_drives")


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drive.id"), nullable=False)
    application_date = db.Column(db.Date, nullable=False)
    status = db.Column(Enum('applied','shortlisted','selected','rejected'), nullable=False)
    
    student = db.relationship("Student", backref="applications")
    drive  = db.relationship("PlacementDrive", backref="applications")


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    name = name = db.Column(db.String(150), unique=True, nullable=False)
    hr_contact = db.Column(db.Text, nullable=False) #email
    website = db.Column(db.Text, nullable=False) 
    approval_status = db.Column(Enum('approved','pending','rejected'), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    name = db.Column(db.String(150), nullable=False)
    gender = db.Column(Enum('Male','Female','Trans'), nullable=False) 
    degree = db.Column(db.ForeignKey('department.id'), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    year = db.Column(Enum('2021','2022','2023','2024','2025','2026'), nullable=False)
    available = db.Column(db.Boolean(), default=True)    

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

def seed_departments():
    departments = [
        Department(name="Computer Engineering"),
        Department(name="Computer Science Engineering"),
        Department(name="Electrical Engineering"),
        Department(name="Mechanical Engineering"),
        Department(name="Civil Engineering"),
        Department(name="Chemical Engineering"),
        Department(name="Aerospace Engineering"),
        Department(name="Automotive Engineering"),
        Department(name="Robotics Engineering"),
        Department(name="Nanotechnology Engineering"),
        Department(name="Data Science and Applications"),
        Department(name="Electronic Systems"),
        Department(name='Management and Data Science')
    ]
    for dept in departments:
        existing = Department.query.filter_by(id=dept.id).first()
        if not existing:
            db.session.add(dept)
    db.session.commit()    
    return


class ScheduledInterview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), unique=True, nullable=False)
    company_message = db.Column(db.Text, nullable=True)
    accepted = db.Column(db.Boolean(), default=False)

class Recruitment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), unique=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    recruitment_date = db.Column(db.Date, nullable=False)
    annual_salary = db.Column(db.Numeric(10,2), nullable=False) #In rupees, like 2200000.00

