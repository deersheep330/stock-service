import os


def read_env(var):
    res = os.getenv(var)
    if res is None:
        raise Exception(f'Cannot get {var} from env')
    else:
        print(f'{var}: {res}')
        return res


def get_db_connection_url():
    return read_env('DB_CONNECTION_URL')
