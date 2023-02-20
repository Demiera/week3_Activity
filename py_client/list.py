import requests
from getpass import getpass

username = input("Username: ")
password = getpass()

auth_endpoint = "http://localhost:8000/api/auth/"

auth_response = requests.post(auth_endpoint, json={'username': username, 'password': password})
print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        "Authorization": f"Bearer {token}"
    }
    endpoint = "http://localhost:8000/api/products/"
    get_response = requests.get(endpoint, headers=headers)
    print(get_response.json())

    data = get_response.json()
    next_url = data['next']
    results = data['results']
    print("next url: ", next_url)
    print(results)
