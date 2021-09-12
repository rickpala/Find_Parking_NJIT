import json
import re
import requests
import time
import logging
from datetime import datetime, timedelta
from pprint import pformat, pprint
from setup import args, db, headers, logger, url

def refresh_headers():
    all_cookies = headers["Cookie"]
    fresh_id = ""
    with open("NJIT_PARKING_PHPSESSID", "r") as f:
        fresh_id = f.read()

    for c in all_cookies.split(";"):
        if re.search(c, "PHPSESSID=(.*)"):
            re.sub("PHPSESSID=(.*)", f"PHPSESSID={fresh_id}", all_cookies)

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

def main():
    duration = timedelta(days=7)
    start_time = datetime.now()
    end_time = datetime.now() + duration
    now = datetime.now()
    error_count = 0
    while now < end_time or error_count < 5:
        data = get_deck_info()
        if "Error" in data:
            error_count += 1
            continue
        for idx, val in data.items():
            input_record(val, now)
        now = datetime.now()
        time.sleep(60)

if __name__=="__main__":
    main()
