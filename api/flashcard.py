from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.flashcard import Flashcard

flashcard_api = Blueprint('flashcard_api', __name__, url_prefix='/api')
api = Api(flashcard_api)

class FlashcardAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new flashcard."""
            current_user = g.current_user
            data = request.get_json()

            # Check for required fields
            if not data or 'title' not in data or 'content' not in data or 'deck_id' not in data:
                return {'message': 'Title, content, and deck_id are required'}, 400

            # Validate deck_id
            deck_id = data['deck_id']
            if not deck_id:
                return {'message': 'Invalid deck_id provided'}, 400

            # Create the flashcard
            flashcard = Flashcard(data['title'], data['content'], current_user.id, deck_id)
            flashcard = flashcard.create()

            if not flashcard:
                return {'message': 'Failed to create flashcard'}, 400

            return jsonify(flashcard.read())

        @token_required()
        def get(self):
            """Get all flashcards for the current user."""
            current_user = g.current_user
            flashcards = Flashcard.query.filter_by(_user_id=current_user.id).all()
            return jsonify([flashcard.read() for flashcard in flashcards])

        @token_required()
        def put(self):
            """Update an existing flashcard."""
            data = request.get_json()
            if not data or 'id' not in data:
                return {'message': 'Flashcard ID is required'}, 400
            flashcard = Flashcard.query.get(data['id'])
            if not flashcard or flashcard._user_id != g.current_user.id:
                return {'message': 'Flashcard not found or unauthorized'}, 404
            flashcard.update(data)
            return jsonify(flashcard.read())

        @token_required()
        def delete(self):
            """Delete a flashcard."""
            data = request.get_json()
            if not data or 'id' not in data:
                return {'message': 'Flashcard ID is required'}, 400
            flashcard = Flashcard.query.get(data['id'])
            if not flashcard or flashcard._user_id != g.current_user.id:
                return {'message': 'Flashcard not found or unauthorized'}, 404
            flashcard.delete()
            return {'message': 'Flashcard deleted'}, 200

api.add_resource(FlashcardAPI._CRUD, '/flashcard')
