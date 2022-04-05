
import os
import requests
import json
import pandas as pd

COMMODITIES_ACCESS_KEY = os.getenv("COMMODITIES_ACCESS_KEY")


def get_commodity_data(parameter, start_date, end_date):
    """
    read in data from commodities-api.com
    """
        base_url = "https://commodities-api.com/api/timeseries?"
        access_key = f"access_key={COMMODITIES_ACCESS_KEY}"
        date = f"&start_date={start_date}&end_date={end_date}"
        base_parameter = f"&base=USD&symbols={parameter}"
        endpoint = f"{base_url}{access_key}{date}{base_parameter}"
        response = requests.get(endpoint)
        data_json = json.loads(response.text)
        return data_json


def read_and_write_json_from_API(parameter, start_date, end_date):
    """
    read in data from commodities-api.com and write file (to minimise use of free API requests)
    """
    commodity_json = get_commodity_data(parameter, start_date, end_date)
    commodity_json_string = json.dumps(commodity_json)
    file_name = f"{parameter}_timeseries.json"
    jsonFile = open(file_name, "w")
    jsonFile.write(commodity_json_string)
    jsonFile.close()


def process_saved_api_data(parameter):
    """
    turn API data into useable pandas dataframe
    """
    file_name = f"{parameter}_timeseries.json"
    f = open(file_name)
    data = json.load(f)
    dates = []
    for i in data['data']['rates']:
        dates.append(i)
    commodity_values = []
    for j in dates:
        day_dict = data['data']['rates'][j]
        value = day_dict.get(parameter)
        commodity_values.append(value)
    df = pd.DataFrame({"date":dates, "commodity values": commodity_values})
    return df



 



