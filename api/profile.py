from flask import Blueprint, jsonify, Flask
from flask_restful import Api, Resource  # used for REST API building
from flask_cors import CORS

profile_api = Blueprint('profile_api', __name__, url_prefix='/api')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')

# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(profile_api)

class ProfileAPI:
    # @app.route('/api/profile/')
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
        return students.get(name)

class ThomasResource(Resource):
    def get(self):
        student = ProfileAPI.get_student("Thomas Edison")
        if student:
            return jsonify(student)
        return {"Data not found"}, 404

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

# Building REST API endpoint
api.add_resource(ThomasResource, '/data/Thomas')
api.add_resource(GraceResource, '/data/Grace')
api.add_resource(NicholasResource, '/data/Nicholas')
api.add_resource(XavierResource, '/data/Xavier')
api.add_resource(ArmaghanResource, '/data/Armaghan')
api.add_resource(ArushResource, '/data/Arush')
