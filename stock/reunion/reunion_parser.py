import requests


class ReunionParser():

    def __init__(self):
        self.url = 'https://www.cmoney.tw/follow/channel/getdata/channellisthotstock?mainId=9&subId=0&size=26'
        self.list = []
        self.num_list = []

    def parse(self):
        print(f'==> request page: {self.url}')
        resp = requests.get(self.url)
        resp_json = resp.json()

        for entry in resp_json:
            _symbol = entry['Caption']
            _popularity = int(entry['Popularity'].replace(',', ''))
            self.list.append(_symbol)
            self.num_list.append(_popularity)

        print(f'==> get {len(self.list)} symbols')
