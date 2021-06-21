from stock.reunion import ReunionTrends

if __name__ == '__main__':

    print('==> reunion_entry')

    trends = ReunionTrends()
    print(trends.get_popularities())
    trends.save_to_db()
