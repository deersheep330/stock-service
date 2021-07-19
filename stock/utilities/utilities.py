import os
import re
from datetime import datetime, timedelta


def read_env(var):
    res = os.getenv(var)
    if res is None:
        raise Exception(f'Cannot get {var} from env')
    else:
        print(f'{var}: {res}')
        return res


def get_db_connection_url():
    return read_env('DB_CONNECTION_URL')


def get_redis_host():
    return read_env('REDIS_HOST')


def get_fugle_api_token():
    return read_env('FUGLE_API_TOKEN')


def remove_common_words_from_corp_name(corp_name):
    return re.sub(r'公司|集團|企業|科技|Corp|Inc|Ltd|CORP|INC|LTD|★|TECHNOLOGIES|LP|PLC', '', corp_name).strip()


def remove_non_han_from_corp_name(corp_name):
    return re.sub(r'[^\u4e00-\u9fff]+', '', corp_name)


def is_tw_stock(_symbol):
    return any(char.isdigit() for char in _symbol)


def how_many_days_ago(days=14):
    return datetime.now().date() - timedelta(days=days)
