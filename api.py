from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restplus import Api, Resource, fields
from dotenv import load_dotenv
from pathlib import Path

import os
import subprocess
import json

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



# Name spaces

hello_space = api.namespace('hello', description='Check the server is on')


# Routes

@hello_space.route('/hello')
class ServerCheck(Resource):
    @api.marshal_with(hello)
    def get(self):
        return {"hello": "Welcome to the API. The server is on"}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')