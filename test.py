import requests

url = "http://localhost:8000/api/lv/"

payload = "{\r\n    \"temperature\": \"30.5\",\r\n    \"humidity\": \"86.5\"\r\n}"
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text.encode('utf8'))
