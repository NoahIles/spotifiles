#! /bin/bash
# Sets up MySQL Database
mysql -ubobby -pbobby --local-infile=1 < /myData/my-data.sql
# if /app/models.py does not exist, it needs to be created
if [ ! -f /app/models.py ]; then
    echo "MODELS WILL NEED TO BE RE-GENERATED!!!"
fi