from data_manager import DataManager
from datetime import datetime, timedelta
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "SCL"

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_destination_data()

if sheet_data[0]["iataCode"] == "":
    city_names = [row["city"] for row in sheet_data]
    data_manager.city_codes = flight_search.get_destination_codes(city_names)
    data_manager.update_destination_codes()
    sheet_data = data_manager.get_destination_data()

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination_code in destinations:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination_code,
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    if flight is None:
        continue

    if flight.price < destinations[destination_code]["price"]:
        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]
        message = f"Oferta de vuelo! Sólo ${round(flight.price):,d} CLP para volar desde {flight.origin_city}-{flight.origin_airport} a {flight.destination_city}-{flight.destination_airport}, desde el {flight.out_date} hasta el {flight.return_date}."
        if flight.stop_overs > 0:
            message += f"\n\nEl vuelo tiene {flight.stop_overs} escalas, en la ruta {flight.via_city}."
        link = f"https://www.google.com/travel/flights?q=Flights%20to%20{flight.destination_airport}%20from%20{flight.origin_airport}%20on%20{flight.out_date}%20through%20{flight.return_date}"

        notification_manager.send_emails(emails, message, link)
