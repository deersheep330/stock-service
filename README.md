# stock-service [![CircleCI](https://circleci.com/gh/deersheep330/stock-service.svg?style=shield)](https://app.circleci.com/pipelines/github/deersheep330/stock-service)

#### local run

(1) setup python
```
sudo apt install python-is-python3
```

(2) setup venv
```
python -m venv .
source bin/activate
```

(3) install dependencies
```
pip install -r requirements.txt
```

(4) setup test database
```
docker run -it --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_DATABASE=mydb -d -t mysql:8.0.23
# db connection url = root:admin@127.0.0.1:3306/mydb
./wait-for-it.sh localhost:3306
```

(5) setup adminer for test database
```
docker run --name adminer --link mysql:mydb -p 7890:8080 -d adminer
# can login to adminer console only after mysql initialized
```

(6) export db host and db connection url
```
export DB_HOST="$(hostname -I | tr -d "[:blank:]"):3306"
export DB_CONNECTION_URL="root:admin@${DB_HOST}/mydb"
export REDIS_HOST="$(hostname -I | tr -d "[:blank:]")"
```

(7) run the application with docker
```
# collect stock symbols
python symbol_entry.py

# collect ptt trend
python ptt_trend_entry.py
# if encounter [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate is not yet valid
# exec sudo ntpdate ntp.ubuntu.com

# collect reunion trend
python reunion_entry.py

# collect institutions overbought / oversold
python institutions_entry.py

# collect prices
python close_price_entry.py
python open_price_entry.py

# collect quote when market open
python quote_entry.py
# if quote_entry.py quits early, check system time by exec: date
# if system time is wrong, exec:
# sudo apt-get install ntp
# sudo apt-get install ntpdate
# sudo ntpdate ntp.ubuntu.com

# fastapi
uvicorn fastapi_entry:app --reload
gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --access-logfile /proc/1/fd/1 fastapi_entry:app -D

# setup alembic
(1) alembic init alembic
(2) modify sqlalchemy.url in alembic.ini
(3) modify target_metadata in alembic/env.py
(4) alembic revision --autogenerate
(5) review changes in revisions/
(6) alembic history --verbose
(7) alembic upgrade head

# mysql command line login
mysql -h <host_url> -P 3306 -u <username> -p
show databases;
use <db_name>;
show tables;
describe <table_name>;
quit;
