# studylog.py
import logging
from sqlalchemy import Text, JSON, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from __init__ import app, db
from model.user import User
from model.channel import Channel

class StudyLog(db.Model):
    """
    StudyLog Model
    
    The StudyLog class represents an individual study log entry.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the studylog.
        user_id (db.Column): An integer representing the user who created the studylog.
        subject (db.Column): A string representing the subject of the studylog.
        hours_studied (db.Column): A float representing the hours studied.
        notes (db.Column): A string representing the notes of the studylog.
        time (db.Column): A datetime representing the time of the studylog.
    """
    __tablename__ = 'studylog'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    hours_studied = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, user_id, subject, hours_studied, notes=''):
        """
        Constructor, 1st step in object creation.
        
        Args:
            user_id (int): The ID of the user who created the studylog.
            subject (str): The subject of the studylog.
            hours_studied (float): The hours studied.
            notes (str, optional): The notes of the studylog. Defaults to None.
            time (datetime, optional): The time of the studylog. Defaults to current time.
        """
        self.user_id = user_id
        self.subject = subject
        self.hours_studied = hours_studied
        self.notes = notes

    def create(self):
        """
        Creates a new studylog in the database.
        
        Returns:
            StudyLog: The created studylog object, or None on error.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "subject": self.subject,
            "hours_studied": self.hours_studied,
            "notes": self.notes,
            "date": self.date.strftime('%Y-%m-%d %H:%M:%S')
        }

    def update(self, data):
        for key, value in data.items():
            if key == "subject":
                self.subject = value
            if key == "hours_studied":
                self.hours_studied = value
            if key == "notes":
                self.notes = value
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

def initStudyLog():
    """
    The initStudyLog function creates the StudyLog table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        StudyLog objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """        
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        studylogs = [
            StudyLog(user_id=5, subject='Math', hours_studied=2.5, notes='Reviewed algebra and geometry.'),
            StudyLog(user_id=5, subject='Science', hours_studied=1.5, notes='Studied physics and chemistry.'),
            StudyLog(user_id=5, subject='History', hours_studied=3.0, notes='Read about World War II.'),
        ]
        
        for studylog in studylogs:
            try:
                studylog.create()
            except IntegrityError:
                db.session.rollback()
                logging.warning(f"IntegrityError: Could not add studylog with subject '{studylog.subject}' due to missing user_id.")