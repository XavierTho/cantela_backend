import logging
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
            if log_data.get('id') in [1, 2, 3]:
                logging.info(f"Skipping log with id {log_data['id']}")
                continue  # Skip entries with IDs 1, 2, and 3

            log_data.pop('id', None)  # Remove 'id' to allow database to auto-generate it
            date_str = log_data.get("date")
            if date_str:
                try:
                    log_data["date"] = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    logging.warning(f"Invalid date format for '{date_str}'. Skipping log.")
                    continue  # Skip invalid entries

            # Ensure required fields exist
            required_fields = ["user_id", "subject", "hours_studied"]
            if not all(field in log_data and log_data[field] for field in required_fields):
                logging.warning(f"Missing required fields in log data: {log_data}. Skipping log.")
                continue

            # Create a new StudyLog entry
            try:
                new_studylog = StudyLog(**log_data)
                db.session.add(new_studylog)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                logging.warning(f"IntegrityError: Could not restore log due to {str(e)}.")
            except Exception as e:
                db.session.rollback()
                logging.warning(f"Error restoring log: {str(e)}.")

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
                db.session.rollback()
                logging.warning(f"IntegrityError: Could not add studylog with subject '{studylog.subject}' due to missing user_id.")