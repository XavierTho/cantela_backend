# imports from flask
from __init__ import app, db
import google.generativeai as genai
import requests
import json
import os
from urllib.parse import urljoin, urlparse
from flask import abort, redirect, render_template, request, send_from_directory, url_for, jsonify
from flask_login import current_user, login_user, logout_user
from flask.cli import AppGroup
from flask_login import current_user, login_required
from flask import current_app
from werkzeug.security import generate_password_hash
import shutil
from flask_cors import CORS  # Import CORS
from flask import Blueprint, jsonify
from api.flashcard_import import flashcard_import_api

# import "objects" from "this" project
from __init__ import app, db, login_manager  # Key Flask objects 
# API endpoints
from api.user import user_api 
from api.pfp import pfp_api
from api.nestImg import nestImg_api  # Custom format
from api.post import post_api
from api.channel import channel_api
from api.group import group_api
from api.section import section_api
from api.nestPost import nestPost_api  # Custom format
from api.messages_api import messages_api  # Messages
from api.flashcard import flashcard_api
from api.vote import vote_api
from api.studylog import studylog_api
from api.gradelog import gradelog_api
from api.profile import profile_api
from api.tips import tips_api


# database Initialization functions
from model.user import studylog, gradelog, User, initUsers
from model.section import Section, initSections
from model.group import Group, initGroups
from model.channel import Channel, initChannels
from model.post import Post, initPosts
from model.nestPost import NestPost, initNestPosts
from model.vote import Vote, initVotes
from model.flashcard import Flashcard, initFlashcards
from model.studylog import initStudyLog
from model.gradelog import initGradeLog
from model.profile import Profile, initProfiles
from model.chatlog import Chatlog, initChatlog

# server only Views

# register URIs for API endpoints
app.register_blueprint(messages_api)
app.register_blueprint(user_api)
app.register_blueprint(pfp_api) 
app.register_blueprint(post_api)
app.register_blueprint(channel_api)
app.register_blueprint(group_api)
app.register_blueprint(section_api)
app.register_blueprint(nestPost_api)
app.register_blueprint(nestImg_api)
app.register_blueprint(vote_api)
app.register_blueprint(flashcard_api)
app.register_blueprint(flashcard_import_api)
app.register_blueprint(studylog_api)
app.register_blueprint(gradelog_api)
app.register_blueprint(profile_api)
app.register_blueprint(tips_api)


# Tell Flask-Login the view function name of your login route
login_manager.login_view = "login"

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login', next=request.path))
 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Helper function to check if the URL is safe for redirects
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next_page = request.args.get('next', '') or request.form.get('next', '')
    if request.method == 'POST':
        user = User.query.filter_by(_uid=request.form['username']).first()
        if user and user.is_password(request.form['password']):
            login_user(user)
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page or url_for('index'))
        else:
            error = 'Invalid username or password.'
    return render_template("login.html", error=error, next=next_page)

@app.route('/logout')
def logout():
    # Your existing logout logic here
    pass

