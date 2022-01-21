import datetime
import requests
import jwt

import os
from dotenv import load_dotenv
import subprocess
from hashlib import md5, sha256

project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()
load_dotenv(os.path.join(project_folder, '.env'))
BCPASSWORD = os.getenv('BCPASSWORD')
BC_PATH=os.getenv('BC_PATH')
if BCPASSWORD == None:
    BCPASSWORD = os.environ.get('BCPASSWORD')
    BC_PATH=os.getenv('BC_PATH')


print(f"BCPASSWORD: {BCPASSWORD}")

url = BC_PATH + '/v1/api/proof/'

def create_record(serums_id, rule_id, hospital_ids):
    """Creates a record on the lineage blockchain that will track the creation of a Smart Patient Health Record
            Parameters:

                serums_id (int): The Serums ID of the patient whose Smart Patient Health Record is being created\n
                rule_id (str): The rule ID from the access blockchain that is being executed\n
                hospital_ids (list): The list of hospitals from which the Smart Patient Health Record is being created from

            Returns:

                proof_id (str): The proof ID of the newly created record on the lineage blockchain that will be used to continue to update the record
    """
    token = jwt.encode({}, BCPASSWORD, algorithm='HS256')
    print(f"TOKEN TYPE: {type(token)}")
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    print(f"BCTOKEN: {token}")
    header = {"Authorization": f"Bearer {token}"}
    body = {
        'serumsId': serums_id,
        'ruleId': rule_id,
        'hospitalIds': hospital_ids,
        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    }
    response = requests.post(url, data=body, headers=header)
    print(f"PROOF RESPONSE: {response.json()}")
    if response.status_code == 200:
        proof_id = response.json()['proofId']
        print(f"PROOF ID: {proof_id}")
        print(f"TOKEN: {token}")
        return proof_id
    else:
        print("ASKDJSKSJKAJSDK")
        return False

def update_record(proof_id, stage, status, content, hospital_id=None):
    print(f"UPDATING RECORD PROOF ID: {proof_id}")
    """Update the record on the lineage blockchain during each stage of the creation of a Smart Patient Health Record

            Parameters:

                proof_id (str): The proof ID of the an existing record on the lineage blockchain\n
                stage (str): The stage of the Smart Patient Health Record creation process which is being executed. Enum: [data_selected, data_filled, data_vault_created, encryption, cleanup]\n
                hospital_id (str): The current hospital that is having its data pulled from\n
                status (str): Whether or not the process was successful. Enum: [success, failed]\n
                content (dict): A dictionary containing details about the operation 
    """
    token = jwt.encode({}, BCPASSWORD, algorithm='HS256')
    print(f"TOKEN TYPE: {type(token)}")
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    print(f"BCTOKEN: {token}")
    header = {"Authorization": f"Bearer {token}"}
    update_url = url + proof_id
    if hospital_id != None:
        body = {
            'id': proof_id,
            'type': stage,
            'hospitalId': hospital_id,
            'status': status,
            'content': content,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        }
    else:
        body = {
        'id': proof_id,
        'type': stage,
        'status': status,
        'content': content,
        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    }
    try:
        response = requests.patch(update_url, json=body, headers=header)
        print(f"UPDATED CALL: {response.json()}")
        if response.status_code == 200:
            return {'stage': stage, 'updated': 'success'}, 200
        else:
            return {'stage': stage, 'updated': 'failed'}, 500
    except Exception as e:
        return {'stage': stage, 'error': str(e)}, 500

def schema_string(columns):
    """Converts the columns that were selected into a hash that can be used to verify that a rule was executed correctly

            Parameters:

                columns (list): The list of columns that was selected from the source system

            Returns:

                column_hash (str): A hash derived from the stringified ordered list
    """
    sorted_columns = sorted(columns)
    sorted_string = "".join(sorted_columns)
    column_hash = sha256(sorted_string.encode()).hexdigest()
    return column_hash