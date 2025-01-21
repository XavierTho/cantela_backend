import jwt
from flask import Blueprint, request, jsonify, Response, g
from flask_restful import Api, Resource  # Used for REST API building
from __init__ import app  # Import the Flask app instance
from api.jwt_authorize import token_required  # Import custom decorator for token authorization
from model.leaderboard import LeaderboardEntry  # Import the LeaderboardEntry model

# Create a Blueprint for the leaderboard API
leaderboard_api = Blueprint('leaderboard_api', __name__, url_prefix='/api')

# Initialize the API object and attach it to the Blueprint
api = Api(leaderboard_api)

class LeaderboardAPI:
    """
    This class defines CRUD (Create, Read, Update, Delete) API endpoints for LeaderboardEntry.
    """

    class _CRUD(Resource):
        @token_required()  # Ensure the user is authorized
        def post(self):
            """
            Create a new leaderboard entry.
            """
            current_user = g.current_user  # Get the current user from the token
            data = request.get_json()  # Parse JSON data from the request
            if "name" not in data or "score" not in data:
                # Return a 400 error if required fields are missing
                return Response("{'message': 'Missing required fields: name or score'}", 400)

            # Create a new LeaderboardEntry object
            entry = LeaderboardEntry(name=data['name'], score=data['score'])

            try:
                entry.create()  # Save the new entry to the database
                return jsonify(entry.read()), 201  # Return the new entry's data with a 201 status
            except Exception as e:
                return jsonify({'error': str(e)}), 500  # Return a 500 error if something goes wrong

        def get(self):
            """
            Retrieve all leaderboard entries, ordered by score descending.
            """
            try:
                entries = LeaderboardEntry.query.order_by(LeaderboardEntry.score.desc()).all()
                if not entries:
                    return Response("{'message': 'No leaderboard entries found'}", 404)
                # Return the list of all entries in JSON format
                return jsonify([entry.read() for entry in entries]), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500  # Handle and return any exceptions

        @token_required()
        def put(self):
            """
            Update an existing leaderboard entry.
            """
            current_user = g.current_user  # Get the current user
            data = request.get_json()  # Parse JSON data from the request
            if "id" not in data or "name" not in data or "score" not in data:
                # Return a 400 error if required fields are missing
                return Response("{'message': 'Missing required fields: id, name, or score'}", 400)

            entry = LeaderboardEntry.query.get(data['id'])  # Find the entry by ID
            if not entry:
                return Response("{'message': 'Leaderboard entry not found'}", 404)

            # Update the entry's fields
            entry.name = data['name']
            entry.score = data['score']

            try:
                entry.update()  # Save the updated entry to the database
                return jsonify(entry.read()), 200  # Return the updated entry's data
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @token_required()
        def delete(self):
            """
            Delete a leaderboard entry.
            """
            current_user = g.current_user  # Get the current user
            data = request.get_json()  # Parse JSON data from the request
            if "id" not in data:
                # Return a 400 error if the ID field is missing
                return Response("{'message': 'Missing required field: id'}", 400)

            entry = LeaderboardEntry.query.get(data['id'])  # Find the entry by ID
            if not entry:
                return Response("{'message': 'Leaderboard entry not found'}", 404)

            try:
                entry.delete()  # Delete the entry from the database
                return jsonify({"message": "Leaderboard entry deleted"}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    # Map the _CRUD class to the /leaderboard API endpoint
    api.add_resource(_CRUD, '/leaderboard')



def initLeaderboard():
    """
    Initialize the Leaderboard database table and add default data.
    """
    with app.app_context():
        from __init__ import db  # Ensure you import the database instance here
        db.create_all()  # Create all tables if they do not exist
        print("Leaderboard table initialized.")

        # Check if the table already has data to prevent duplication
        if LeaderboardEntry.query.first() is None:
            default_entries = [
                {'name': 'Alice', 'score': 95},
                {'name': 'Bob', 'score': 87},
                {'name': 'Charlie', 'score': 78}
            ]
            for entry_data in default_entries:
                entry = LeaderboardEntry(name=entry_data['name'], score=entry_data['score'])
                db.session.add(entry)  # Add entry to the session
            db.session.commit()  # Commit all entries to the database
            print("Default leaderboard entries added.")
        else:
            print("Leaderboard table already initialized with data.")
