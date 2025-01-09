from flask import Blueprint, jsonify, Flask
from flask_restful import Api, Resource  # For building REST APIs
from flask_cors import CORS  # Handles cross-origin requests

# Set up the Flask app and API
profile_api = Blueprint('profile_api', __name__, url_prefix='/api')  # Blueprint for modular API
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allows frontend to talk to the backend without issues

api = Api(profile_api)  # Connect the API to the Blueprint

# This is where we store all the student info for now (just static data)
class ProfileAPI:
    def get_student(name):
        students = {
            "Thomas Edison": {
                "Classes": ["AP Physics", "AP Chemistry", "AP Statistics"],
                "FavoriteClass": "AP Physics",
                "FavoriteFlashcard": "Kinematics Equations",
                "Grade": "A"
            },
            "Grace Hopper": {
                "Classes": ["AP CSP", "AP Statistics", "AP US History"],
                "FavoriteClass": "AP CSP",
                "FavoriteFlashcard": "Binary Numbers",
                "Grade": "A+"
            },
            "Nicholas Tesla": {
                "Classes": ["AP Physics", "AP Chemistry", "AP Statistics"],
                "FavoriteClass": "AP Physics",
                "FavoriteFlashcard": "Electromagnetic Theory",
                "Grade": "A"
            },
            "Xavier Thompson": {
                "Classes": ["AP World History", "AP US History", "AP Statistics"],
                "FavoriteClass": "AP World History",
                "FavoriteFlashcard": "Industrial Revolution Key Terms",
                "Grade": "B+"
            },
            "Armaghan Zarak": {
                "Classes": ["AP US History", "AP World History", "AP CSP"],
                "FavoriteClass": "AP US History",
                "FavoriteFlashcard": "Constitutional Amendments",
                "Grade": "A-"
            },
            "Arush Shah": {
                "Classes": ["AP CSP", "AP Statistics", "AP Physics"],
                "FavoriteClass": "AP CSP",
                "FavoriteFlashcard": "Python Functions",
                "Grade": "A+"
            }
        }
        # Try to get the student data by name, or return None if not found
        return students.get(name)

# Each class below is basically an endpoint for one student's data
class ThomasResource(Resource):
    def get(self):
        student = ProfileAPI.get_student("Thomas Edison")
        if student:  # If we found the student, return their data
            return jsonify(student)
        return {"Data not found"}, 404  # If no data, send a 404 error

class GraceResource(Resource):
    def get(self):
        student = ProfileAPI.get_student("Grace Hopper")
        if student:
            return jsonify(student)
        return {"Data not found"}, 404

class NicholasResource(Resource):
    def get(self):
        student = ProfileAPI.get_student("Nicholas Tesla")
        if student:
            return jsonify(student)
        return {"Data not found"}, 404

class XavierResource(Resource):
    def get(self):
        student = ProfileAPI.get_student("Xavier Thompson")
        if student:
            return jsonify(student)
        return {"Data not found"}, 404

class ArmaghanResource(Resource):
    def get(self):
        student = ProfileAPI.get_student("Armaghan Zarak")
        if student:
            return jsonify(student)
        return {"Data not found"}, 404

class ArushResource(Resource):
    def get(self):
        student = ProfileAPI.get_student("Arush Shah")
        if student:
            return jsonify(student)
        return {"Data not found"}, 404

# Add routes for each student. The URL will map to the right resource.
api.add_resource(ThomasResource, '/data/Thomas')  # /api/data/Thomas
api.add_resource(GraceResource, '/data/Grace')    # /api/data/Grace
api.add_resource(NicholasResource, '/data/Nicholas')  # /api/data/Nicholas
api.add_resource(XavierResource, '/data/Xavier')  # /api/data/Xavier
api.add_resource(ArmaghanResource, '/data/Armaghan')  # /api/data/Armaghan
api.add_resource(ArushResource, '/data/Arush')    # /api/data/Arush
