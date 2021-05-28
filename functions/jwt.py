import requests


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
        print(response)
        if response.status_code == 200:
            print(
                "SUCCESS. Status code: {} - Result: {}".format(
                    response.status_code,
                    response.json()
                )
            )
        else:
            print(
                "ERROR. Status code: {}​ - Reason: {}​".format(
                    response.status_code,
                    response.text
                )
            )
    except Exception as e:
        print("Failed to make request. Reason: {}​".format(str(e)))