import os
import requests
from dotenv import load_dotenv

load_dotenv()

url_access = os.getenv('URL_ACCESS')

payload = {
    'scope': os.getenv('SCOPE')
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': os.getenv("RQUID"),
    'Authorization': os.getenv("AUTH")
}

response = requests.post(url_access, headers=headers, data=payload, verify=False)

print(response.text)