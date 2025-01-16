from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String, nullable=False)  # New column for name
    _classes = db.Column(db.String, nullable=False)  # Comma-separated list of class names
    _favorite_class = db.Column(db.String, nullable=True)
    _favorite_flashcard = db.Column(db.String, nullable=True)
    _grade = db.Column(db.String, nullable=True)  # High school grade (e.g., Junior, Senior)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name, classes, favorite_class, favorite_flashcard, grade, user_id):
        self._name = name
        self._classes = classes
        self._favorite_class = favorite_class
        self._favorite_flashcard = favorite_flashcard
        self._grade = grade
        self._user_id = user_id

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Profile class.
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Profile(id={self.id}, name={self._name}, classes={self._classes}, favorite_class={self._favorite_class}, favorite_flashcard={self._favorite_flashcard}, grade={self._grade}, user_id={self._user_id})"

    def create(self):
        """
        The create method adds the object to the database and commits the transaction.
        Uses:
            The db ORM methods to add and commit the transaction.
        Raises:
            Exception: An error occurred when adding the object to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        Uses:
            The User.query method to retrieve the user object.
        Returns:
            dict: A dictionary containing the profile data, including user information.
        """
        user = User.query.get(self._user_id)
        data = {
            "id": self.id,
            "name": self._name,
            "classes": self._classes.split(',') if self._classes else [],
            "favorite_class": self._favorite_class,
            "favorite_flashcard": self._favorite_flashcard,
            "grade": self._grade,
            "user_name": user.name if user else None,
        }
        return data

    def update(self):
        """
        The update method commits the transaction to the database.
        Uses:
            The db ORM method to commit the transaction.
        Raises:
            Exception: An error occurred when updating the object in the database.
        """
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """
        The delete method removes the object from the database and commits the transaction.
        Uses:
            The db ORM methods to delete and commit the transaction.
        Raises:
            Exception: An error occurred when deleting the object from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


def initProfiles():
    """
    The initProfiles function creates the Profile table and adds tester data to the table.
    Uses:
        The db ORM methods to create the table.
    Instantiates:
        Profile objects with tester data.
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        profiles_data = [
            {"name": "Thomas Edison", "classes": "AP Physics,AP Chemistry,AP Statistics", "favorite_class": "AP Physics", "favorite_flashcard": "Kinematics Equations", "grade": "Senior", "user_id": 1},
            {"name": "Grace Hopper", "classes": "AP CSP,AP Statistics,AP US History", "favorite_class": "AP CSP", "favorite_flashcard": "Binary Numbers", "grade": "Junior", "user_id": 2},
            {"name": "Nicholas Tesla", "classes": "AP Physics,AP Chemistry,AP Statistics", "favorite_class": "AP Physics", "favorite_flashcard": "Electromagnetic Theory", "grade": "Senior", "user_id": 3},
            {"name": "Xavier Thompson", "classes": "AP World History,AP US History,AP Statistics", "favorite_class": "AP World History", "favorite_flashcard": "Industrial Revolution Key Terms", "grade": "Junior", "user_id": 4},
            {"name": "Armaghan Zarak", "classes": "AP US History,AP World History,AP CSP", "favorite_class": "AP US History", "favorite_flashcard": "Constitutional Amendments", "grade": "Senior", "user_id": 5},
            {"name": "Arush Shah", "classes": "AP CSP,AP Statistics,AP Physics", "favorite_class": "AP CSP", "favorite_flashcard": "Python Functions", "grade": "Junior", "user_id": 6}
        ]

        for data in profiles_data:
            profile = Profile(
                name=data["name"],
                classes=data["classes"],
                favorite_class=data["favorite_class"],
                favorite_flashcard=data["favorite_flashcard"],
                grade=data["grade"],
                user_id=data["user_id"]
            )
            try:
                profile.create()
                print(f"Record created: {repr(profile)}")
            except IntegrityError:
                '''Fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {profile.id}")