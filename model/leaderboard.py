from flask import Blueprint, request, jsonify, Response, g
from flask_restful import Api, Resource
from __init__ import db, app  # Import `app` for context management
from api.jwt_authorize import token_required

# Blueprint for Leaderboard API
leaderboard_api = Blueprint('leaderboard_api', __name__, url_prefix='/api')

# Flask-RESTful API object
api = Api(leaderboard_api)

# LeaderboardEntry Model
class LeaderboardEntry(db.Model):
    __tablename__ = 'leaderboard'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def read(self):
        return {"id": self.id, "name": self.name, "score": self.score}

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



# Initialize the Leaderboard Table
def initLeaderboard():
    """
    Initialize the leaderboard table and populate it with default data.
    """
    with app.app_context():  # Use Flask app context
        db.create_all()  # Create all tables
        print("Leaderboard table initialized.")

        # Add default data if the table is empty
        if LeaderboardEntry.query.first() is None:
            default_entries = [
                {"name": "Alice", "score": 150},
                {"name": "Bob", "score": 120},
                {"name": "Charlie", "score": 180},
            ]
            for entry in default_entries:
                new_entry = LeaderboardEntry(name=entry['name'], score=entry['score'])
                db.session.add(new_entry)
            try:
                db.session.commit()
                print("Default leaderboard entries added.")
            except Exception as e:
                db.session.rollback()
                print(f"Error initializing leaderboard data: {e}")
        else:
            print("Leaderboard table already contains data.")



# Leaderboard API Class
class LeaderboardAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new leaderboard entry.
            """
            # Obtain data from the request
            data = request.get_json()
            if "name" not in data or "score" not in data:
                return Response("{'message': 'Missing required fields: name or score'}", status=400)

            # Create a new entry
            entry = LeaderboardEntry(name=data['name'], score=data['score'])

            # Save to the database
            try:
                entry.create()
                return jsonify(entry.read()), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        def get(self):
            """
            Retrieve all leaderboard entries, ordered by score descending.
            """
            try:
                entries = LeaderboardEntry.query.order_by(LeaderboardEntry.score.desc()).all()
                if not entries:
                    return Response("{'message': 'No leaderboard entries found'}", status=404)
                return jsonify([entry.read() for entry in entries]), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @token_required()
        def put(self):
            """
            Update an existing leaderboard entry.
            """
            # Obtain data from the request
            data = request.get_json()
            if "id" not in data or "name" not in data or "score" not in data:
                return Response("{'message': 'Missing required fields: id, name, or score'}", status=400)

            # Find the leaderboard entry
            entry = LeaderboardEntry.query.get(data['id'])
            if not entry:
                return Response("{'message': 'Leaderboard entry not found'}", status=404)

            # Update the entry
            entry.name = data['name']
            entry.score = data['score']

            # Save updates
            try:
                entry.update()
                return jsonify(entry.read()), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @token_required()
        def delete(self):
            """
            Delete a leaderboard entry.
            """
            # Obtain data from the request
            data = request.get_json()
            if "id" not in data:
                return Response("{'message': 'Missing required field: id'}", status=400)

            # Find the leaderboard entry
            entry = LeaderboardEntry.query.get(data['id'])
            if not entry:
                return Response("{'message': 'Leaderboard entry not found'}", status=404)

            # Delete the entry
            try:
                entry.delete()
                return jsonify({"message": "Leaderboard entry deleted"}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    # Add Resource Endpoints
    api.add_resource(_CRUD, '/leaderboard')  # /api/leaderboard

# Register the Blueprint
app.register_blueprint(leaderboard_api)
