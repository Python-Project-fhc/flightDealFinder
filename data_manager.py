import requests
import os
from requests.auth import HTTPBasicAuth


class DataManager:

    def __init__(self):
        self.api_endpoint = os.environ.get("SHEETY_GET_ENDPOINT")
        self.auth = HTTPBasicAuth(os.environ.get("SHEETY_USER"), os.environ.get("SHEETY_PASS"))

    def get_data(self):
        response = requests.get(url=self.api_endpoint, auth=self.auth)
        response.raise_for_status()
        return response.json()["prices"]

    def update_data(self, data_id, data_dict):
        update_endpoint = f"{self.api_endpoint}/{data_id}"
        response = requests.put(url=update_endpoint, json=data_dict, auth=self.auth)
        response.raise_for_status()
        return response.json()
