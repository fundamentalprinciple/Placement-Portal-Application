import json
from celery import shared_task
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from .database import db
from .models import PlacementDrive, Student, Application, User
from main import create_app

app, _ = create_app()
mail = Mail(app)

def parse_criteria(text):
    try:
        data = json.loads(text)
        if isinstance(data, list):
            branch = data[0]
            if isinstance(branch, list):
                branch = branch[0]
            cgpa = float(data[1]) if len(data) > 1 else 0.0
            year = str(data[2]) if len(data) > 2 else None
            return branch, cgpa, year
    except Exception:
        pass
    parts = [p.strip() for p in text.split(',')]
    branch = parts[0] if len(parts) > 0 else None
    cgpa = float(parts[1]) if len(parts) > 1 and parts[1] else 0.0
    year = parts[2] if len(parts) > 2 else None
    return branch, cgpa, year

@shared_task
def send_daily_reminders():
    with app.app_context():
        tomorrow = datetime.now().date() + timedelta(days=1)
        upcoming_drives = PlacementDrive.query.filter(
            PlacementDrive.deadline == tomorrow,
            PlacementDrive.status == 'approved'
        ).all()

        print(f"DEBUG: Found {len(upcoming_drives)} drives with tomorrow deadline")        

        for drive in upcoming_drives:
            eligible_students = get_eligible_students(drive)
            print(f"DEBUG: Drive '{drive.job_title}' has {len(eligible_students)} eligible students")

            for student in eligible_students:
                if not has_applied(student, drive):
                    send_reminder(student, drive)

def get_eligible_students(drive):
    import json
    try:
        criteria_data = json.loads(drive.eligibility_criteria)
        if isinstance(criteria_data, list):
            branch_criteria = criteria_data[0]
            if isinstance(branch_criteria, list):
                branch_criteria = branch_criteria[0]
            cgpa_criteria = float(criteria_data[1]) if len(criteria_data) > 1 else 0.0
            year_criteria = str(criteria_data[2]) if len(criteria_data) > 2 else None
        else:
            branch_criteria = None
            cgpa_criteria = 0.0
            year_criteria = None
    except (json.JSONDecodeError, ValueError, IndexError):
        parts = drive.eligibility_criteria.split(',')
        branch_criteria = parts[0].strip() if len(parts) > 0 else None
        cgpa_criteria = float(parts[1].strip()) if len(parts) > 1 else 0.0
        year_criteria = parts[2].strip() if len(parts) > 2 else None

    print(f"DEBUG: Parsed criteria - branch: '{branch_criteria}', cgpa: {cgpa_criteria}, year: '{year_criteria}'")
    
    query = Student.query.filter(Student.available == True)
    
    if branch_criteria:
        query = query.filter(Student.degree == branch_criteria)
    if cgpa_criteria > 0:
        query = query.filter(Student.cgpa >= cgpa_criteria)
    if year_criteria:
        query = query.filter(Student.year >= year_criteria)

    result = query.all()
    
    print(f"DEBUG: Query returned {len(result)} students")    

    return result

def has_applied(student, drive):
    return Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first() is not None

def send_reminder(student, drive):
    user = User.query.get(student.user_id)
    if not user:
        return
    subject = f"Reminder: Application deadline for {drive.job_title} tomorrow"
    body = f"Dear {student.name},\n\nThe application deadline for {drive.job_title} at {drive.company.name} is tomorrow ({drive.deadline}).\n\nPlease apply if you haven't already.\n\nBest regards,\nPlacement Portal Team"
    send_email(user.email, subject, body)
    print(f"SMS TO {user.email}: {body}")
    print(f"WEBHOOK: {body}")

def send_email(recipient, subject, body):
    if not app.config.get('MAIL_USERNAME'):
        print(f"EMAIL TO {recipient}: {body}")
        return
    msg = Message(subject, recipients=[recipient], sender="server@ppa.com")
    msg.body = body
    mail.send(msg)
