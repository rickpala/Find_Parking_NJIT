#!/bin/bash


usage () {
    # Help message from https://stackoverflow.com/questions/33815600/
    readarray message <<EOF
        : Dumped data on the pi at /home/pi/dev/dump
        : 
        : 1. Grab the Mac's IP Address
        :   ipconfig getifaddr en1  # en0 for WiFI
        : 
        : 2. Send the BSON dump over to the Mac
        :   scp -r /home/pi/dev/dump ricky@<MACBOOK_IP_ADDRESS>:/Users/ricky/dump
        : 
        : 3. Restore the files on the Mac
        :   mongorestore -d parking_backup dump/NJIT_Parking --drop
EOF
        shopt -s extglob
        printf '%s' "${message[@]#+( ): }" # Magical array expansion
        shopt -u extglob
}

mongodump --db=NJIT_Parking --out=/home/pi/dev/dump
usage
