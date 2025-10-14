import requests

url = "http://127.0.0.1:5001/auth/register"  # Cambia al puerto que expusiste
data = {"email": "gatito@example.com", "password": "miau1234"}

r = requests.post(url, json=data)
print("Status code:", r.status_code)

try:
    print("JSON:", r.json())
except Exception:
    print("Response text:", r.text)
