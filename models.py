# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'STUDENT' or 'HOD'
    student = db.relationship('Student', backref='user', uselist=False)

class Student(db.Model):
    __tablename__ = 'student'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100))
    roll = db.Column(db.String(20))
    phone = db.Column(db.String(15))
    semester = db.Column(db.String(10))
    mentor = db.Column(db.String(100))
    company = db.Column(db.String(100))
    company_guide = db.Column(db.String(100))
    project_name = db.Column(db.String(200))
    current_topic = db.Column(db.String(200))
    project_progress = db.Column(db.Integer, default=0)
    notification_seen = db.Column(db.Boolean, default=True, nullable=False)  # New field

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())