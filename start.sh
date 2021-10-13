#!/bin/bash

# Init mongo
sudo systemctl enable mongodb
sudo systemctl start mongodb

# Run python app
source ./venv/bin/activate
# python3 refresher.py &
python3 main.py -v3 &
wait
python3 mailer.py
