import json
import re
import requests
import time
import logging
from datetime import datetime, timedelta
from http.cookies import SimpleCookie
from pprint import pformat, pprint
from setup import args, db, headers, logger, url, gfile

# Keep only 'SiteName', 'Available', 'Occupied'
extraneous_columns = ["EngineName", "Description", "Total",
                      "Name", "Address", "AddressURL", "type"]

def refresh_headers():
    # Get freshest ID
    with open("NJIT_PARKING_PHPSESSID", "r") as f:
        fresh_id = f.read()

    # Raw string to dict
    cookies = headers["Cookie"].split(";")
    if "" in cookies:
        cookies.remove("")
    cookies = {c.split("=")[0]: c.split("=")[1] for c in cookies}

    # Edit PHPSESSID in-place
    cookies["PHPSESSID"] = fresh_id

    # Rebuild into one long string
    full = ""
    for c, val in cookies.items():
        full += f"{c}={val};" 

    headers["Cookie"] = full
    logging.info(f"Refreshed headers to: {json.dumps(dict(headers), indent=2)}")

def get_deck_info(log=False):
    try:
        logging.info(f"Reaching {url}...")
        resp = requests.post(url, headers=headers)
        if resp.status_code != 200:
            raise ConnectionError
        data = resp.json().get("decks")
        logging.info(f"Status: {resp.status_code}")
        logging.info(f"Received:\n{json.dumps(data, indent=2)}")
    except ConnectionError as e:
        refresh_headers()
        err = f"Unable to complete request to {url}. {e}"
        logging.error(err)
        return {"Error": err}
    return data

def input_record(df, timestamp):
    collection = db[df['SiteName']]
    logging.info(f"Inserting into {collection}:\n {json.dumps(df, indent=2)}")
    df["datetime"] = timestamp
    collection.insert_one(df)

def get_curr_sheet(timestamp):
    sheets = gfile.worksheets()
    sheet_titles = [sheet.title for sheet in sheets]
    today = timestamp.strftime("%Y_%m_%d")
    if today not in sheet_titles:
        gfile.add_worksheet(title=today, rows=1450, cols=5)
        gfile.append_row("timestamp", "Available", "Occupied", "SiteName")
    return gfile.worksheet(today)

def prepare_payload(json_data, timestamp):
    for col in extraneous_columns:
        json_data.pop(col, None)  # remove extraneous columns
    
    fmt_time = timestamp.strftime("%H:%M")
    available = json_data["Available"]
    occupied = json_data["Occupied"]
    site_name = json_data["SiteName"]
    payload = [fmt_time, available, occupied, site_name]
    return payload

def input_gsheet(json_data, timestamp):
    # Collect gsheet
    curr_sheet = get_curr_sheet(timestamp)
    payload = prepare_payload(json_data, timestamp)
    logging.info(f"Inserting into {timestamp.strftime('%Y_%m_%d')}:\n {payload}")
    curr_sheet.append_row(payload)

def main():
    duration = timedelta(days=30)
    start_time = datetime.now()
    end_time = datetime.now() + duration
    now = datetime.now()
    error_count = 0
    while now < end_time or error_count < 5:
        try: 
            data = get_deck_info()
            if "Error" in data:
                error_count += 1
                continue
            for _, json_data in data.items():
                input_gsheet(json_data, now)
            now = datetime.now()
            time.sleep(60)
        except Exception as e:
            continue

if __name__=="__main__":
    main()
