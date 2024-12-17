from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

# ========================
# Class Schedule
# ========================
schedule = [
    {"Period": 1, "Class": "Honors Medical Intervention", "Start": "08:35", "End": "09:41"},
    {"Period": 2, "Class": "AP CSP", "Start": "09:46", "End": "10:55"},
    {"Period": 3, "Class": "AFA 2", "Start": "11:37", "End": "12:43"},
    {"Period": 4, "Class": "APUSH", "Start": "13:18", "End": "14:24"},
    {"Period": 5, "Class": "AmLit", "Start": "14:29", "End": "15:35"}
]

# ========================
# Helper Functions
# ========================
def get_next_school_day_start():
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    next_school_start = datetime.combine(tomorrow, datetime.strptime("08:35", "%H:%M").time())
    return next_school_start - today

# ========================
# Class Schedule Countdown
# ========================
@app.route('/html/schedule', methods=['GET'])
def render_schedule_html():
    now = datetime.now().time()
    current_period = None
    next_period = None

    for period in schedule:
        start = datetime.strptime(period["Start"], "%H:%M").time()
        end = datetime.strptime(period["End"], "%H:%M").time()
        if start <= now <= end:
            current_period = period
        elif now < start and not next_period:
            next_period = period

    next_day_time = get_next_school_day_start()
    template = """
    <html>
    <head>
        <title>Class Schedule Countdown</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background: linear-gradient(to bottom, #FFF5E1, #FFDAB9);
                animation: fadeIn 2s;
            }
            h1 { font-size: 36px; color: #FF4500; }
            h2 { font-size: 24px; color: #2F4F4F; }
            .celebration {
                color: #FF4500;
                font-size: 24px;
                font-weight: bold;
                margin-top: 20px;
                animation: pulse 1s infinite alternate;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes pulse {
                from { transform: scale(1); }
                to { transform: scale(1.1); }
            }
        </style>
    </head>
    <body>
        <h1>Class Schedule Countdown</h1>
        {% if current_period %}
        <h2>Current Period: {{ current_period["Class"] }}</h2>
        <p>Class ends at: {{ current_period["End"] }}</p>
        {% elif next_period %}
        <h2>Next Period: {{ next_period["Class"] }}</h2>
        <p>Starts at: {{ next_period["Start"] }}</p>
        {% else %}
        <h2 class="celebration">You're done for the day! 🎉</h2>
        <p>Next school day starts in: {{ next_day_time }}</p>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(template, current_period=current_period, next_period=next_period, next_day_time=next_day_time)

# ========================
# Run the Flask App
# ========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5013, debug=True)




### http://localhost:5013/html/schedule
### http://127.0.0.1:5013/html/schedule