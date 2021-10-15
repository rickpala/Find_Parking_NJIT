#!/bin/bash

# Run python app
source ./venv/bin/activate
refresher_pid=`pgrep -f "python3 refresher.py"`
if pgrep -f "python3 refresher.py"; then
    echo "refresher.py already running on ${refresher_pid}"
else
    python3 refresher.py &
fi
python3 main.py -v3 &

wait
python3 mailer.py  # Email me if main.py crashes
