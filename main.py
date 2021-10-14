import json
import requests
import time
import logging
from datetime import datetime, timedelta
from pprint import pformat, pprint
from setup import args, db, headers, logger, url, gfile, script_duration
from typing import List, Dict

class Headers:
    def __init__(self, headers):
        self.headers = headers

    def refresh_headers(self):
        """Updates current PHPSESSID with the one in file NJIT_PARKING_PHPSESSID."""
        with open("NJIT_PARKING_PHPSESSID", "r") as f:
            fresh_id = f.read()

        # Raw string of cookies to usable dict
        cookies = self.headers["Cookie"].split(";")
        if "" in cookies:
            cookies.remove("")
        cookies = {c.split("=")[0]: c.split("=")[1] for c in cookies}
        cookies["PHPSESSID"] = fresh_id

        # Rebuild into one long string
        full = ""
        for c, val in cookies.items():
            full += f"{c}={val};" 

        self.headers["Cookie"] = full
        logging.info(f"Refreshed headers to: {json.dumps(dict(self.headers), indent=2)}")

class DataHandler:
    """Responsible for retrieving, cleaning, and inserting data for NJIT Parking."""
    SITENAME_TRANSLATOR = {"PARK": "PARK", "Science & Tech Garage": "TECH",
                           "FENS1": "FENS1", "FENS2": "FENS2",
                           "Lot 10": "LOT10"}
    DECKS = {"TECH": "0", "PARK": "1", "LOT10": "2", "FENS1": "3", "FENS2": "4"}
    def __init__(self):
        self.headers = Headers(headers)
        self.gfile = gfile
        self._ensure_sheet_is_uptodate() 

    def get_deck_info(self):
        """Gets the parking data and returns a list of the availability of each deck."""
        for _ in range(3):  # Retry up to 3 times
            try:
                # Reach http://mobile.njit.edu/parking/data.php
                logging.info(f"Reaching {url}...")
                resp = requests.post(url, headers=headers)
                logging.info(f"Status: {resp.status_code}")
                if resp.status_code != 200:
                    raise ConnectionError

                # Clean data
                resp_json = resp.json().get("decks")
                data = self._parse_response(resp_json)

            except ConnectionError as e:
                logging.error(f"[DataHandler.get_deck_info] Unable to connect. Trying again...")
                logging.error(e)
                self.headers.refresh_headers()
            else:
                return data  # executed succesfully; no need to retry

    def _parse_response(self, resp):
        """
        Returns the flattened response containing the *availability* of each deck.
        
        The structure of the response will be in the order:
        [timestamp (HH:MM), TECH, PARK, LOT10, FENS1, FENS2]
        """
        logging.info(f"Raw JSON:\n{json.dumps(resp, indent=2)}")

        now = datetime.now()
        now = now.strftime("%H:%M")
        rv = [now]
        for _, deck in self.DECKS.items():
            data = resp[deck]
            availablility = int(data["Available"])
            rv.append(availablility)

        logging.info(f"Flattened to: {rv}")
        return rv

    def _ensure_sheet_is_uptodate(self):
        """Updates self.curr_sheet if no sheet exists yet for today. Otherwise return the current sheet"""
        sheets = self.gfile.worksheets()
        sheet_titles = [sheet.title for sheet in sheets]
        today = datetime.now().strftime("%Y_%m_%d")
        if today not in sheet_titles:
            logging.info(f"[DataHandler._get_and_set_curr_sheet] Creating new sheet: {today}")
            new_sheet = self.gfile.add_worksheet(title=today, rows=1450, cols=5)
            new_sheet.append_row(["timestamp", "TECH", "PARK", "LOT10", "FENS1", "FENS2"]) 
            self.curr_sheet = new_sheet  # Update for today's sheet
        else:
            self.curr_sheet = self.gfile.worksheet(today)

    def insert_to_gsheet(self, payload):
        logging.info(f"Appending row: {payload}")
        self._ensure_sheet_is_uptodate() 
        self.curr_sheet.append_row(payload)

if __name__=="__main__":
    end_time = datetime.now() + script_duration
    dh = DataHandler()
    while datetime.now() < end_time:
        try:
            data = dh.get_deck_info()
            dh.insert_to_gsheet(data) 
            time.sleep(60)
        except Exception as e:
            logger.error(f"[main]: {e}")
