from flask import Blueprint
from flask_restful import Api, Resource # used for REST API building

student_api = Blueprint('student_api', __name__,
                   url_prefix='/api')

# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(student_api)

class StudentAPI:        
    class _John(Resource): 
        def get(self):
           # implement the get method 
           pass
    
    class _Jeff(Resource): 
        def get(self):
           # implement the get method 
           pass

    # building RESTapi endpoint
    api.add_resource(_John, '/student/john')          
    api.add_resource(_Jeff, '/student/jeff')