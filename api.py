from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restplus import Api, Resource, fields
from dotenv import load_dotenv
from pathlib import Path

import os
import subprocess
import json


# Functions

from functions.jwt import validate_jwt


# Setting up environment

FLASK_DEBUG=1

project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()
load_dotenv(os.path.join(project_folder, '.env'))
PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')

app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
CORS(app)
api = Api(
    app, 
    version='0.0.1', 
    title='Blank API',
    description='This is the a template for writing APIs in Flask',
)

# Models

hello = api.model('Server Check', {
    'hello': fields.String(required=True, description='Quick check that the server is on', example='Welcome to the API. The server is on')
})


parser = api.parser()
# parser.add_argument('Name of field', type=list, required=True, help='Field used as part of request or reply', location='json')
# parser.add_argument('Name of another field', type=list, required=True, help='Another field used as part of request or reply', location='json')

jwt_parser = api.parser()
jwt_parser.add_argument('Authorization', help="The authorization token", location="headers", default="""Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMDkwNTkzOCwianRpIjoiNjZjNTgwYmUtOTViMC00YjhiLWE3ZjQtYzU3ODkyOGJhM2NjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QiLCJuYmYiOjE2MjA5MDU5MzgsImV4cCI6MTg4MDEwNTkzOH0.zeJNNiXE7XbeNPC5g2OEQvu1EsYeohUsgvsY2_fg8EM""")


# Name spaces

hello_space = api.namespace('hello', description='Check the server is on')
staff_space = api.namespace('staff tables', description='Return the staff tables')
jwt_space = api.namespace('jwt', description='JWT endpoints')


# Routes

@hello_space.route('/hello')
class ServerCheck(Resource):
    @api.marshal_with(hello)
    def get(self):
        return {"hello": "Welcome to the API. The server is on"}

@staff_space.route('/department')
class Department(Resource):
    def post(self):


        return 200

@jwt_space.route("/authorize_jwt", methods=["POST"])
class AuthJWT(Resource):
    '''Verify JWT with Authentication module'''
    def post(self):

        jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjIyODAwNTI4LCJqdGkiOiJmZDk1MzcxOTVlOTE0ZTk1YjllZWI4MjMwYmViODVlOSIsInVzZXJJRCI6MzY0LCJpc3MiOiJTZXJ1bXNBdXRoZW50aWNhdGlvbiIsImlhdCI6MTYyMjE5NTcyOCwic3ViIjoiZXVhbkB0ZXN0LmNvbSIsImdyb3VwSURzIjpbIlBBVElFTlQiXSwib3JnSUQiOiJVU1RBTiIsImF1ZCI6Imh0dHBzOi8vdXJsZGVmZW5zZS5wcm9vZnBvaW50LmNvbS92Mi91cmw_dT1odHRwLTNBX193d3cuc2VydW1zLmNvbSZkPUR3SURhUSZjPWVJR2pzSVRmWFBfeS1ETExYMHVFSFhKdlU4bk9IclVLOElyd05LT3RrVlUmcj11VGZONXVRMWtod2JSeV9UZ0tINmFVZDAtQmJtMEc4Sy1WYWprelpteTk4Jm09MmlVTm4yOUZTYWY3LTAzeHU5eE1CcmNuNHQ2VV8zdzN1cUxpTHl0VGZUNCZzPTVqQjJqbXFoc05BX2cxU1Z5WmdVRlJGOW9FUDhfQVFhLWxpY1lXM0l1ZncmZT0ifQ.7xY76j-_K7r3Dos7E0aoUoCnMmGLXwwzDa-d1TYRkeQ".encode('ascii', 'ignore').decode('unicode_escape')
        # print(jwt.encode('latin-1'))
        validate_jwt(jwt)
        return 200



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')
