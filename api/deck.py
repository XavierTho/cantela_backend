from flask import Blueprint, request, jsonify
from model.deck import Deck
from model.flashcard import Flashcard
from __init__ import db
from api.jwt_authorize import token_required


deck_api = Blueprint('deck_api', __name__, url_prefix='/api/deck')

@deck_api.route('', methods=['POST'])
@token_required()
def create_deck():
    data = request.json
    title = data.get('title')
    user_id = data.get('user_id')
    cards = data.get('cards', [])  # List of flashcards

    if not title or not user_id:
        return jsonify({"error": "Deck title and user ID are required."}), 400

    # Create the deck
    deck = Deck(title=title, user_id=user_id)
    deck.create()

    # Add flashcards to the deck
    for card in cards:
        flashcard = Flashcard(
            title=card['question'],
            content=card['answer'],
            user_id=user_id,
            deck_id=deck.id
        )
        flashcard.create()

    return jsonify(deck.read()), 201

@deck_api.route('/<int:deck_id>', methods=['GET'])
def get_deck(deck_id):
    deck = Deck.query.get(deck_id)
    if not deck:
        return jsonify({"error": "Deck not found."}), 404

    flashcards = Flashcard.query.filter_by(_deck_id=deck.id).all()
    deck_data = deck.read()
    deck_data['cards'] = [card.read() for card in flashcards]
    return jsonify(deck_data), 200

@deck_api.route('', methods=['GET'])
@token_required()
def get_all_decks():
    decks = Deck.query.all()
    return jsonify([deck.read() for deck in decks]), 200  # Ensure `read()` includes `id`


@deck_api.route('/deck/<int:deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
    try:
        # Fetch the deck by ID
        deck = Deck.query.get(deck_id)
        if not deck:
            return jsonify({"error": "Deck not found"}), 404

        # Delete associated flashcards
        Flashcard.query.filter_by(_deck_id=deck_id).delete()

        # Delete the deck itself
        db.session.delete(deck)
        db.session.commit()

        return jsonify({"message": "Deck deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error while deleting deck: {e}")
        return jsonify({"error": str(e)}), 500