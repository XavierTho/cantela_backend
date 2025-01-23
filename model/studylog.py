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

    def __init__(self, user_id, subject, hours_studied, notes='', date=None):
        self.user_id = user_id
        self.subject = subject
        self.hours_studied = hours_studied
        self.notes = notes
        if date:
            self.date = date

    def __repr__(self):
        return f"StudyLog(id={self.id}, user_id={self.user_id}, subject={self.subject}, hours_studied={self.hours_studied}, notes={self.notes})"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not create studylog with subject '{self.subject}' due to {str(e)}.")
            return None
        return self

    def read(self):
        user = User.query.get(self.user_id)
        data = {
            "id": self.id,
            "user_id": user.id if user else None,
            "subject": self.subject,
            "hours_studied": self.hours_studied,
            "notes": self.notes,
            "date": self.date.strftime('%Y-%m-%d %H:%M:%S')
        }
        return data

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def restore(data):
        for log_data in data:
            _ = log_data.pop('id', None)  # Remove 'id' from log_data
            user_id = log_data.get("user_id", None)
            subject = log_data.get("subject", None)
            date_str = log_data.get("date", None)
            if date_str:
                log_data["date"] = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            studylog = StudyLog.query.filter_by(user_id=user_id, subject=subject).first()
            if studylog:
                studylog.update(log_data)
            else:
                studylog = StudyLog(**log_data)
                studylog.create()

def initStudyLog():
    """
    The initStudyLog function creates the StudyLog table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        StudyLog objects with tester data.
    
    Raises:    import logging
    from sqlalchemy.exc import IntegrityError
    from datetime import datetime
    from __init__ import app, db
    from model.user import User
    
    class StudyLog(db.Model):
        __tablename__ = 'studylog'
    
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        subject = db.Column(db.String(100), nullable=False)
        hours_studied = db.Column(db.Float, nullable=False)
        notes = db.Column(db.Text)
        date = db.Column(db.DateTime, default=db.func.current_timestamp())
    
        def __init__(self, user_id, subject, hours_studied, notes='', date=None):
            self.user_id = user_id
            self.subject = subject
            self.hours_studied = hours_studied
            self.notes = notes
            if date:
                self.date = date
    
        def __repr__(self):
            return f"StudyLog(id={self.id}, user_id={self.user_id}, subject={self.subject}, hours_studied={self.hours_studied}, notes={self.notes})"
    
        def create(self):
            try:
                db.session.add(self)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                logging.warning(f"IntegrityError: Could not create studylog with subject '{self.subject}' due to {str(e)}.")
                return None
            return self
    
        def read(self):
            user = User.query.get(self.user_id)
            data = {
                "id": self.id,
                "user_id": user.id if user else None,
                "subject": self.subject,
                "hours_studied": self.hours_studied,
                "notes": self.notes,
                "date": self.date.strftime('%Y-%m-%d %H:%M:%S')
            }
            return data
    
        def update(self, data):
            for key, value in data.items():
                setattr(self, key, value)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
    
        def delete(self):
            try:
                db.session.delete(self)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
    
        @staticmethod
        def restore(data):
            for log_data in data:
                _ = log_data.pop('id', None)  # Remove 'id' from log_data
                user_id = log_data.get("user_id", None)
                subject = log_data.get("subject", None)
                date_str = log_data.get("date", None)
                if date_str:
                    log_data["date"] = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                studylog = StudyLog.query.filter_by(user_id=user_id, subject=subject).first()
                if studylog:
                    studylog.update(log_data)
                else:
                    studylog = StudyLog(**log_data)
                    studylog.create()
    
    def initStudyLog():
        with app.app_context():
            db.create_all()
            studylogs = [
                StudyLog(user_id=1, subject='Math', hours_studied=2.5, notes='Reviewed algebra and geometry.'),
                StudyLog(user_id=1, subject='Science', hours_studied=1.5, notes='Studied physics and chemistry.'),
                StudyLog(user_id=2, subject='History', hours_studied=3.0, notes='Read about World War II.'),
            ]
            
            for studylog in studylogs:
                try:
                    studylog.create()
                    print(f"Record created: {repr(studylog)}")
                except IntegrityError:
                    db.session.remove()
                    print(f"Records exist, duplicate data, or error: {studylog.subject}")
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