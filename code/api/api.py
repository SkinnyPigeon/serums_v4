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
from functions.encryption import encrypt_data_with_new_key, encrypt_key


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

request_fields = api.model('Request Smart Patient Health Record', {
    'serums_id': fields.Integer(required=True, description='The Serums ID for the patient', example=364),
    'tags': fields.String(required=True, description='Rule to be executed', example=['address', 'treatments', 'wearable']),
    'hospital_ids': fields.String(required=True, description='The id of the hospital for the source data', example=['FCRB', 'USTAN', 'ZMC']),
    'public_key': fields.String(required=True, description="The public key used as part of the API's encryption", example="""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCDM+DNCybR7LdizOcK1gH2P7dD
sajGUEIoPFp7wjhgKykYkCGVQCvl55g/zdh6UI9Cd/i2IEf5wo+Ct9oihy9SnJSp
3sOp1KESV+ElwdK3vkaIo1AUuj+E8LTe7llyJ61JJdZaozyT0PxM8jB2vIaNEdbO
bURHcIsIDc64L0e1ZQIDAQAB
-----END PUBLIC KEY-----""")
})

reply_fields = api.model('Successful Response', {
    'key': fields.String(required=True, description='The encrypted Fernet key', example="BqKQKHWaCMOozw8U77Cvh0Mj8S+HnvkjuOYzZKrF9L4unP+S9xosAiBF0lJ1hOgZ5mfo0EfyxFdyuBh0ywNBNSUxJdCdnQ+ocwkd14IjsE54VmwTXdTFVcdepR1tjudcIyvVCy+Mxymt4vPh1P7pYTl92wYkEovEpHrs28l++EsaPOgZUiAD7LD5lZ0jZCW5fyFtyBwm8n+aAhNlb0YKnoYKDb88bg9DFyQxazX8SVBBwfmJEklSunVe5s9FULm50BeY1eDS87noQ4nM+so1EPsN5GuBM41KmeySwZZCVYiLh5NfwY+f5efMPbtV683pCL3YoJ89ojYeTlMLJEug=="),
    'data': fields.String(required=True, description='The encrypted patient record', example="gAAAAABeneOIy6q3QxfwmHTjxMjZdP5rxKaQFDbYT-KtJOzgsqZYdnct3qsRcNcAzIrmcnDluR-Q6RLLi8CUthGsa_-7b-VCZrkRO3cLcGKLNuPi2v109dSzXeQ27EazKf49oss4IE11khs6tLZt-yqYCZTz_R84gK6X0BMc0pzoYP-3Qr_h1rV_I6DD3oWHpnbRE4vn86HSR77YajYsi3BGbqPfh-_FJYlgaPWG5USiIXoQYTvJCtHj8kcM9jdhkNICGdlnLkuSZ2A60zx8XpcHImQYd5YzbxENMvWl0Q6SamziiZ5Kl5UXzlyY3IHGpTM-K9T-ycmZj6dkr0hzzqr8lAiWNSinZR2YZDM-diGM7tr8b10hGLF2D1_7-ArvuP12f_aznLgonn4kZtDpro2ImGmzsg-oz01B0pZjNkTvkmOaz32e1ntmvWHBD16yLLHPFdQDw--z0R4i7n_WNJB0Jn3M0sgyHsIkBIB53Pg8ZFKoAxnfACiKIaPJ26JtrVEQ9es6VupfDCT4nUM2WPIiegZ5LmQDXuGBwvw9NrfEW4pC5Sg7CoRv6RvTuT_ywSrhCnd2jePxpdIk0FqTdUsAqancd09IWEnFWQpLxTr348Qq3Dplk5L_dws2H2y8e--AAkBoy08Q-OpT5o8DFS1i9nO84r0KXgWIo4APcmH0UOL53INsgULZDSohzcT675zV8wWxfaja_b3CIVsj54iKs--XgdoSQHijhgasW1UqYgSRqGjW18BTPHUfA1uJ4397U3ZBjZTKCwzgzhr4YBVSBhxMGqEWw8sJCLBXLGxr0MUl1kDRmSptBsc2k7EerGm8JlKI4Xu6XbmXJy3Mjq4aa7Q0elayCnr5izbh9-VJoOEnXMkNgS4PcsEPm3yQdlyk1AlkXK71S4gfUW0DVzfh3NJxWS-xnHPGafu0WnvDdl42wUl-prt6A8AAHWQOQZW1hrGi3gxwCJqQ5vOcqmxXuMdGdCd7xEdBaeuzOFBZSLW5AF1i_0gvmMQAr7YYsV33ZKfX59UHuQG7-Ia9WNRhCRvm2N35jZBQz-F2uenNHd5RFB4h28OvJ5yIVKHVmDAVxrAfq2tf6liqdhECPwqV1BUf13TfF-LDwm93zp4Sp4Enbjur4egN1Pyl2lkGQNQKSWHgAgzq60uNPuzeS-DUm0OvnxmDGaJ-S966lBl7FmPOnoZCJZTk3uXB96m3N4qJ6dZddgqKQDfhBG_Zd87wVQbLjR4bYdBqcH3NY51s1mqjurRzy5RCEqsZCZQL7xCRh5uwyjWZC-oqIp9XBTyqvu7E_j6kWIGX4P0FispRPOxc-LJLoau6Fu1Fp1ZcxBLYBJyRfBAnwIaoRHpoM_zlWUVzkEx_ChUYFkxjCBEJMqf027087_aTB5rdFNxm7etW5RQBPcWwc5KtxTcWo9ae5XfE1aJmRVX17P2rlkXmYD9oiZdOxt21hUktNKM1Y3ZXmbfKLsgteFHv1G8KTN52xPz4y0AYmORD2U1jFn_e0DeQulYQrdgcTys9WLmteZZe1CE7VgBmj-Pd_U9zDMJ8OI8jj3Y7enuWa1TiIyCuHzwnNcT7wDnlcbrpxQfz3zztsdAw6qO1HfJm4VgA0K1UeCQzggySjMUaYMQa20euqLIko-TmdoWPjgIPG0BcVKXbbwyeW178M8ZOMZ32Y-zoZoWs26GwzrKZFolX4EHiNvZlKBa5FJmi4l6aGjT5r4Ipe68EYwsojCCNdtTVO4Ds1tfeNqDT3FmuBktg3aLAwQggQj_Jinjc9hLglTqfKm5TSUEl1iIvt3t9jxv5UKJ06LgXru2YZxX6f255wPmtHVxqqBggVLmhpRKTV2ifq6bQ0AWSexN3PKQ6XXIpsF2UWmtUJABiJmRuy4UOg85uZC4V56JjJFEwiAjw9VBYf5I0nbSOaBEQkSx7-qSF2fXOkYKw7fl09ur9Q40ZkvVDcCtJRemPMpult7sVB_lg3eINTwSq8tqN6AOrsBQpk4UjidQlXatgXKtXWahkINCruy_PHlQQSYCLL9UxUMhA9Xw1WDircweDeS_4IwoSWqrApu1FBRYQemHvGpWO1kGrdhJCph9V548iRIJd5-6q5lWDZiGGWVs5_drjS6LlBgWNOrkxV80Hv1EI0eKm_G9N08HvpEHhcOu1tpRZhLFzPP5PvWlEecXUTbrxJ6RJEJVBRxTDnzW2ngSoHSC10rZdAwcTV6nkeGYcUv_TH-TJxsBe6-3p8kMpJaGaGIJ83e9av0Uegonl0KGbv0XGcmI2MR2rAvgyPN4oSDtsCqu2pYVeIjF8JJq-WmJfKpP8TwiFGQgXRJSyAkOSDfQF3K4f3ucjW-Vca5YMX7q7b3jtV_YyVZDB-pUve6qaRFcgKw7ZDoQAVMY04yNMG61YWpjetPHl4sf3j39_CMinVq5UGHZgvlTErEqBIVaFksee5QDL5M552-ksp9XHuxOewK-QzpKqK7WalNnwI9YxlRJEu1utoOrp3y5ZO-HtLLTGjunL9bwSaFQ_M1MqqNqDHMOUEwuZuiF0zLq61UDT5Z00JXsYbMBRHFqYam6KkTrEub6Dx9pljsQW-J-S0LAJWO5pnsRSCQuoHu6tx3cTnPeCJQMMA1ThqFcrELxmM3EYv4pUZ6AiugwaTmq2Ym4f_UF9hgIr74O8M2xgTUOc2eoLaMuPInf55EzzKtWNuDrGvKsEJAgKzCDn7w==")
})

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



@sphr_space.route('/get_sphr')
class SPHR(Resource):
    '''Return the Smart Patient Health Record from the Serums data lake'''
    @api.doc(body=request_fields)
    # @api.marshal_with(reply_fields, code=200)
    def post(self):

        body = {
            "serums_id": 364,
            "tags": ["all"],
            "hospital_ids": ["FCRB"],
            "public_key": "abc"
        }
        # body = request.get_json()
        patient_data = get_patient_data(body)

        return patient_data


@sphr_space.route('/encrypted')
class SPHR_Encrypted(Resource):
    '''Return the encrypted Smart Patient Health Record from the Serums data lake'''
    @api.doc(body=request_fields)
    def post(self):
        body = request.get_json()
        patient_data = get_patient_data(body)
        encrypted_data, encryption_key, public_key = encrypt_data_with_new_key(patient_data, body['public_key'])
        encrypted_key = encrypt_key(encryption_key, public_key)
        return {'data': encrypted_data, 'key': encrypted_key} 


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')
