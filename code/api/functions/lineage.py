import time
import requests
import jwt

import os
from dotenv import load_dotenv
import subprocess

project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()
load_dotenv(os.path.join(project_folder, '.env'))
BCPASSWORD = os.getenv('BCPASSWORD')
if BCPASSWORD == None:
    BCPASSWORD = os.environ.get('BCPASSWORD')

def create_record(serums_id, hospitals):
    pass
