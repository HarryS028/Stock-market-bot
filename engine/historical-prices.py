import pandas as pd
import numpy as np
import sys,requests
import time
import urllib.parse
import pandas as pd
from pandas.io.json import json_normalize

def log_in(rest_api_key, rest_identifier, rest_password):
    # IG rest API parameters

    rest_url = "https://demo-api.ig.com/gateway/deal/session"

    headers = {}
    headers["Content-Type"] = "application/json; charset=UTF-8"
    headers["Accept"] = "application/json; charset=UTF-8"
    headers ["X-IG-API-KEY"] = rest_api_key
    headers ["Version"] = "2"

    request_json = {}
    request_json["identifier"] = rest_identifier
    request_json["password"] = rest_password

    rest_response = requests.request("POST", rest_url, headers=headers, json=request_json)
    if rest_response.status_code != 200:
        print("error", rest_response.status_code, rest_url, rest_response.text)
        sys.exit(0)
        
    # collect params from login response

    xst = rest_response.headers["X-SECURITY-TOKEN"]
    cst = rest_response.headers["CST"]

    # Get accounts list
    headers["X-SECURITY-TOKEN"] = xst
    headers["CST"] = cst
    headers["Version"] = "1"
    accounts = requests.request("GET", "https://demo-api.ig.com/gateway/deal/accounts", headers=headers,\
                                json=request_json)
    if accounts.status_code != 200:
        print("error", accounts.status_code, accounts.text)

    # Check account type is spreadbet, otherwise switch accounts
    if rest_response.json()['accountType'] == 'SPREADBET':
        pass
    else:
        account_json = {}
        account_json["accountId"] = "Hidden"
        switch_response = requests.request("PUT", "https://demo-api.ig.com/gateway/deal/session/", headers=headers,\
                                    json=account_json)
        if switch_response.status_code != 200:
            print("error", switch_response.status_code, switch_response.text)
    
    return headers

def get_data(headers, start_date, end_date, resolution, epic):
    ### Use this code to download historical data ###
    headers["Version"] = "2"

    # S&P 500 = "IX.D.SPTRD.DAILY.IP"
    # FTSE 100 = "IX.D.FTSE.DAILY.IP"

    data_url = f"https://demo-api.ig.com/gateway/deal/prices/{epic}/{resolution}/{start_date}/{end_date}"

    historical_data = requests.request("GET", data_url, headers=headers)

    if historical_data.status_code != 200:
        print("error", historical_data.status_code, historical_data.text)

    # Convert historical data to pandas dataframe and export
    t = time.localtime()
    current_time = time.strftime("%M%H%d%m%y", t)
    data = historical_data.json()['prices']

    df = pd.DataFrame.from_dict(json_normalize(data), orient='columns')

    df.to_csv(f'output.csv', encoding="UTF-8")

    return "Data collection is complete."

log_in_head = log_in()
print(get_data(log_in_head, "2020-03-20 02:00:00", "2020-03-20 03:00:00", "MINUTE_5", "IX.D.FTSE.DAILY.IP"))

 
