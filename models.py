from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import enum
import json
from flask import url_for
from sqlalchemy import Enum as SQLEnum


db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    course = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Event Types Enum
class EventType(enum.Enum):
    Seminar = 'Seminar'
    Webinar = 'Webinar'
    Workshop = 'Workshop'
    Conference = 'Conference'
    Lecture = 'Lecture'
    Training = 'Training'   
    Competition = 'Competition'
    Hackathon = 'Hackathon'

# Updated Event Model with Logo and Signature

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    event_type = db.Column(SQLEnum(EventType), nullable=False, default=EventType.Workshop)
    organizer = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)  # Keep for compatibility if needed
    location = db.Column(db.String(200), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # New date range fields
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Image fields
    logo_path = db.Column(db.String(255), nullable=True)
    signature_path = db.Column(db.String(255), nullable=True)
    background_path = db.Column(db.String(255), nullable=True)

    created_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def get_logo_url(self):
        if self.logo_path:
            return url_for('uploaded_file', filename=self.logo_path)
        return None

    def get_signature_url(self):
        if self.signature_path:
            return url_for('uploaded_file', filename=self.signature_path)
        return None

    def duration_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 1

    @property
    def is_multi_day(self):
        return self.start_date != self.end_date if self.start_date and self.end_date else False

    @property
    def status(self):
        today = date.today()
        if self.end_date < today:
            return "completed"
        elif self.start_date <= today <= self.end_date:
            return "ongoing"
        else:
            return "upcoming"

    @property
    def date_range_display(self):
        if self.start_date == self.end_date:
            return self.start_date.strftime('%Y-%m-%d')
        else:
            return f"{self.start_date.strftime('%Y-%m-%d')} → {self.end_date.strftime('%Y-%m-%d')}"

    def __repr__(self):
        return f'<Event {self.title}>'

class EventParticipant(db.Model):
    __tablename__ = 'event_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    participation_type = db.Column(db.String(50), default='Participant')
    achievement_level = db.Column(db.String(20))
    special_recognition = db.Column(db.Text)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', backref='event_participations')
    event = db.relationship('Event', backref='participants')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('event_id', 'student_id', name='unique_event_student'),)

class CertificateTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    template_type = db.Column(db.String(20), default='predefined')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_active = db.Column(db.Boolean, default=True)
    config = db.Column(db.Text)
    background_image = db.Column(db.String(300))
    logo_image = db.Column(db.String(300))
    signature_image = db.Column(db.String(300)) 
    
    # Relationship
    creator = db.relationship('User', backref='certificate_templates')
    
    @property
    def template_config(self):
        """Get template configuration as dictionary"""
        if self.config:
            try:
                return json.loads(self.config)
            except:
                return {}
        return {}
    
    @template_config.setter
    def template_config(self, config_dict):
        """Set template configuration from dictionary"""
        self.config = json.dumps(config_dict)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('certificate_template.id'))
    certificate_path = db.Column(db.String(300))
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', backref='certificates')
    event = db.relationship('Event', backref='certificates')
    template = db.relationship('CertificateTemplate', backref='certificates')
