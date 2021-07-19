import pickle
import redis

from stock.institutions_chart import InstitutionsOverBoughtChart, InstitutionsOverSoldChart
from stock.utilities import get_redis_host

if __name__ == '__main__':

    # get redis connection
    r = redis.Redis(host=get_redis_host(), port=6379, db=0)

    # generate ins buy trend chart and store in redis
    chart = InstitutionsOverBoughtChart()
    ins_buy_data = pickle.dumps(chart.trends)
    r.set('ins_buy', ins_buy_data)
    print('store ins_buy trend chart in redis ok:')
    print(pickle.loads(r.get('ins_buy')))

    # generate ins sell trend chart and store in redis
    chart = InstitutionsOverSoldChart()
    ins_sell_data = pickle.dumps(chart.trends)
    r.set('ins_sell', ins_sell_data)
    print('store ins_sell trend chart in redis ok:')
    print(pickle.loads(r.get('ins_sell')))
