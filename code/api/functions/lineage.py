import json
import requests
from datetime import datetime




body = {'rule_id': 123, 'serums_id': 123, 'hospital_ids': ['ZMC', 'FCRB']}


def create_record_on_blockchain(body, jwt):
    headers = {
        "Authorization": "Bearer {}".format(jwt),
        "Accept: application/json",
        "Content-Type": "application/json"
    }

    data = {
        'ruleId': body['rule_id'],
        'serumsId': body['serums_id'],
        'hospitalIds': body['hospital_ids'],
        'date': str(datetime.today())
    }

    url = "localhost:30001/api/proof"

    response = requests.request("POST", url, headers=headers, data=data)
    if response.status_code == 200:
        return {"status_code": response.status_code, "body": response.json()}
    else:
        return {"status_code": response.status_code, "body": response.text}




    print(data)

create_record_on_blockchain(body)