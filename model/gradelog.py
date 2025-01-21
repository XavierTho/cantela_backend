from sqlalchemy.exc import IntegrityError
from __init__ import app, db
from model.user import User

class GradeLog(db.Model):
    """
    GradeLog Model
    
    Attributes:
        id (int): Primary key for the grade log.
        user_id (int): ID of the user who owns this grade log.
        subject (str): Subject for which the grade is recorded.
        grade (float): Grade received for the subject.
        notes (str): Additional notes about the grade.
        date (datetime): Date when the grade was recorded.
    """
    __tablename__ = 'grade_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, user_id, subject, grade, notes=''):
        self.user_id = user_id
        self.subject = subject
        self.grade = grade
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
            "grade": self.grade,
            "notes": self.notes,
            "date": self.date.strftime('%Y-%m-%d %H:%M:%S')
        }

    def update(self, data):
        for key, value in data.items():
            if key == "subject":
                self.subject = value
            if key == "grade":
                self.grade = value
            if key == "notes":
                self.notes = value
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

def initGradeLog():
    with app.app_context():
        db.create_all()  # Create all tables
        print("GradeLog table initialized.")

        # Ensure the admin user exists
        admin_user = User.query.filter_by(_uid="admin").first()
        if not admin_user:
            print("Admin user not found. Cannot initialize GradeLogs.")
            return

        # Define test grade logs
        grade_logs = [
            GradeLog(user_id=admin_user.id, subject='Math', grade=50, notes='Failed basic arithmetic'),
            GradeLog(user_id=admin_user.id, subject='Science', grade=60, notes='Failed physics exam'),
            GradeLog(user_id=admin_user.id, subject='History', grade=70, notes='Forgot details on American Civil War'),
            GradeLog(user_id=admin_user.id, subject='English', grade=80, notes='Analyzed Shakespeare'),
        ]

        # Add the test data to the database
        for log in grade_logs:
            db.session.add(log)
        db.session.commit()
        print("Grade logs table initialized with test data.")
