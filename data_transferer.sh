#!/bin/bash

rm ~/dump
mongodump --db=NJIT_Parking --out=~/dump

echo "Dumped files at ~/dump"
echo "On the Pi, run"
echo "    scp -r ~/dump ricky@<MACBOOK_IP_ADDR>:~/dump"

echo "On the Mac, run"
echo "    ipconfig getifaddr en1"
echo "    mongorestore -d parking_backup dump/NJIT_Parking --drop"
