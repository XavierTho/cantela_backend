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
    {"id": 15, "text": "Which territory was acquired as a result of the Spanish-American War?", "options": ["Puerto Rico", "Hawaii", "Alaska", "Texas"], "correctAnswer": "Puerto Rico"},
    {"id": 16, "text": "Who was the President during the Louisiana Purchase?", "options": ["Thomas Jefferson", "James Madison", "John Adams", "George Washington"], "correctAnswer": "Thomas Jefferson"},
    {"id": 17, "text": "What was the primary goal of the Freedmen's Bureau?", "options": ["To help former slaves and poor whites", "To establish segregation laws", "To create northern industries", "To rebuild the southern economy"], "correctAnswer": "To help former slaves and poor whites"},
    {"id": 18, "text": "Which event led directly to the start of the American Revolution?", "options": ["Boston Tea Party", "Stamp Act", "Boston Massacre", "Intolerable Acts"], "correctAnswer": "Intolerable Acts"},
    {"id": 19, "text": "What was the significance of the Battle of Yorktown?", "options": ["It ended the Revolutionary War", "It began the Civil War", "It was a turning point in World War I", "It marked the end of the French and Indian War"], "correctAnswer": "It ended the Revolutionary War"},
    {"id": 20, "text": "Which President issued the New Deal during the Great Depression?", "options": ["Franklin D. Roosevelt", "Herbert Hoover", "Harry S. Truman", "Woodrow Wilson"], "correctAnswer": "Franklin D. Roosevelt"},
    {"id": 21, "text": "What was the goal of the Sherman Antitrust Act?", "options": ["To prevent monopolies and promote competition", "To establish labor unions", "To regulate stock markets", "To create income taxes"], "correctAnswer": "To prevent monopolies and promote competition"},
    {"id": 22, "text": "Who was the author of 'Common Sense'?", "options": ["Thomas Paine", "Benjamin Franklin", "John Locke", "Alexander Hamilton"], "correctAnswer": "Thomas Paine"},
    {"id": 23, "text": "Which treaty ended the Mexican-American War?", "options": ["Treaty of Guadalupe Hidalgo", "Treaty of Paris", "Adams-Onís Treaty", "Jay Treaty"], "correctAnswer": "Treaty of Guadalupe Hidalgo"},
    {"id": 24, "text": "Which President is associated with the Trail of Tears?", "options": ["Andrew Jackson", "Martin Van Buren", "James Monroe", "Zachary Taylor"], "correctAnswer": "Andrew Jackson"},
    {"id": 25, "text": "Which war was fought between the U.S. and Britain in the early 19th century?", "options": ["War of 1812", "Mexican-American War", "Spanish-American War", "World War I"], "correctAnswer": "War of 1812"},

    {"id": 26, "text": "Which treaty ended the Revolutionary War?", "options": ["Treaty of Paris", "Treaty of Versailles", "Jay's Treaty", "Treaty of Ghent"], "correctAnswer": "Treaty of Paris"},
    {"id": 27, "text": "Who was the leader of the Confederate Army during the Civil War?", "options": ["Robert E. Lee", "Ulysses S. Grant", "Stonewall Jackson", "Jefferson Davis"], "correctAnswer": "Robert E. Lee"},
    {"id": 28, "text": "What was the primary goal of the abolitionist movement?", "options": ["To end slavery", "To expand suffrage", "To promote industrialization", "To defend states' rights"], "correctAnswer": "To end slavery"},
    {"id": 29, "text": "What was the significance of the Homestead Act of 1862?", "options": ["It provided free land to settlers in the West", "It ended Reconstruction", "It promoted the growth of railroads", "It abolished slavery"], "correctAnswer": "It provided free land to settlers in the West"},
    {"id": 30, "text": "Which economic policy was promoted by Alexander Hamilton?", "options": ["A strong central bank", "Laissez-faire capitalism", "Agrarian-based economy", "Free trade with Britain"], "correctAnswer": "A strong central bank"},
    {"id": 31, "text": "What was the primary purpose of the Gadsden Purchase?", "options": ["To build a southern transcontinental railroad", "To annex California", "To establish Texas' borders", "To acquire Oregon"], "correctAnswer": "To build a southern transcontinental railroad"},
    {"id": 32, "text": "What was the main effect of the Compromise of 1850?", "options": ["It allowed California to enter as a free state", "It started the Civil War", "It ended Reconstruction", "It established popular sovereignty in the North"], "correctAnswer": "It allowed California to enter as a free state"},
    {"id": 33, "text": "Who was the main author of the U.S. Constitution?", "options": ["James Madison", "Alexander Hamilton", "Thomas Jefferson", "George Washington"], "correctAnswer": "James Madison"},
    {"id": 34, "text": "What was the significance of the Dred Scott v. Sandford case?", "options": ["It ruled that African Americans could not be U.S. citizens", "It ended segregation", "It granted voting rights to women", "It established judicial review"], "correctAnswer": "It ruled that African Americans could not be U.S. citizens"},
    {"id": 35, "text": "What was the main purpose of the Federalist Papers?", "options": ["To promote the ratification of the Constitution", "To establish the Bill of Rights", "To outline states' rights", "To end the Revolutionary War"], "correctAnswer": "To promote the ratification of the Constitution"},
    {"id": 36, "text": "What did the Kansas-Nebraska Act of 1854 do?", "options": ["Allowed popular sovereignty to decide slavery", "Ended slavery in the U.S.", "Granted voting rights to women", "Created new railroads"], "correctAnswer": "Allowed popular sovereignty to decide slavery"},
    {"id": 37, "text": "What was the primary reason for the War of 1812?", "options": ["British impressment of American sailors", "U.S. expansion into Mexico", "Conflict over the Louisiana Purchase", "Spanish interference in trade"], "correctAnswer": "British impressment of American sailors"},
    {"id": 38, "text": "Who were the main laborers on the Transcontinental Railroad?", "options": ["Chinese and Irish immigrants", "Slaves and Native Americans", "Freedmen and women", "Mexicans and Canadians"], "correctAnswer": "Chinese and Irish immigrants"},
    {"id": 39, "text": "Which event is associated with the start of the women's suffrage movement?", "options": ["Seneca Falls Convention", "Montgomery Bus Boycott", "The New Deal", "The Great Migration"], "correctAnswer": "Seneca Falls Convention"},
    {"id": 40, "text": "What was the purpose of the Proclamation of 1763?", "options": ["To limit colonial expansion west of the Appalachians", "To establish new taxes on tea", "To create a trade alliance with Spain", "To declare war on France"], "correctAnswer": "To limit colonial expansion west of the Appalachians"},
    {"id": 41, "text": "What did the 19th Amendment achieve?", "options": ["Granted women the right to vote", "Abolished slavery", "Limited presidential terms", "Guaranteed freedom of speech"], "correctAnswer": "Granted women the right to vote"},
    {"id": 42, "text": "Which President is known for the Square Deal?", "options": ["Theodore Roosevelt", "Franklin D. Roosevelt", "Woodrow Wilson", "William Taft"], "correctAnswer": "Theodore Roosevelt"},
    {"id": 43, "text": "What was the goal of the Civilian Conservation Corps (CCC)?", "options": ["To create jobs during the Great Depression", "To end slavery", "To promote women's suffrage", "To build the Transcontinental Railroad"], "correctAnswer": "To create jobs during the Great Depression"},
    {"id": 44, "text": "Which treaty ended World War I?", "options": ["Treaty of Versailles", "Treaty of Paris", "Treaty of Ghent", "Treaty of Guadalupe Hidalgo"], "correctAnswer": "Treaty of Versailles"},
    {"id": 45, "text": "What was the purpose of the Fugitive Slave Act?", "options": ["To require the return of escaped slaves to their owners", "To abolish slavery in the North", "To create abolitionist societies", "To protect freed slaves in the South"], "correctAnswer": "To require the return of escaped slaves to their owners"},
    {"id": 46, "text": "What was the primary goal of the Lewis and Clark Expedition?", "options": ["To explore the Louisiana Territory", "To establish settlements in Oregon", "To expand the railroad system", "To negotiate with Native American tribes"], "correctAnswer": "To explore the Louisiana Territory"},
    {"id": 47, "text": "Who was the President during the Cuban Missile Crisis?", "options": ["John F. Kennedy", "Dwight D. Eisenhower", "Lyndon B. Johnson", "Richard Nixon"], "correctAnswer": "John F. Kennedy"},
    {"id": 48, "text": "What was the main reason for the Salem Witch Trials?", "options": ["Religious hysteria and social tensions", "A Native American uprising", "Political corruption", "A lack of education"], "correctAnswer": "Religious hysteria and social tensions"},
    {"id": 49, "text": "What was the purpose of the Social Security Act of 1935?", "options": ["To provide financial assistance to the elderly and unemployed", "To regulate labor unions", "To fund public education", "To establish a minimum wage"], "correctAnswer": "To provide financial assistance to the elderly and unemployed"},
    {"id": 50, "text": "Which amendment gave African American men the right to vote?", "options": ["15th Amendment", "13th Amendment", "14th Amendment", "19th Amendment"], "correctAnswer": "15th Amendment"}
]

    # Add 25 more questions (following the same format).

# Leaderboard data (in-memory for now)
leaderboard = []

@app.route('/api/quiz/apush', methods=['GET'])
def get_questions():
    selected_questions = random.sample(question_pool, 10)  #number of random questions taken from pool . 
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
