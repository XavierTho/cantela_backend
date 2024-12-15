from flask import Flask, jsonify, request
from flask_cors import CORS
import random

# Initialize Flask application
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')

# ------------------------------
# USER DATA API
# ------------------------------
@app.route('/api/data')
def get_data():
    InfoDb = [
        {"FirstName": "Zafeer", "LastName": "Ahmed", "DOB": "January 11", "Residence": "San Diego", "Email": "zafeer10ahmed@gmail.com", "Owns_Cars": ["Tesla Model 3"]},
        {"FirstName": "Arush", "LastName": "Shah", "DOB": "December 20", "Residence": "San Diego", "Email": "emailarushshah@gmail.com", "Owns_Cars": ["Tesla Model 3"]},
        {"FirstName": "Nolan", "LastName": "Yu", "DOB": "October 7", "Residence": "San Diego", "Email": "nolanyu2@gmail.com", "Owns_Cars": ["Mazda"]},
        {"FirstName": "Xavier", "LastName": "Thompson", "DOB": "January 23", "Residence": "San Diego", "Email": "xavierathompson@gmail.com", "Favorite_Foods": "Popcorn"},
        {"FirstName": "Armaghan", "LastName": "Zarak", "DOB": "October 21", "Residence": "San Diego", "Email": "Armaghanz@icloud.com", "Owns_Vehicles": ["2015-scooter", "Half-a-bike", "2013-Honda-Pilot", "The-other-half-of-the-bike"]}
    ]
    return jsonify(InfoDb)

# ------------------------------
# HOME PAGE
# ------------------------------
@app.route('/')
def home():
    html_content = """
    <html>
    <head><title>Welcome</title></head>
    <body>
        <h1>Welcome to the Flask App</h1>
        <ul>
            <li><a href="/api/data">User Data</a></li>
            <li><a href="/api/quiz/apush">APUSH Quiz Questions</a></li>
            <li><a href="/api/leaderboard/apush">APUSH Leaderboard</a></li>
        </ul>
    </body>
    </html>
    """
    return html_content

# ------------------------------
# QUIZ HANDLING BACKEND
# ------------------------------

# Pool of 15 APUSH Questions
question_pool = [
    {"id": 1, "text": "Who was the first President of the United States?", "options": ["George Washington", "Thomas Jefferson", "John Adams", "James Madison"], "correctAnswer": "George Washington"},
    {"id": 2, "text": "What year did the American Revolutionary War end?", "options": ["1776", "1781", "1783", "1791"], "correctAnswer": "1783"},
    {"id": 3, "text": "What was the primary purpose of the Declaration of Independence?", "options": ["To declare war on Britain", "To establish a federal government", "To explain the reasons for American independence", "To create a constitution"], "correctAnswer": "To explain the reasons for American independence"},
    {"id": 4, "text": "Which battle is considered the turning point of the American Civil War?", "options": ["Battle of Antietam", "Battle of Gettysburg", "Battle of Fort Sumter", "Battle of Vicksburg"], "correctAnswer": "Battle of Gettysburg"},
    {"id": 5, "text": "Who wrote the 'Star-Spangled Banner' during the War of 1812?", "options": ["Francis Scott Key", "Thomas Paine", "Paul Revere", "John Quincy Adams"], "correctAnswer": "Francis Scott Key"},
    {"id": 6, "text": "What was the main reason for the Louisiana Purchase?", "options": ["To expand westward", "To secure navigation rights on the Mississippi River", "To establish trade with Mexico", "To claim Alaska"], "correctAnswer": "To secure navigation rights on the Mississippi River"},
    {"id": 7, "text": "Which event marked the start of the Great Depression?", "options": ["Stock Market Crash of 1929", "World War I", "Dust Bowl", "New Deal"], "correctAnswer": "Stock Market Crash of 1929"},
    {"id": 8, "text": "What was the purpose of the Emancipation Proclamation?", "options": ["To free slaves in Confederate states", "To end the Civil War", "To grant voting rights to African Americans", "To create a constitutional amendment"], "correctAnswer": "To free slaves in Confederate states"},
    {"id": 9, "text": "What was the significance of the Seneca Falls Convention of 1848?", "options": ["It launched the women's suffrage movement", "It ended slavery in the United States", "It marked the beginning of the abolitionist movement", "It established labor unions"], "correctAnswer": "It launched the women's suffrage movement"},
    {"id": 10, "text": "What was the main goal of the Marshall Plan?", "options": ["To rebuild European economies after World War II", "To contain communism in Asia", "To establish NATO", "To rebuild Japan's military"], "correctAnswer": "To rebuild European economies after World War II"},
    {"id": 11, "text": "Which Supreme Court case established judicial review?", "options": ["Marbury v. Madison", "McCulloch v. Maryland", "Dred Scott v. Sandford", "Brown v. Board of Education"], "correctAnswer": "Marbury v. Madison"},
    {"id": 12, "text": "What was the main cause of the Mexican-American War?", "options": ["Border disputes over Texas", "Annexation of California", "Desire to acquire New Mexico", "Clash over Oregon territory"], "correctAnswer": "Border disputes over Texas"},
    {"id": 13, "text": "Which amendment abolished slavery in the United States?", "options": ["13th Amendment", "14th Amendment", "15th Amendment", "19th Amendment"], "correctAnswer": "13th Amendment"},
    {"id": 14, "text": "What was the primary purpose of the Monroe Doctrine?", "options": ["To prevent European colonization in the Americas", "To establish trade agreements with Europe", "To create alliances in Asia", "To defend against Native American attacks"], "correctAnswer": "To prevent European colonization in the Americas"},
    {"id": 15, "text": "Which territory was acquired as a result of the Spanish-American War?", "options": ["Puerto Rico", "Hawaii", "Alaska", "Texas"], "correctAnswer": "Puerto Rico"}
]

# Leaderboard data (in-memory for now)
leaderboard = []

@app.route('/api/quiz/apush', methods=['GET'])
def get_questions():
    selected_questions = random.sample(question_pool, 10)
    sanitized_questions = [{key: value for key, value in q.items() if key != "correctAnswer"} for q in selected_questions]
    return jsonify(sanitized_questions), 200

@app.route('/api/quiz/apush/submit', methods=['POST'])
def submit_quiz():
    data = request.json
    answers = data.get('answers', [])
    user_name = data.get('name', 'Anonymous')

    score = 0
    for answer in answers:
        question = next((q for q in question_pool if q["id"] == answer["questionId"]), None)
        if question and question["correctAnswer"] == answer["answer"]:
            score += 1

    leaderboard.append({"name": user_name, "score": score})
    return jsonify({"name": user_name, "score": score}), 200

@app.route('/api/leaderboard/apush', methods=['GET'])
def get_leaderboard():
    sorted_leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    return jsonify(sorted_leaderboard), 200

# Run Server
if __name__ == '__main__':
    app.run(port=5003)
