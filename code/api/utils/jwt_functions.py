import requests

import subprocess
from dotenv import load_dotenv
import os

project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()
load_dotenv(os.path.join(project_folder, '.env'))
JWT_KEY = os.getenv('JWT_KEY')
JWT_PATH = os.getenv('JWT_PATH')
if JWT_KEY == None:
    JWT_KEY = os.environ.get('JWT_KEY')
    JWT_KEY = os.environ.get('JWT_PATH')


patient_emails = {
    'ustan': 'ppp1@ustan.com',
    'fcrb': 'ppp1@fcrb.com',
    'zmc': 'ppp1@zmc.com'
}

staff_emails = {
    'ustan': 'medstaff1@ustan.com',
    'fcrb': 'medstaff1@fcrb.com',
    'zmc': 'medstaff1@zmc.com'
}

admin_emails = {
    'ustan': 'hospadm1@ustan.com',
    'fcrb': 'hospadm1@fcrb.com',
    'zmc': 'hospadm1@zmc.com'
}

password = 'thisisagoodpassword'

def get_jwt(user, password=password):
    url = JWT_PATH + "/create_jwt/"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "username": user,
        "password": password,
        "login_type": "TEXT"
    }
    try:
        response = requests.request("POST", url, headers=headers, json=body)
        if response.status_code == 201:
            return {"status_code": response.status_code, "body": response.json()}
        else:
            return {"status_code": response.status_code, "body": response.text}
    except Exception as e:
        print("Failed to make request. Reason: {}​".format(str(e)))