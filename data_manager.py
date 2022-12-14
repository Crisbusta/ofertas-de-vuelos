
import requests
import os
SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/15fa2532238887f9ff79feeef7c23f27/ofertasDeVuelos/prices"
SHEETY_USERS_ENDPOINT = "https://api.sheety.co/15fa2532238887f9ff79feeef7c23f27/ofertasDeVuelos/users"
SHEETY_API_KEY = os.environ.get("SHEETY_API_KEY")
BEARER_TOKEN = f"Bearer {SHEETY_API_KEY}"
BEARER_HEADERS = {
    "Authorization": BEARER_TOKEN
}


class DataManager:
    def __init__(self):
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=BEARER_HEADERS)
        print(response.text)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=BEARER_HEADERS
            )
            print(response.text)

    def get_customer_emails(self):
        customers_endpoint = SHEETY_USERS_ENDPOINT
        response = requests.get(url=customers_endpoint, headers=BEARER_HEADERS)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
