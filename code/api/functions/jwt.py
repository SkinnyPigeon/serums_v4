import requests
import subprocess
from dotenv import load_dotenv
import os
import jwt

project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()
load_dotenv(os.path.join(project_folder, '.env'))
JWT_KEY = os.getenv('JWT_KEY')
if JWT_KEY == None:
    JWT_KEY = os.environ.get('JWT_KEY')

def validate_jwt(encoded_jwt):
    token = encoded_jwt.replace('Bearer ', '')
    try:
        decoded_jwt = jwt.decode(token, JWT_KEY, audience="https://shcs.serums.cs.st-andrews.ac.uk/", algorithms='HS256')
        # print(f"DECODED JWT: {decoded_jwt}")
        if decoded_jwt:
            return {'serums_id': decoded_jwt['userID'], 'hospital_id': decoded_jwt['orgID'], 'groupIDs': decoded_jwt['groupIDs'], 'status_code': 200}
    except jwt.exceptions.InvalidSignatureError as e:
        return {'status_code': 404, 'message': str(e)}
    except jwt.exceptions.DecodeError as d:
        return {'status_code': 422, 'message': str(d)}

def refresh_jwt(hospital):
    """Used in testing to generate a fresh JWT quickly. New JWTs can be selected by logging into the Serums portal, however, they have a finite life on them. Using the refresh tokens limits the need to do the logging in. Calls the authentication module to refresh the token
    
            Parameters:

                hospital (str): The name of the hospital to refresh a jwt for

            Returns:

                response (dict): The response from the authentication module including a refreshed JWT when successful
    
    """

    if hospital == 'fcrb':
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyOTUzNDYyOCwianRpIjoiMDAxMmE5NjAwZjMzNDdlOTk2ZjYzOTQ5YTk4N2U0YzAiLCJ1c2VySUQiOjM3NSwiaXNzIjoiU2VydW1zQXV0aGVudGljYXRpb24iLCJpYXQiOjE2MjY5NDI2MjgsInN1YiI6ImV1YW4yQHRlc3QuY29tIiwiZ3JvdXBJRHMiOlsiTUVESUNBTF9TVEFGRiJdLCJvcmdJRCI6IkZDUkIiLCJhdWQiOiJodHRwczovL3VybGRlZmVuc2UucHJvb2Zwb2ludC5jb20vdjIvdXJsP3U9aHR0cC0zQV9fd3d3LnNlcnVtcy5jb20mZD1Ed0lEYVEmYz1lSUdqc0lUZlhQX3ktRExMWDB1RUhYSnZVOG5PSHJVSzhJcndOS090a1ZVJnI9dVRmTjV1UTFraHdiUnlfVGdLSDZhVWQwLUJibTBHOEstVmFqa3pabXk5OCZtPTJpVU5uMjlGU2FmNy0wM3h1OXhNQnJjbjR0NlVfM3czdXFMaUx5dFRmVDQmcz01akIyam1xaHNOQV9nMVNWeVpnVUZSRjlvRVA4X0FRYS1saWNZVzNJdWZ3JmU9In0.tYBCaritki7Tn9tqmQatcDvkPUCmsTs8Yf3xK3H9Dp0"
    elif hospital == 'ustan':
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyOTQ1ODQzNywianRpIjoiNjUyOTU0NTc2NTVmNDVlYmEwZTc1YzY5NzVlZDlkMWIiLCJ1c2VySUQiOjM2NCwiaXNzIjoiU2VydW1zQXV0aGVudGljYXRpb24iLCJpYXQiOjE2MjY4NjY0MzcsInN1YiI6ImV1YW5AdGVzdC5jb20iLCJncm91cElEcyI6WyJQQVRJRU5UIl0sIm9yZ0lEIjoiVVNUQU4iLCJhdWQiOiJodHRwczovL3VybGRlZmVuc2UucHJvb2Zwb2ludC5jb20vdjIvdXJsP3U9aHR0cC0zQV9fd3d3LnNlcnVtcy5jb20mZD1Ed0lEYVEmYz1lSUdqc0lUZlhQX3ktRExMWDB1RUhYSnZVOG5PSHJVSzhJcndOS090a1ZVJnI9dVRmTjV1UTFraHdiUnlfVGdLSDZhVWQwLUJibTBHOEstVmFqa3pabXk5OCZtPTJpVU5uMjlGU2FmNy0wM3h1OXhNQnJjbjR0NlVfM3czdXFMaUx5dFRmVDQmcz01akIyam1xaHNOQV9nMVNWeVpnVUZSRjlvRVA4X0FRYS1saWNZVzNJdWZ3JmU9In0.lyKHDBYsQoz2YjFAVlJHpMZeotcVM2xr7ohluiVxwiM"
    elif hospital == 'zmc':
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyOTUzNDg3NSwianRpIjoiZjdiM2MzMTZjNjgyNDU2NDkyZDIyMDk4MDczZjY2MmYiLCJ1c2VySUQiOjM3NiwiaXNzIjoiU2VydW1zQXV0aGVudGljYXRpb24iLCJpYXQiOjE2MjY5NDI4NzUsInN1YiI6ImV1YW4zQHRlc3QuY29tIiwiZ3JvdXBJRHMiOlsiTUVESUNBTF9TVEFGRiJdLCJvcmdJRCI6IlpNQyIsImF1ZCI6Imh0dHBzOi8vdXJsZGVmZW5zZS5wcm9vZnBvaW50LmNvbS92Mi91cmw_dT1odHRwLTNBX193d3cuc2VydW1zLmNvbSZkPUR3SURhUSZjPWVJR2pzSVRmWFBfeS1ETExYMHVFSFhKdlU4bk9IclVLOElyd05LT3RrVlUmcj11VGZONXVRMWtod2JSeV9UZ0tINmFVZDAtQmJtMEc4Sy1WYWprelpteTk4Jm09MmlVTm4yOUZTYWY3LTAzeHU5eE1CcmNuNHQ2VV8zdzN1cUxpTHl0VGZUNCZzPTVqQjJqbXFoc05BX2cxU1Z5WmdVRlJGOW9FUDhfQVFhLWxpY1lXM0l1ZncmZT0ifQ.2g9wRnPgdxy9DPM7AAQFWQEN_aVoUjpYb1-zSpSXW4g"
    
    url = "https://authentication.serums.cs.st-andrews.ac.uk/ua/refresh_jwt/"
    payload = '{{"refresh": "{}"}}'.format(token)
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


def validate_jwt_legacy(jwt):
    """Calls the authentication module to validate a JWT included in the header of the request
    
            Parameters:

                jwt (str): A JWT that is generated upon login to the Serums frontend

            Returns:

                response (dict): A response object from the authentication module that dictates whether or not a JWT is valid
    
    """
    url = "https://authentication.serums.cs.st-andrews.ac.uk/ua/verify_jwt/"
    payload = ""
    headers = {
        "Authorization": f"{jwt}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            return {"status_code": response.status_code, "body": response.json()}
        else:
            return {"status_code": response.status_code, "body": response.text}
    except Exception as e:
        print("Failed to make request. Reason: {}​".format(str(e)))