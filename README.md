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
```

(7) run the application with docker
```
# collect stock symbols
python symbol_entry.py

# collect ptt trend
python ptt_trend_entry.py

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

# vue web frontend
# sudo apt update
# sudo apt install nodejs npm
# npm install -g @vue/cli
cd web
npm run serve
```
