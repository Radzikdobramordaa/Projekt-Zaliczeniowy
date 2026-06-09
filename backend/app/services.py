import requests

NBP_URL = "https://api.nbp.pl/api/exchangerates/tables/A?format=json"


def fetch_rates_from_nbp():
    response = requests.get(NBP_URL)

    if response.status_code != 200:
        raise Exception("NBP API unavailable")

    data = response.json()

    return data[0]