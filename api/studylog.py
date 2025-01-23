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
        @token_required()
        def get(self):
            all_studylogs = StudyLog.query.all()
            studylogs = []

            for log in all_studylogs:
                studylogs.append(log.read())

            return jsonify(studylogs)

        @token_required()
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

        @token_required()
        def put(self):
            try:
                data = request.get_json()
                if not data:
                    return {'message': 'No input data provided'}, 400

                studylog_id = data.get('id')
                studylog = StudyLog.query.get(studylog_id)
                if not studylog:
                    return {'message': 'StudyLog not found'}, 404

                studylog.user_id = data.get('user_id', studylog.user_id)
                studylog.subject = data.get('subject', studylog.subject)
                studylog.hours_studied = data.get('hours_studied', studylog.hours_studied)
                studylog.notes = data.get('notes', studylog.notes)
                db.session.commit()

                return jsonify(studylog.read())
            
            except Exception as e:
                return {'message': f"An error occurred: {str(e)}"}, 500

        @token_required()
        def delete(self):
            try:
                data = request.get_json()
                if not data:
                    return {'message': 'No input data provided'}, 400

                studylog_id = data.get('id')
                studylog = StudyLog.query.get(studylog_id)
                if not studylog:
                    return {'message': 'StudyLog not found'}, 404

                db.session.delete(studylog)
                db.session.commit()

                return {'message': 'StudyLog deleted successfully'}, 200
            
            except Exception as e:
                return {'message': f"An error occurred: {str(e)}"}, 500

        @staticmethod
        def restore(data):
            for log_data in data:
                _ = log_data.pop('id', None)  # Remove 'id' from log_data
                user_id = log_data.get("user_id", None)
                subject = log_data.get("subject", None)
                studylog = StudyLog.query.filter_by(user_id=user_id, subject=subject).first()
                if studylog:
                    studylog.update(log_data)
                else:
                    studylog = StudyLog(**log_data)
                    studylog.create()

    api.add_resource(CRUD, '/studylognew')