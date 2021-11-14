FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim as fast_api
COPY data/app /app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
ENV DATABASE_URL=mysql://root:example@db:3306/db1

# --platform=amd64/linux
FROM --platform=linux/x86_64 mysql:8.0.27 as mysql_db
COPY --chown=root:root data/myData /myData
ENV MYSQL_ROOT_PASSWORD=example
ENV MYSQL_DATABASE=db1
ENV MYSQL_USER=bobby
ENV MYSQL_PASSWORD=bobby
COPY data/myData/initDB.sh /docker-entrypoint-initdb.d/initDB.sh
RUN chmod +x /docker-entrypoint-initdb.d/initDB.sh
EXPOSE 3306
# CMD --default-authentication-plugin=mysql_native_password
# RUN mysql -u root -e "set local_infile = 'ON';"
# RUN mysql --local-infile -u root < /myData/my-data.sql

FROM --platform=arm64 nginx:1.21.4-alpine as nginx_alpine
COPY --chown=nginx:nginx data/nginx /nginx