# New routes for study tracker
@app.route('/api/study-tracker/log', methods=['POST'])
def log_study_session():
    try:
        data = request.json
        new_log = studylog(
            user_id=data['user_id'],
            subject=data['subject'],
            hours_studied=data['hours'],
            notes=data.get('notes', '')
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({'message': 'Study session logged successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/study-tracker/progress/<int:user_id>', methods=['GET'])
def get_study_progress(user_id):
    try:
        logs = studylog.query.filter_by(user_id=user_id).all()
        data = [
            {'subject': log.subject, 'hours': log.hours_studied, 'date': log.date.strftime('%Y-%m-%d')}
            for log in logs
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Routes for grade logger
@app.route('/api/grade-tracker/log', methods=['POST'])
def log_grade():
    """
    Log a new grade for a user.
    """
    try:
        data = request.json
        new_log = gradelog(
            user_id=data['user_id'],
            subject=data['subject'],
            grade=data['grade'],  # Changed from hours_studied to grade
            notes=data.get('notes', '')
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({'message': 'Grade logged successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/grade-tracker/progress/<int:user_id>', methods=['GET'])
def get_grade_progress(user_id):
    """
    Retrieve all grades for a specific user.
    """
    try:
        logs = gradelog.query.filter_by(user_id=user_id).all()
        data = [
            {
                'subject': log.subject,
                'grade': log.grade,  # Changed from hours to grade
                'date': log.date.strftime('%Y-%m-%d')
            }
            for log in logs
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    print("Home:", current_user)
    return render_template("index.html")

@app.route('/users/table')
@login_required
def utable():
    users = User.query.all()
    return render_template("utable.html", user_data=users)

@app.route('/users/table2')
@login_required
def u2table():
    users = User.query.all()
    return render_template("u2table.html", user_data=users)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.delete()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/reset_password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    if current_user.role != 'Admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.update({"password": app.config['DEFAULT_PASSWORD']}):
        return jsonify({'message': 'Password reset successfully'}), 200
    return jsonify({'error': 'Password reset failed'}), 500

@app.route('/api/id', methods=['GET'])
def get_id():
    return jsonify({"message": "API is working!"}), 200


# Custom CLI Commands
custom_cli = AppGroup('custom', help='Custom commands')

@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initSections()
    initGroups()
    # initChannels()
    initPosts()
    initFlashcards()
    initChatlog()

def backup_database(db_uri, backup_uri):
    if backup_uri:
        db_path = db_uri.replace('sqlite:///', 'instance/')
        backup_path = backup_uri.replace('sqlite:///', 'instance/')
        shutil.copyfile(db_path, backup_path)
        print(f"Database backed up to {backup_path}")
    else:
        print("Backup not supported for production database.")

def extract_data():
    data = {}
    with app.app_context():
        data['users'] = [user.read() for user in User.query.all()]
        data['sections'] = [section.read() for section in Section.query.all()]
        data['groups'] = [group.read() for group in Group.query.all()]
        data['channels'] = [channel.read() for channel in Channel.query.all()]
        data['posts'] = [post.read() for post in Post.query.all()]
    return data

def save_data_to_json(data, directory='backup'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for table, records in data.items():
        with open(os.path.join(directory, f'{table}.json'), 'w') as f:
            json.dump(records, f)
    print(f"Data backed up to {directory} directory.")

def load_data_from_json(directory='backup'):
    data = {}
    for table in ['users', 'sections', 'groups', 'channels', 'posts']:
        with open(os.path.join(directory, f'{table}.json'), 'r') as f:
            data[table] = json.load(f)
    return data

def restore_data(data):
    with app.app_context():
        users = User.restore(data['users'])
        _ = Section.restore(data['sections'])
        _ = Group.restore(data['groups'], users)
        _ = Channel.restore(data['channels'])
    print("Data restored to the new database.")

@custom_cli.command('backup_data')
def backup_data():
    data = extract_data()
    save_data_to_json(data)
    backup_database(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_BACKUP_URI'])

@custom_cli.command('restore_data')
def restore_data_command():
    data = load_data_from_json()
    restore_data(data)

app.cli.add_command(custom_cli)

# AI Homework Help Endpoint
genai.configure(api_key="AIzaSyAdopg5pOVdNN8eveu5ZQ4O4u4IZuK9NaY")
model = genai.GenerativeModel('gemini-pro')

@app.route('/api/ai/help', methods=['POST'])
def ai_homework_help():
    data = request.get_json()
    question = data.get("question", "")
    
    if not question:
        return jsonify({"error": "No question provided."}), 400
    try:
        response = model.generate_content(
            f"Your name is CanTeach. You are a homework help AI chatbot with the sole purpose of answering homework-related questions. "
            f"Under any circumstances, don't answer non-homework-related questions.\n"
            f"Here is your prompt: {question}"
        )
        
        new_msg = Chatlog(prompt=question, response=response.text)
        new_msg.create()
        return jsonify({"response": response.text}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500
    

@app.route('/profiles', methods=['GET'])
def get_profiles():
    profiles = Profile.query.all()
    return jsonify([profile.read() for profile in profiles])
#get all profiles

@app.route('/profiles/<int:id>', methods=['GET'])
def get_profile(id):
    profile = Profile.query.get_or_404(id)
    return jsonify(profile.read())
#get a specific profile

@app.route('/profiles', methods=['POST'])
def create_profile():
    data = request.json
    new_profile = Profile(
        name=data['name'],
        classes=data['classes'],
        favorite_class=data['favorite_class'],
        favorite_flashcard=data['favorite_flashcard'],
        grade=data['grade'],
        user_id=data['user_id']
    )
    try:
        new_profile.create()
        return jsonify(new_profile.read()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
#create new profile post
    
if __name__ == "__main__":
    with app.app_context():
        initFlashcards()
        initStudyLog()
        initGradeLog()
        initProfiles()
        # initChatlog()
    app.run(debug=True, host="0.0.0.0", port="8887")
