import requests


endpoint = "http://localhost:8000/api/products/1/update/"
data = {
    'title': 'hello world',
    'price': 00.00
        }

get_response = requests.put(endpoint, json=data)

print(get_response.json())