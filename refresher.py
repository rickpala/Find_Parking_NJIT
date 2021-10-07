import requests
import time
import threading
import logging
from os import environ
from requests.structures import CaseInsensitiveDict
from setup import url
from typing import Dict, Optional

# Defaults
def_headers = CaseInsensitiveDict()
def_headers["Connection"] = "keep-alive"
def_headers["Accept"] = "application/json, text/plain, */*"
def_headers["DNT"] = "1"
def_headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
def_headers["Content-Type"] = "application/json;charset=UTF-8"
def_headers["Origin"] = "http://mobile.njit.edu"
def_headers["Referer"] = "http://mobile.njit.edu/parking/"
def_headers["Accept-Language"] = "en-US,en;q=0.9,es-419;q=0.8,es;q=0.7"
def_headers["sec-gpc"] = "1"

refresh_url = "http://mobile.njit.edu/parking"

class Refresher:

    def __init__(self):
        with open("NJIT_PARKING_PHPSESSID") as f:
            id_from_file = f.read()
            logging.info("Initial PHPSESSID:", id_from_file) 
            self._env_id = id_from_file

    def _extract_id_from_headers(self, headers: Dict) -> Optional[str]:
        cookie = headers.get("Set-Cookie")
        key, new_id = None, None
        if cookie is not None:
            full_id = cookie.split(";")[0]  # 0th element is the PHPSESSID=HexID
            key, new_id = full_id.split("=")
        return new_id

    def refresh_id(self) -> str:
        r = requests.get(refresh_url, headers=def_headers)
        new_id = self._extract_id_from_headers(r.headers)
        self.env_id = new_id

    @property
    def env_id(self):
        return self._env_id
    
    @env_id.setter
    def env_id(self, new_id: str):
        logging.info(f"Setting PHPSESSID: {new_id}")
        self._env_id = new_id
        with open("NJIT_PARKING_PHPSESSID", "w") as f:
            f.write(self._env_id)

def main():
    r = Refresher()
    while True:
        r.refresh_id()
        time.sleep(10 * 60) # 10 minutes
        
if __name__ == "__main__":
    t = threading.Thread(target=main)
    t.start()
