import requests

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
    url = "https://authentication.serums.cs.st-andrews.ac.uk/ua/create_jwt/"
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

# def validate_jwt(jwt):
#     url = "https://authentication.serums.cs.st-andrews.ac.uk/ua/verify_jwt/"
#     payload = ""
#     headers = {
#         "Authorization": f"Bearer {jwt}",
#         "Content-Type": "application/json"
#     }
#     try:
#         response = requests.request("POST", url, headers=headers, data=payload)
#         if response.status_code == 200:
#             return {"status_code": response.status_code, "body": response.json()}
#         else:
#             return {"status_code": response.status_code, "body": response.text}
#     except Exception as e:
#         print("Failed to make request. Reason: {}​".format(str(e)))