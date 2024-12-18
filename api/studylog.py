from flask import Blueprint, request, g
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.studylog import StudyLog

# Blueprint and API
studylog_api = Blueprint('studylog_api', __name__, url_prefix='/api')
api = Api(studylog_api)

class StudylogAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new study session."""
            current_user = g.current_user
            data = request.get_json()


            # Validate input
            if not data or 'subject' not in data or 'hours' not in data:
                return {"message": "Subject and hours are required"}, 400
            
            # Create a new study log
            new_study_log = StudyLog(
                user_id=current_user.id,
                subject=data['subject'],
                hours_studied=data['hours'],
                notes=data.get('notes', '')
            )
            created_log = new_study_log.create()
            if created_log:
                return {"message": "Study session logged successfully", "study_log_id": created_log.id}, 201
            return {"message": "Failed to create study log"}, 500

        @token_required()
        def get(self):
            """Get all study sessions for the current user."""
            current_user = g.current_user
            study_logs = StudyLog.query.filter_by(user_id=current_user.id).all()
            logs = [{
                'id': log.id,
                'subject': log.subject,
                'hours_studied': log.hours_studied,
                'notes': log.notes,
                'date': log.date.strftime('%Y-%m-%d')
            } for log in study_logs]
            return logs, 200

        @token_required()
        def put(self):
            """Update an existing study log."""
            data = request.get_json()
            if not data or 'id' not in data:
                return {"message": "Study Log ID is required"}, 400
            study_log = StudyLog.query.get(data['id'])
            if not study_log or study_log.user_id != g.current_user.id:
                return {"message": "Study Log not found or unauthorized"}, 404
            updated_log = study_log.update(data)
            return updated_log.read(), 200

        @token_required()
        def delete(self):
            """Delete a study log."""
            data = request.get_json()
            if not data or 'id' not in data:
                return {"message": "Study Log ID is required"}, 400
            study_log = StudyLog.query.get(data['id'])
            if not study_log or study_log.user_id != g.current_user.id:
                return {"message": "Study Log not found or unauthorized"}, 404
            study_log.delete()
            return {"message": "Study Log deleted successfully"}, 200

# Register the resource
api.add_resource(StudylogAPI._CRUD, '/studylog')