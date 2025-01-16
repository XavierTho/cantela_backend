from flask import current_app
from sqlalchemy.exc import IntegrityError
from __init__ import app, db

class Profile(db.Model):
    """
    Profile Model

    This class represents the Profile model, which is used to manage actions in the 'profiles' table of the database.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database.
        id (Column): The primary key, an integer representing the unique identifier for the profile.
        name (Column): A string representing the profile's name, not unique and cannot be null.
        classes (Column): A string representing the classes the user is enrolled in.
        favorite_class (Column): A string representing the user's favorite class.
        grade (Column): A string representing the user's grade.
    """
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    classes = db.Column(db.String(255), unique=False, nullable=False)
    favorite_class = db.Column(db.String(255), unique=False, nullable=False)
    grade = db.Column(db.String(10), unique=False, nullable=False)

    def __init__(self, name, classes, favorite_class, grade):
        """
        Constructor for Profile.
        
        Args:
            name (str): The name of the profile owner.
            classes (str): The list of classes as a single string.
            favorite_class (str): The favorite class of the user.
            grade (str): The grade of the user.
        """
        self.name = name
        self.classes = classes
        self.favorite_class = favorite_class
        self.grade = grade

    def create(self):
        """
        Adds a new profile to the database.
        
        Returns:
            Profile: The created profile object, or None if there was an error.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        """
        Converts the profile object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the profile object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "classes": self.classes,
            "favorite_class": self.favorite_class,
            "grade": self.grade
        }

    def update(self, updates):
        """
        Updates the profile with new data.
        
        Args:
            updates (dict): A dictionary containing the new data for the profile.
        
        Returns:
            Profile: The updated profile object, or None if there was an error.
        """
        if not isinstance(updates, dict):
            return self

        self.name = updates.get("name", self.name)
        self.classes = updates.get("classes", self.classes)
        self.favorite_class = updates.get("favorite_class", self.favorite_class)
        self.grade = updates.get("grade", self.grade)

        try:
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def delete(self):
        """
        Deletes the profile from the database.
        
        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def initProfiles():
    """
    The initProfiles function creates the profiles table and adds test data.
    """
    with app.app_context():
        db.create_all()
        profiles = [
            Profile(name="Armaghan Zarak", classes="Math, Science, History", favorite_class="Science", grade="A"),
            Profile(name="Arush Shah", classes="Art, PE, English", favorite_class="Art", grade="B"),
            Profile(name="Jackson Patrick", classes="Computer Science, Math, Music", favorite_class="Computer Science", grade="A+")
        ]

        for profile in profiles:
            try:
                profile.create()
            except IntegrityError:
                db.session.rollback()
