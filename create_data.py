from commodities_api_utils import read_and_write_json_from_API

COMMODITIES = ["WHEAT", "CORN", "BRENTOIL", "NG"]

CURRENCIES = ["RUB", "UAH", "EUR"]

START_DATE = "2022-01-05"
END_DATE = "2022-04-03"

for commodity in COMMODITIES:
    read_and_write_json_from_API(commodity, START_DATE, END_DATE)

for currency in CURRENCIES:
    read_and_write_json_from_API(currency, START_DATE, END_DATE)
