import argparse
import logging
from datetime import datetime, timedelta
from pymongo import MongoClient
from requests.structures import CaseInsensitiveDict
import gspread
from oauth2client.service_account import ServiceAccountCredentials

url = "http://mobile.njit.edu/parking/data.php"

# >>> Headers
headers = CaseInsensitiveDict()
headers["Connection"] = "keep-alive"
headers["Accept"] = "application/json, text/plain, */*"
headers["DNT"] = "1"
headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
headers["Content-Type"] = "application/json;charset=UTF-8"
headers["Origin"] = "http://mobile.njit.edu"
headers["Referer"] = "http://mobile.njit.edu/parking/"
headers["Accept-Language"] = "en-US,en;q=0.9,es-419;q=0.8,es;q=0.7"
headers["sec-gpc"] = "1"
headers["Cookie"] = (
    "PHPSESSID=5dc5e83dc26cf12db537bb612bf71ee9")
# <<< Headers

# >>> argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=int, action="store",
                    default=1, dest="verbosity",
                    help=("Set logging verbosity: "
                          "-1=quiet, 0=fatal, 1=error (default), 2=warn, "
                          "3=info, 4=debug"))
parser.add_argument("-d", "--duration-days", type=int, action="store",
                    default=0, dest="duration_days",
                    help=("Set duration in days. A nonpositive "
                          "value runs the script indefinitely.\n"
                          "Default: 0 (runs indefinitely).\n"
                          "See also --duration-minutes"))
parser.add_argument("--duration-minutes", type=int, action="store",
                    default=None, dest="duration_minutes",
                    help=("Set duration in minutes (Usually used for debugging). "
                          "Overrides --duration-days.\n"
                          "Default: None.\n"
                          "See also --duration-minutes"))
args = parser.parse_args()
# <<< argparse

# >>> logging
LOG_LEVELS = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO,
              logging.DEBUG]
verbosity = args.verbosity

if verbosity >= 0:
    basic_logging_level = LOG_LEVELS[verbosity]
else:
    # "verbosity=-1" can be used to disable all logging, so configure
    # logging accordingly.
    basic_logging_level = logging.CRITICAL + 1

logger = logging.getLogger()
logger.setLevel(basic_logging_level)
fmt = "%(asctime)s %(levelname)s:%(name)s %(message)s"
logging.basicConfig(level=basic_logging_level, format=fmt)
# <<< logging

# >>> duration >>>
# Set the duration for the script to run for, from command line arguments.
# NOTE: duration_mintues takes precedence over duration_days.
script_duration = timedelta(days=args.duration_days)
if args.duration_days <= 0:
    script_duration = timedelta(weeks=5*52)
if args.duration_minutes:
    script_duration = timedelta(minutes=args.duration_minutes)
# <<< duration <<<

# >>> MongoDB Database
client = MongoClient("mongodb://localhost")
db = client.NJIT_Parking
# <<< MongoDB Database

# >>> Google Sheets API >>>
gc = gspread.service_account()
gfile = gc.open("njit_parking_gsheet")
# <<< Google Sheets API <<<
