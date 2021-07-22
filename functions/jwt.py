import requests
import json

def refresh_jwt():
    ustan_refresh = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyOTQ1ODQzNywianRpIjoiNjUyOTU0NTc2NTVmNDVlYmEwZTc1YzY5NzVlZDlkMWIiLCJ1c2VySUQiOjM2NCwiaXNzIjoiU2VydW1zQXV0aGVudGljYXRpb24iLCJpYXQiOjE2MjY4NjY0MzcsInN1YiI6ImV1YW5AdGVzdC5jb20iLCJncm91cElEcyI6WyJQQVRJRU5UIl0sIm9yZ0lEIjoiVVNUQU4iLCJhdWQiOiJodHRwczovL3VybGRlZmVuc2UucHJvb2Zwb2ludC5jb20vdjIvdXJsP3U9aHR0cC0zQV9fd3d3LnNlcnVtcy5jb20mZD1Ed0lEYVEmYz1lSUdqc0lUZlhQX3ktRExMWDB1RUhYSnZVOG5PSHJVSzhJcndOS090a1ZVJnI9dVRmTjV1UTFraHdiUnlfVGdLSDZhVWQwLUJibTBHOEstVmFqa3pabXk5OCZtPTJpVU5uMjlGU2FmNy0wM3h1OXhNQnJjbjR0NlVfM3czdXFMaUx5dFRmVDQmcz01akIyam1xaHNOQV9nMVNWeVpnVUZSRjlvRVA4X0FRYS1saWNZVzNJdWZ3JmU9In0.lyKHDBYsQoz2YjFAVlJHpMZeotcVM2xr7ohluiVxwiM"
    fcrb_refresh = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyOTUzNDYyOCwianRpIjoiMDAxMmE5NjAwZjMzNDdlOTk2ZjYzOTQ5YTk4N2U0YzAiLCJ1c2VySUQiOjM3NSwiaXNzIjoiU2VydW1zQXV0aGVudGljYXRpb24iLCJpYXQiOjE2MjY5NDI2MjgsInN1YiI6ImV1YW4yQHRlc3QuY29tIiwiZ3JvdXBJRHMiOlsiTUVESUNBTF9TVEFGRiJdLCJvcmdJRCI6IkZDUkIiLCJhdWQiOiJodHRwczovL3VybGRlZmVuc2UucHJvb2Zwb2ludC5jb20vdjIvdXJsP3U9aHR0cC0zQV9fd3d3LnNlcnVtcy5jb20mZD1Ed0lEYVEmYz1lSUdqc0lUZlhQX3ktRExMWDB1RUhYSnZVOG5PSHJVSzhJcndOS090a1ZVJnI9dVRmTjV1UTFraHdiUnlfVGdLSDZhVWQwLUJibTBHOEstVmFqa3pabXk5OCZtPTJpVU5uMjlGU2FmNy0wM3h1OXhNQnJjbjR0NlVfM3czdXFMaUx5dFRmVDQmcz01akIyam1xaHNOQV9nMVNWeVpnVUZSRjlvRVA4X0FRYS1saWNZVzNJdWZ3JmU9In0.tYBCaritki7Tn9tqmQatcDvkPUCmsTs8Yf3xK3H9Dp0"
    zmc_refresh = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyOTUzNDg3NSwianRpIjoiZjdiM2MzMTZjNjgyNDU2NDkyZDIyMDk4MDczZjY2MmYiLCJ1c2VySUQiOjM3NiwiaXNzIjoiU2VydW1zQXV0aGVudGljYXRpb24iLCJpYXQiOjE2MjY5NDI4NzUsInN1YiI6ImV1YW4zQHRlc3QuY29tIiwiZ3JvdXBJRHMiOlsiTUVESUNBTF9TVEFGRiJdLCJvcmdJRCI6IlpNQyIsImF1ZCI6Imh0dHBzOi8vdXJsZGVmZW5zZS5wcm9vZnBvaW50LmNvbS92Mi91cmw_dT1odHRwLTNBX193d3cuc2VydW1zLmNvbSZkPUR3SURhUSZjPWVJR2pzSVRmWFBfeS1ETExYMHVFSFhKdlU4bk9IclVLOElyd05LT3RrVlUmcj11VGZONXVRMWtod2JSeV9UZ0tINmFVZDAtQmJtMEc4Sy1WYWprelpteTk4Jm09MmlVTm4yOUZTYWY3LTAzeHU5eE1CcmNuNHQ2VV8zdzN1cUxpTHl0VGZUNCZzPTVqQjJqbXFoc05BX2cxU1Z5WmdVRlJGOW9FUDhfQVFhLWxpY1lXM0l1ZncmZT0ifQ.2g9wRnPgdxy9DPM7AAQFWQEN_aVoUjpYb1-zSpSXW4g"
    url = "https://authentication.serums.cs.st-andrews.ac.uk/ua/refresh_jwt/"
    payload = '{{"refresh": "{}"}}'.format(zmc_refresh)
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
    payload = ""
    headers = {
        "Authorization": "Bearer {}".format(jwt),
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