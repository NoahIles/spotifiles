# Dockerfile containing all the customized images for the app  
# Maintainer: Noah Iles 
# A Project inspired by a love for music and a desire to learn more about the world of computer science.

#------------------------------------------------------------------------------

# AN API interface for the app
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim as fast_api
COPY data/app /app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#------------------------------------------------------------------------------

# The MYSQL Database for the app
FROM --platform=linux/x86_64 mysql:8.0.27 as mysql_db
# This is just an initial copy these files are also volume mounted in the compose
COPY --chown=root:root data/myData /myData
# This COPY means you have to rebuild if you modify the initDB.sh file
COPY data/myData/initDB.sh /docker-entrypoint-initdb.d/initDB.sh
RUN chmod +x /docker-entrypoint-initdb.d/initDB.sh
EXPOSE 3306
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#------------------------------------------------------------------------------

# The Pretty interface for the app
FROM --platform=arm64 nginx:1.21.4-alpine as nginx_alpine
COPY --chown=nginx:nginx data/nginx /nginx
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
#TODO: Work on the pretty interface
