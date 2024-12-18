from sqlalchemy.exc import IntegrityError
from __init__ import app, db
from model.user import User

class StudyLog(db.Model):
    """
    StudyLog Model
    
    Attributes:
        id (int): Primary key for the study log.
        user_id (int): ID of the user who owns this study log.
        subject (str): Subject of the study session.
        hours_studied (float): Number of hours studied.
        notes (str): Additional notes for the study session.
        date (datetime): Date of the study session.
    """
    __tablename__ = 'study_logs'


    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    hours_studied = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, user_id, subject, hours_studied, notes=''):
        self.user_id = user_id
        self.subject = subject
        self.hours_studied = hours_studied
        self.notes = notes

    def create(self):
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
    with app.app_context():
        db.create_all()
        print("StudyLogs table initialized.")