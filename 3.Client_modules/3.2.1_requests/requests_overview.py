import json
import requests


def main():
    session = requests.Session()
    base_url = "https://httpbin.org"

    query_params = {
        "param1": "foo",
        "param2": "bar"
    }

    headers = {
        "User-Agent": "Chrome",
        "Authorization": "Bearer: ewerewrwer34r",
    }

    payload = {
        "id": 32323,
        "name": "Python"
    }

    with open("text_desc.txt") as text_file:

        files = {
            "text_file": text_file
        }
        try:
            response = session.post(url=base_url + "/post",
                                    params=query_params,
                                    headers=headers,
                                    data=payload,
                                    files=files,
                                    timeout=0.001)

            response_2 = session.get(url=base_url + "/get",
                                     params=query_params,
                                     headers=headers,
                                     timeout=0.00001)
            print(response.status_code)
            print(response.text)
            jsonified_response_2 = json.loads(response_2.text)
            print(jsonified_response_2)
        except requests.exceptions.ConnectTimeout:
            print("Ресурс недоступен")
