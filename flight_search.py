import requests
import os
from flight_data import FlightData

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.TEQUILA_LOC_API_QUERY = "https://api.tequila.kiwi.com/locations/query"
        self.TEQUILA_SEARCH_API = "https://api.tequila.kiwi.com/v2/search"
        self.headers = {
            "apikey": os.environ.get("TEQUILA_API_KEY")
        }

    def search_iata_code_by_cityName(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city",
            "limit": 1,
            "active_only": True
        }
        response = requests.get(url=self.TEQUILA_LOC_API_QUERY, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()["locations"][0]["code"]

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        params = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        response = requests.get(url=f"{self.TEQUILA_SEARCH_API}", headers=self.headers, params=params)
        response.raise_for_status()
        try:
            data = response.json()["data"][0]
        except KeyError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data
