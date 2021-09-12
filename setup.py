import argparse
import logging
from pymongo import MongoClient
from requests.structures import CaseInsensitiveDict

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
    "_ga=GA1.2.22165298.1599156809;"
    "__utma=203523791.22165298.1599156809.1599445885.1599445885.1;"
    "_gcl_au=1.1.2099377566.1628959653;"
    "_fbp=fb.1.1628959653672.351302010;"
    "PHPSESSID=5dc5e83dc26cf12db537bb612bf71ee9")
# <<< Headers

# >>> argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose",
    help="Increate output verbosity",
    action='store_true')
args = parser.parse_args()
# <<< argparse

# >>> logging
logger = logging.getLogger()
if args.verbose:
    FORMAT = "%(asctime) %(message)s"
    datefmt = "%m/%d %H:%M"
    logging.basicConfig(level=logging.INFO,
                        format=FORMAT,
                        datefmt=datefmt)
    hdlr = logger.handlers[0]
    fmt = logging.Formatter("[%(levelname)-5s %(asctime)s]: %(message)s",
                            datefmt)
    hdlr.setFormatter(fmt)
    logger.setLevel("INFO")
# <<< logging


# >>> MongoDB Database
client = MongoClient("mongodb://localhost")
db = client.NJIT_Parking
# collection = db.ScienceTest
# collection.insert_one({"x": 1, "y": 2, "z": 3})
# from pprint import pprint
# pprint(collection.find_one({"x": 1}))

# <<< MongoDB Database