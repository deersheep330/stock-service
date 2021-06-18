# stock-service

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
python symbol_entry.py
python ptt_trend_entry.py
python reunion_entry.py
```