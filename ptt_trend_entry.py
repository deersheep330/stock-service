from stock.ptt import PttTrends

if __name__ == '__main__':

    print('==> ptt_trend_entry')

    trends = PttTrends()
    trends.save_to_db()
