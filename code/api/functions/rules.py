import requests
from functions.departments import get_department_of_staff_member
from functions.jwt import validate_jwt

def get_rules(jwt, grantor_id, grantee_id):
    url = 'http://localhost:30001/v1/api/getRules'
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json"
    }
    data = {
        "filters": [
            {
                "filterType": "SIMPLE",
                "key": "grantor.id",
                "value": grantor_id
            },
            {
                "filterType": "NOT_EXPIRED"
            },
            {
                "filterType": "SIMPLE",
                "key": "grantee.id",
                "value": grantee_id
            }

        ]
    }
    response = requests.request('POST', url, headers=headers, json=data)
    return response.json()

def sum_up_rules(rules):
    allow_tags = set()
    deny_tags = set()
    for rule in rules:
        print(rule)
        for tag in rule['access']:
            if rule['action'] == 'ALLOW':
                allow_tags.add(tag['name'])
            if rule['action'] == 'DENY':
                deny_tags.add(tag['name'])

    results = allow_tags ^ deny_tags
    return list(results)


def validate_doctor(group_ids):
    if 'MEDICAL_STAFF' in group_ids:
        return True
    else:
        return False

def validate_admin(group_ids):
    if 'MEDICAL_ADMIN' in group_ids:
        return True
    else:
        return False

def validate_patient(group_ids):
    if 'PATIENT' in group_ids:
        return True
    else:
        return False


def get_rules_for_doctor(jwt, grantor_id, serums_and_department_ids):
    response = []
    url = 'http://localhost:30001/v1/api/getRules'
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json"
    }
    for id in serums_and_department_ids:
        data = {
            "filters": [
                {
                    "filterType": "SIMPLE",
                    "key": "grantor.id",
                    "value": grantor_id
                },
                {
                    "filterType": "NOT_EXPIRED"
                },
                {
                    "filterType": "SIMPLE",
                    "key": "grantee.id",
                    "value": serums_and_department_ids[id]
                }

            ]
        }
        rule_response = requests.request('POST', url, headers=headers, json=data)
        response.extend(rule_response.json())
    return response


def validate_rules(jwt, body):
    tags = []
    jwt_response = validate_jwt(jwt)
    requestor_type = jwt_response['body']['groupIDs']
    if validate_patient(requestor_type):
        print('PATIENT')
        if jwt_response['status_code'] == 200:
            if body['serums_id'] == jwt_response['body']['userID']:
                tags = ['all']
    elif validate_doctor(requestor_type):
        print('DOCTOR')
        serums_and_department_ids = get_department_of_staff_member(jwt)
        rules = get_rules_for_doctor(jwt, body['serums_id'], serums_and_department_ids)
        tags = sum_up_rules(rules)
    return tags

# tags = validate_rules(jwt, body)
# print(tags)