from commodities_api_utils import read_and_write_json_from_API

COMMODITIES = ["WHEAT", "CORN", "ETHANOL", "BRENTOIL", "NG"]

START_DATE = "2022-01-01"
END_DATE = "2022-04-01"


for commodity in COMMODITIES:
    read_and_write_json_from_API(commodity, START_DATE, END_DATE)
