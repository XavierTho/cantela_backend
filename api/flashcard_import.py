import requests
from flask import Blueprint, jsonify
from model.flashcard import Flashcard
from __init__ import db

flashcard_import_api = Blueprint('flashcard_import_api', __name__, url_prefix='/api')

@flashcard_import_api.route('/import-flashcards', methods=['GET'])
def import_flashcards():
    """
    Import questions and answers from an external API and save them as flashcards.
    """
    try:
        # Fetch data from an external API (e.g., Open Trivia Database)
        response = requests.get("https://opentdb.com/api.php?amount=10&difficulty=medium&type=multiple")
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from external API"}), 500

        trivia_data = response.json()
        results = trivia_data.get("results", [])

        flashcards = []
        for item in results:
            question = item.get("question")
            answer = item.get("correct_answer")
            if question and answer:
                # Create and store a flashcard in the database
                flashcard = Flashcard(title=question, content=answer, user_id=1)  # Replace user_id as needed
                db.session.add(flashcard)
                flashcards.append(flashcard.read())

        db.session.commit()
        return jsonify({
            "message": f"{len(flashcards)} flashcards imported successfully!",
            "flashcards": flashcards
        }), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500
