from sqlalchemy.exc import IntegrityError
from __init__ import app, db
from model.deck import Deck
from model.user import User

class Flashcard(db.Model):
    """
    Flashcard Model
    
    Attributes:
        id (int): Primary key for the flashcard.
        title (str): Title of the flashcard.
        content (str): Content of the flashcard.
        user_id (int): ID of the user who owns this flashcard.
        deck_id (int): ID of the deck to which this flashcard belongs.
    """
    __tablename__ = 'flashcards'

    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _content = db.Column(db.String(255), nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _deck_id = db.Column(db.Integer, db.ForeignKey('decks.id'), nullable=True)  

    def __init__(self, title, content, user_id, deck_id=None):
        self._title = title
        self._content = content
        self._user_id = user_id
        self._deck_id = deck_id

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            print(f"Flashcard Created: {self._title}, {self._content}")
            return self
        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError while creating flashcard: {e}")
            return None
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error while creating flashcard: {e}")
            return None





    def read(self):
        return {
            "id": self.id,
            "title": self._title,
            "content": self._content,
            "user_id": self._user_id,
            "deck_id": self._deck_id
        }

    def update(self, data):
        for key, value in data.items():
            if key == "title":
                self._title = value
            if key == "content":
                self._content = value
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

def initFlashcards():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()  # This will create all tables
        print("Flashcards table initialized.")

        # Add test data if the tables are empty
        if Flashcard.query.count() == 0:
            user = User.query.first()  # Assuming at least one user exists
            if not user:
                user = User(username='testuser', password='password123')  # Create a test user if not exists
                db.session.add(user)
                db.session.commit()

            # Example: Create some decks
            deck = Deck(title='Math Flashcards', user_id=user.id)  # Provide user_id here
            db.session.add(deck)
            db.session.commit()

            # Add some flashcards with test data
            flashcards_data = [
                {"title": "What is 2+2?", "content": "4", "user_id": user.id, "deck_id": deck.id},
                {"title": "What is 5+3?", "content": "8", "user_id": user.id, "deck_id": deck.id},
                {"title": "What is 10-6?", "content": "4", "user_id": user.id, "deck_id": deck.id}
            ]

            for card_data in flashcards_data:
                flashcard = Flashcard(**card_data)
                db.session.add(flashcard)

            db.session.commit()
            print("Test data added to Flashcards.")
        else:
            print("Flashcards already exist.")
