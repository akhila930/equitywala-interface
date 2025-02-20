from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_manager = db.Column(db.Boolean, default=False)
    department = db.Column(db.String(100))
    hierarchy_level = db.Column(db.Integer, default=0)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    dob = db.Column(db.Date)
    role = db.Column(db.String(100))
    department = db.Column(db.String(100))
    employee_type = db.Column(db.String(50))
    salary = db.Column(db.Float)
    pay_frequency = db.Column(db.String(20), default='monthly')
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    profile_photo = db.Column(db.String(500))
    
    tasks = db.relationship('Task', backref='task_employee', lazy=True)
    attendances = db.relationship('Attendance', backref='attendance_employee', lazy=True)
    milestones = db.relationship('Milestone', backref='milestone_employee', lazy=True)
    documents = db.relationship('Document', backref='document_employee', lazy=True)
    salary_components = db.relationship('SalaryComponent', backref='salary_component_employee', lazy=True)
    salaries = db.relationship('EmployeeSalary', backref='salary_employee', lazy=True)
    assigned_leads = db.relationship('Lead', backref='lead_employee', lazy=True)
    assigned_clients = db.relationship('Client', backref='client_employee', lazy=True)
    received_feedback = db.relationship('EmployeeFeedback', back_populates='employee', lazy=True)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    comments = db.Column(db.Text)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    priority = db.Column(db.String(50), default='medium')
    status = db.Column(db.String(50), default='pending')
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    assigned_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_by = db.relationship('User', backref='assigned_tasks')

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    role_applied = db.Column(db.String(100))
    experience = db.Column(db.Float)
    source = db.Column(db.String(50))
    status = db.Column(db.String(50))
    resume_path = db.Column(db.String(500))
    resume_link = db.Column(db.String(500))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

class Job_Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    job_title = db.Column(db.String(100), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    scheduled_date = db.Column(db.DateTime)
    interviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(50))
    feedback = db.Column(db.Text)
    rating = db.Column(db.Integer)

class SocialMediaCampaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    budget = db.Column(db.Float, default=0.0)
    amount_spent = db.Column(db.Float, default=0.0)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ScheduledPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    platforms = db.Column(db.String(200))
    scheduled_time = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    campaign_id = db.Column(db.Integer, db.ForeignKey('social_media_campaign.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, default=0.0)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    expenses = db.relationship('Expense', backref='department', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(100))
    receipt_path = db.Column(db.String(500))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    status = db.Column(db.String(50), default='active')
    assigned_to = db.Column(db.Integer, db.ForeignKey('employee.id'))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_contact = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    feedback = db.relationship('ClientFeedback', backref='client', lazy=True)

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    source = db.Column(db.String(50))
    status = db.Column(db.String(50), default='new')
    assigned_to = db.Column(db.Integer, db.ForeignKey('employee.id'))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_contact = db.Column(db.DateTime)
    notes = db.Column(db.Text)

class ClientFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    rating = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class EmployeeFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    feedback_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    employee = db.relationship('Employee', back_populates='received_feedback')

class EmployeeSalary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    base_salary = db.Column(db.Float, nullable=False)
    bonus = db.Column(db.Float, default=0.0)
    deductions = db.Column(db.Float, default=0.0)
    net_salary = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='pending')

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    document_type = db.Column(db.String(50))
    file_path = db.Column(db.String(500))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
