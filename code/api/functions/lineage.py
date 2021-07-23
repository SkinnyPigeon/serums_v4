import json
import requests
from datetime import datetime

body = {'rule_id': 123, 'serums_id': 123, 'hospital_ids': ['ZMC', 'FCRB']}

def create_record_on_blockchain(body, jwt):
    headers = {
        'Authorization': 'Bearer {}'.format(jwt),
        'Content-Type': 'application/json'
    }

    data = {
        'ruleId': body['rule_id'],
        'serumsId': body['serums_id'],
        'hospitalIds': body['hospital_ids'],
        'date': str(datetime.today())
    }

    url = 'http://localhost:3000/proof'

    try:
        response = requests.request('POST', url, headers=headers, data=data)
        if response.status_code == 200:
            return {'status_code': response.status_code, 'body': response.json()}
        else:
            return {'status_code': response.status_code, 'body': response.text}
    except Exception as e:
        return {'error': str(e)}

proof_id = create_record_on_blockchain(body, 'jkasjdsajkas')['body']['proofId']
print(proof_id)


def add_update_to_blockchain(proof_id, jwt, body):
    headers = {
        'Authorization': 'Bearer {}'.format(jwt),
        'Content-Type': 'application/json'
    }

    data = {
        'type': body['type'],
        'hospitalId': body['hospital_id'],
        'status': body['status'],
        'content': body['content'],
        'date': str(datetime.today())
    }

    url = 'http://localhost:3000/proof/{}'.format(proof_id)

    try:
        response = requests.request('PATCH', url, headers=headers, data=data)
        if response.status_code == 200:
            return {'status_code': response.status_code, 'body': response.json()}
        else:
            return {'status_code': response.status_code, 'body': response.text}
    except Exception as e:
        return {'error': str(e)}

body = {
    'type': 'data_vault_created',
    'hospital_id': 'zmc',
    'status': 'success',
    'content': {
        'schema': '_abc92039'
    },
    'date': str(datetime.today())
}

print(body)

response = add_update_to_blockchain('abc123', 'this_is_my_jwt', body)
print(response)
