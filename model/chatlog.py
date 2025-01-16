from sqlalchemy.exc import IntegrityError
from __init__ import app, db

class Chatlog(db.Model):
    """
    Flashcard Model
    
    Attributes:
        id (int): Primary key for the flashcard.
        title (str): Title of the flashcard.
        content (str): Content of the flashcard.
        user_id (int): ID of the user who owns this flashcard.
    """
    __tablename__ = 'chatlog'

    id = db.Column(db.Integer, primary_key=True)
    _prompt = db.Column(db.String(255), nullable=False)
    _response = db.Column(db.String(255), nullable=False)

    def __init__(self, prompt, response):
        self._prompt = prompt
        self._response = response
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self
    

    def read(self):
        return {
            "prompt": self._prompt,
            "response": self._response,
        }

    def update(self, data):
        for key, value in data.items():
            if key == "prompt":
                self._prompt = value
            if key == "response":
                self._response = value
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

def initChatlog():
    msg = Chatlog(prompt="What is the capital of China?", response="Beijing")
    msg.create()
    with app.app_context():
        db.create_all()  # This will create all tables
        print("Flashcards table initialized.")



