from data_api import fetch_mandi_data
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DATA_GOV_API_KEY")

url = "https://api.data.gov.in/resource/35985678-d079-46b4-9ed6-6f13308a1d24"

params = {
    "api-key": API_KEY,
    "format": "json",
    "limit": 5
}

res = requests.get(url, params=params)

print(res.json())
