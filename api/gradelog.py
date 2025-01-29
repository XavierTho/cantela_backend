from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from __init__ import db
from model.gradelog import GradeLog

# Create a Blueprint for the gradelog API
gradelog_api = Blueprint('gradelog_api', __name__, url_prefix='/api')
# Create an API object for the Blueprint
api = Api(gradelog_api)

# Define the GradelogAPI class
class GradelogAPI:
    # Define an inner class _CRUD that inherits from Resource
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new grade entry.
            
            This method handles POST requests to create a new grade log entry.
            It requires the user to be authenticated and expects a JSON payload
            with 'subject' and 'grade' fields. Optionally, 'notes' can also be provided.
            """
            # Get the current authenticated user
            current_user = g.current_user
            # Get the JSON data from the request body
            data = request.get_json()

            # Validate input: Check if 'subject' and 'grade' are present in the data
            if not data or 'subject' not in data or 'grade' not in data:
                return {"message": "Subject and grade are required"}, 400
            
            # Create a new GradeLog instance with the provided data
            new_grade_log = GradeLog(
                user_id=current_user.id,
                subject=data['subject'],
                grade=data['grade'],
                notes=data.get('notes', '')  # Use an empty string if 'notes' is not provided
            )
            # Save the new grade log to the database
            created_log = new_grade_log.create()
            if created_log:
                # Return a success message with the ID of the created grade log
                return {"message": "Grade logged successfully", "grade_log_id": created_log.id}, 201
            # Return an error message if the grade log could not be created
            return {"message": "Failed to create grade log"}, 500

        @token_required()
        def get(self):
            """
            Get all grade entries for the current user.
            
            This method handles GET requests to retrieve all grade log entries
            for the authenticated user. It returns a JSON array of grade logs.
            """
            # Get the current authenticated user
            current_user = g.current_user
            # Query the database to get all grade logs for the current user
            all_gradelogs = GradeLog.query.filter_by(user_id=current_user.id).all()
            # Initialize an empty list to hold the grade logs
            gradelog = []

            # Iterate over the list of GradeLog instances
            for log in all_gradelogs:
                # Convert each GradeLog instance to a dictionary and append to the list
                gradelog.append(log.read())

            # Return the list of grade logs as a JSON response
            return jsonify(gradelog)

        @token_required()
        def put(self):
            """
            Update an existing grade log.
            
            This method handles PUT requests to update an existing grade log entry.
            It requires the user to be authenticated and expects a JSON payload
            with 'id' and the fields to be updated ('subject', 'grade', 'notes').
            """
            # Get the JSON data from the request body
            data = request.get_json()
            # Validate input: Check if 'id' is present in the data
            if not data or 'id' not in data:
                return {"message": "Grade Log ID is required"}, 400
            # Query the database to get the grade log by ID
            grade_log = GradeLog.query.get(data['id'])
            # Check if the grade log exists and belongs to the current user
            if not grade_log or grade_log.user_id != g.current_user.id:
                return {"message": "Grade Log not found or unauthorized"}, 404
            # Update the grade log with the new data
            updated_log = grade_log.update(data)
            # Return the updated grade log as a JSON response
            return updated_log.read(), 200

        @token_required()
        def delete(self):
            """
            Delete a grade log.
            
            This method handles DELETE requests to delete an existing grade log entry.
            It requires the user to be authenticated and expects the 'id' of the grade log
            to be provided as a query parameter.
            """
            # Get the grade log ID from the query parameters
            grade_log_id = request.args.get('id')
            # Validate input: Check if the grade log ID is provided and is a digit
            if not grade_log_id or not grade_log_id.isdigit():
                return {"message": "A valid Grade Log ID is required"}, 400

            # Query the database to get the grade log by ID
            grade_log = GradeLog.query.get(int(grade_log_id))
            # Check if the grade log exists and belongs to the current user
            if not grade_log or grade_log.user_id != g.current_user.id:
                return {"message": "Grade Log not found or unauthorized"}, 404

            try:
                # Delete the grade log from the database
                grade_log.delete()
                # Return a success message
                return {"message": "Grade Log deleted successfully"}, 200
            except Exception as e:
                # Return an error message if an exception occurs
                return {"message": f"An error occurred: {str(e)}"}, 500

# Register the _CRUD resource with the API
api.add_resource(GradelogAPI._CRUD, '/gradelog')
