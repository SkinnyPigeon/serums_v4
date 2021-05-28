import requests
import json

def refresh_jwt():
    refresh_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyNDc4NzcyOCwianRpIjoiYjk1ZGI4OGI0ZGRlNGJkMTk3ZjRmZGY3NTY3ZTgyMzUiLCJ1c2VySUQiOjM2NCwiaXNzIjoiU2VydW1zQXV0aGVudGljYXRpb24iLCJpYXQiOjE2MjIxOTU3MjgsInN1YiI6ImV1YW5AdGVzdC5jb20iLCJncm91cElEcyI6WyJQQVRJRU5UIl0sIm9yZ0lEIjoiVVNUQU4iLCJhdWQiOiJodHRwczovL3VybGRlZmVuc2UucHJvb2Zwb2ludC5jb20vdjIvdXJsP3U9aHR0cC0zQV9fd3d3LnNlcnVtcy5jb20mZD1Ed0lEYVEmYz1lSUdqc0lUZlhQX3ktRExMWDB1RUhYSnZVOG5PSHJVSzhJcndOS090a1ZVJnI9dVRmTjV1UTFraHdiUnlfVGdLSDZhVWQwLUJibTBHOEstVmFqa3pabXk5OCZtPTJpVU5uMjlGU2FmNy0wM3h1OXhNQnJjbjR0NlVfM3czdXFMaUx5dFRmVDQmcz01akIyam1xaHNOQV9nMVNWeVpnVUZSRjlvRVA4X0FRYS1saWNZVzNJdWZ3JmU9In0.EDlHovqYw5pDprTZOlMgdJmrerz4mX3vAMsT99KtBWo"
    url = "https://authentication.serums.cs.st-andrews.ac.uk/ua/refresh_jwt/"
    payload = '{{"refresh": "{}"}}'.format(refresh_jwt)
    print(payload)
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 201:
            return {"status_code": response.status_code, "body": response.json()}
        else:
            return {"status_code": response.status_code, "body": response.text}
    except Exception as e:
        print("Failed to make request. Reason: {}​".format(str(e)))


def validate_jwt(jwt):
    url = "https://authentication.serums.cs.st-andrews.ac.uk/ua/verify_jwt/"
    # url = "https://localhost:9000/ua/verify_jwt/"
    '''
    You might as well use the following url since apps can see each other on Fracas:
    url = "https://localhost:9000/ua/verify_jwt/"
    '''
    payload = ""

    headers = {
        "Authorization": "Bearer {}".format(jwt),
        "Content-Type": "application/json"
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            # print(
            #     "SUCCESS. Status code: {} - Result: {}".format(
            #         response.status_code,
            #         response.json()
            #     )
            # )
            return {"status_code": response.status_code, "body": response.json()}
        else:
            # print(
            #     "ERROR. Status code: {}​ - Reason: {}​".format(
            #         response.status_code,
            #         response.text
            #     )
            # )
            return {"status_code": response.status_code, "body": response.text}
    except Exception as e:
        print("Failed to make request. Reason: {}​".format(str(e)))