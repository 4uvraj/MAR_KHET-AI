import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_mandi_data(
    commodity=None,
    state=None,
    district=None,
    limit=100,
    offset=0
):

    url = "https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24?api-key=579b464db66ec23bdd0000013502eb6c09c24b996e51713e800d7d46&format=json&offset=10&limit=1000"

    params = {
        "api-key": '579b464db66ec23bdd0000013502eb6c09c24b996e51713e800d7d46',
        "format": "json",
        "limit": limit,
        "offset": offset
    }

    if commodity:
        params["filters[Commodity]"] = commodity

    if state:
        params["filters[State]"] = state

    if district:
        params["filters[District]"] = district

    response = requests.get(url, params=params, timeout=20)

    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}")

    data = response.json()

    return data.get("records", [])
