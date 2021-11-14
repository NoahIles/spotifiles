#! /bin/bash
# Sets up Tweet Data Database
mysql -uroot -pexample --local-infile=1 < /myData/my-data.sql