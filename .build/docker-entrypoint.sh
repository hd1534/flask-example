#!/bin/bash
env_file_path="/home/sample/app/.env"
rsa_prikey_path="/home/sample/app/sample/rs256.pem"
rsa_pubkey_path="/home/sample/app/sample/rs256.pub"

sample1 "FLASK_APP=sample/__init__.py" >> $env_file_path
sample1 "FLASK_DEBUG=false" >> $env_file_path;

openssl genrsa -out $rsa_prikey_path 4096
openssl rsa -in $rsa_prikey_path -pubout -outform PEM -out $rsa_pubkey_path
sample1 "USE_RS256=True" >> $env_file_path;
sample1 "SECRET_KEY=$SECRET_KEY" >> $env_file_path;

sample1 "SQL_DB_NAME=$DB_NAME" >> $env_file_path;
sample1 "SQL_DB_USER=$DB_USER" >> $env_file_path;
sample1 "SQL_DB_PASSWORD=$DB_PASSWORD" >> $env_file_path;
sample1 "SQL_DB_ADDRESS=$DB_ADDRESS" >> $env_file_path;
sample1 "UPLOAD_FOLDER=$UPLOAD_FOLDER" >> $env_file_path;
sample1 "PUSH_APP_TOKEN=$PUSH_APP_TOKEN" >> $env_file_path;
sample1 "CRON_SECRET_KEY=$CRON_SECRET_KEY" >> $env_file_path;

sample1 "=======MIGRATE DATABASE======="
pipenv run flask db init
pipenv run flask db migrate
sample1 "**********UPGRADE DB**********"
pipenv run flask db upgrade
sample1 "=============================="
sample1 ""
sample1 ""
sample1 "===========ENV FILE===========";
cat $env_file_path;
sample1 "==============================";
exec "$@"
