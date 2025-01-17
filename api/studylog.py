import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app, db
from api.jwt_authorize import token_required
from model.studylog import StudyLog
import json

studylog_api = Blueprint('studylog_api', __name__, url_prefix='/api')

api = Api(studylog_api)


class StudyLogAPI:
    class CRUD(Resource):
        def post(self):
            try:
                data = request.get_json()
            
                if not data:
                    return {'message': 'No input data provided'}, 400
                
                user_id = data.get('user_id')
                subject = data.get('subject')
                hours_studied = data.get('hours_studied')
                notes = data.get('notes')

                '''
                Example payload:
                {
                    "user_id": 1,
                    "subject": "AP Physics",
                    "hours_studied": 2.5,
                    "notes": "Studied Newton's Laws of Motion."
                }
                '''
                
                if not user_id:
                    return {'message': 'User ID is required'}, 400
                if not subject:
                    return {'message': 'Subject is required'}, 400
                if not hours_studied:
                    return {'message': 'Hours studied is required'}, 400
                if not notes:
                    return {'message': 'Notes is required'}, 400
                
                studylog = StudyLog(user_id, subject, hours_studied, notes)
                print(json.dumps({
                    "user_id": user_id,
                    "subject": subject,
                    "hours_studied": hours_studied,
                    "notes": notes
                }))
                studylog.create()

                return jsonify(studylog.read())
            
            except Exception as e:
                return {'message': f"An error occurred: {str(e)}"}, 500

            
    api.add_resource(CRUD, '/studylognew')