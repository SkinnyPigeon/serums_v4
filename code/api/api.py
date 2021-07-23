from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restplus import Api, Resource, fields
from dotenv import load_dotenv
from pathlib import Path

import os
import subprocess
import json


# Functions

from functions.jwt import validate_jwt, refresh_jwt
from functions.departments import get_departments
from functions.ml import get_patient_data
from functions.get_source_data import get_patient_data


# Setting up environment

FLASK_DEBUG = 1

project_folder = subprocess.check_output(
    "pwd", shell=True).decode("utf-8").rstrip()
load_dotenv(os.path.join(project_folder, '.env'))
PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
if PORT == None:
    PASSWORD = os.environ.get('PGPASSWORD')
    PORT = os.environ.get('PGPORT')

app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
CORS(app)
api = Api(
    app,
    version='0.0.1',
    title='Smart Patient Health Record API',
    description='Return the encrypted Smart Patient Health Record from the Serums data lake',
)

# Models

hello = api.model('Server Check', {
    'hello': fields.String(required=True, description='Quick check that the server is on', example='Welcome to the API. The server is on')
})

parser = api.parser()


# Staff

staff_parser = api.parser()
staff_parser.add_argument('Authorization', help="The authorization token", location="headers",
                          default="""Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMDkwNTkzOCwianRpIjoiNjZjNTgwYmUtOTViMC00YjhiLWE3ZjQtYzU3ODkyOGJhM2NjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QiLCJuYmYiOjE2MjA5MDU5MzgsImV4cCI6MTg4MDEwNTkzOH0.zeJNNiXE7XbeNPC5g2OEQvu1EsYeohUsgvsY2_fg8EM""")


# Machine learning

ml_parser = api.parser()
ml_parser.add_argument('Authorization', help="The authorization token", location="headers",
                       default="""Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMDkwNTkzOCwianRpIjoiNjZjNTgwYmUtOTViMC00YjhiLWE3ZjQtYzU3ODkyOGJhM2NjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QiLCJuYmYiOjE2MjA5MDU5MzgsImV4cCI6MTg4MDEwNTkzOH0.zeJNNiXE7XbeNPC5g2OEQvu1EsYeohUsgvsY2_fg8EM""")


# Smart Patient Health Record

sphr_parser = api.parser()
sphr_parser.add_argument('Authorization', help="The authorization token", location="headers",
                         default="""Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMDkwNTkzOCwianRpIjoiNjZjNTgwYmUtOTViMC00YjhiLWE3ZjQtYzU3ODkyOGJhM2NjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QiLCJuYmYiOjE2MjA5MDU5MzgsImV4cCI6MTg4MDEwNTkzOH0.zeJNNiXE7XbeNPC5g2OEQvu1EsYeohUsgvsY2_fg8EM""")

# Name spaces

hello_space = api.namespace('hello', description='Check the server is on')
staff_space = api.namespace(
    'staff_tables', description='Return the staff tables')
ml_space = api.namespace(
    'machine_learning', description='Return the patient data for the machine learning algorithm')
sphr_space = api.namespace('smart_patient_health_record',
                           description='Retrieve the Smart Patient Health Record')

# Routes

# Server check


@hello_space.route('/hello')
class ServerCheck(Resource):
    @api.marshal_with(hello)
    def get(self):
        return {"hello": "Welcome to the API. The server is on"}


# Staff tables

@staff_space.route('/department')
class Department(Resource):
    def post(self):
        refreshed_jwt = refresh_jwt()
        print(refreshed_jwt)
        jwt = refreshed_jwt['body']['resource_str']
        response = validate_jwt(jwt)
        print(response['body'])
        if response['status_code'] == 200:
            department_ids = get_departments(response['body'])
        return department_ids


# Machine Learning

@ml_space.route('/analytics')
class MachineLearning(Resource):
    def post(self):
        refreshed_jwt = refresh_jwt()
        jwt = refreshed_jwt['body']['resource_str']
        response = validate_jwt(jwt)
        print(response['body'])
        if response['status_code'] == 200:
            patient_data = get_patient_data(response['body'])
        return patient_data


# Smart Patient Health Record


@sphr_space.route('/sphr')
class SPHR(Resource):
    def post(self):
        
        body = {
            'serums_id': 364,
            'hospital_ids': ['ZMC', 'USTAN'],
            'tags': ['wearable', 'all']
        }
        patient_data = get_patient_data(body)

        return patient_data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')
