import redis
from stock.utilities import get_redis_host

if __name__ == '__main__':

    r = redis.Redis(host=get_redis_host(), port=6379, db=0)

    print(r.set('foo', 'bar'))
    print(r.get('foo'))
