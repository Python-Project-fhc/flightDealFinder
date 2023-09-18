# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

sheet_data_manager = DataManager()
flight_search_data = FlightSearch()
sheet_data = sheet_data_manager.get_data()
email_notif = NotificationManager()

ORIGIN_CITY_IATA = "LON"

for data in sheet_data:
    if data["iataCode"] == "":
        iata_code = flight_search_data.search_iata_code_by_cityName(data["city"])
        data_dict = {
            "price": {
                "city": data["city"],
                "iataCode": iata_code,
                "lowestPrice": data["lowestPrice"]
            }
        }
        sheet_data_manager.update_data(data["id"], data_dict)

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search_data.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    if flight is not None:
        if flight.price < destination["lowestPrice"]:
            email_notif.sendMail(flight)
            if flight.stop_overs > 0:
                print(f"we found cheaper flight to {flight.destination_city} only £{flight.price}\nFlight has "
                      f"{flight.stop_overs} stop over, via {flight.via_city} city.")
            else:
                print(f"we found cheaper flight to {flight.destination_city} only £{flight.price}")
    else:
        continue

