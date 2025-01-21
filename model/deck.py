from __init__ import db
from flask import current_app

class Deck(db.Model):
    """
    Deck Model

    Attributes:
        id (int): Primary key for the deck.
        title (str): Title of the deck.
        user_id (int): ID of the user who owns this deck.
    """
    __tablename__ = 'decks'

    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Constructor
    def __init__(self, title, user_id):
        self._title = title
        self._user_id = user_id

    # Property for title
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    # Property for user_id
    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    # Create method
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    # Read method
    def read(self):
        return {
            "id": self.id,
            "title": self.title,  # Access via property
            "user_id": self.user_id,  # Access via property
        }

    # Delete method
    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Initialization function
def initDecks():
    with current_app.app_context():
        db.create_all()
        print("Decks table initialized.")
