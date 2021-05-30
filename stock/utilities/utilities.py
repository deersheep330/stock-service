import os
import re


def read_env(var):
    res = os.getenv(var)
    if res is None:
        raise Exception(f'Cannot get {var} from env')
    else:
        print(f'{var}: {res}')
        return res


def get_db_connection_url():
    return read_env('DB_CONNECTION_URL')


def remove_common_words_from_corp_name(corp_name):
    return re.sub(r'公司|集團|企業|科技|Corp|Inc|Ltd|CORP|INC|LTD|★|TECHNOLOGIES|LP|PLC', '', corp_name).strip()


def remove_non_han_from_corp_name(corp_name):
    return re.sub(r'[^\u4e00-\u9fff]+', '', corp_name)
