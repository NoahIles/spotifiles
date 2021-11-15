#! /bin/bash
# Sets up Tweet Data Database
mysql -uroot -pexample --local-infile=1 < /myData/my-data.sql
# if /app/models.py does not exist, create it
if [ ! -f /app/models.py ]; then
echo "MODELS WILL NEED TO BE RE-GENERATED!!!"
fi