import requests

{'token': '4b5c72c9d3bc9997fd823b90c8fe993995efdf36'}

endpoint = "http://localhost:8000/api/products/"
data = {"title": 'this is great'}
headers = {
    'Authorization': 'Bearer 4b5c72c9d3bc9997fd823b90c8fe993995efdf36'
}
get_response = requests.post(endpoint, json=data, headers=headers)

print(get_response.json())