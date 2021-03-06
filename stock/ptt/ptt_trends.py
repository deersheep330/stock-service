from copy import deepcopy
from datetime import datetime, timedelta

from stock.db import create_engine, start_session, insert, delete_older_than
from stock.models import StockSymbol, PttTrend
from stock.nlp import JiebaPipeline
from stock.utilities import get_db_connection_url
from .ptt_parser import PttParser


class PttTrends():

    def __init__(self):
        # step 0
        # setup db connection
        self.connection_url = get_db_connection_url()
        self.engine = create_engine(self.connection_url)
        self.session = start_session(self.engine)

        count = delete_older_than(self.session, PttTrend, PttTrend.date,
                                  datetime.now().date() - timedelta(days=180))
        print(f'delete {count} old PttTrend records')
        self.session.commit()

        # step 1
        # get stock symbols and names for constructing custom dict later
        stocks = self.session.query(StockSymbol).all()
        print(f'get {len(list(stocks))} symbols !')
        self.custom_dict = {}
        self.reverse_custom_dict = {}
        self.custom_words = []
        for stock in stocks:
            self.custom_dict[stock.symbol] = stock.name
            self.reverse_custom_dict[stock.name] = stock.symbol
            self.custom_words.append(stock.symbol)
            self.custom_words.append(stock.name)

        # step 2
        # for removing meaningless words later
        # prevent them from being treated as stock symbols
        self.excludes = ['2020', '2021', '2022', '2023', '2024', '2025', 'DDD', 'VVV', 'RRR', 'ALL', 'TW', 'FB', '中國', '新聞']

        # step 3
        # parse ptt articles
        self.parser = PttParser('Stock')
        # article title + pushes
        self.sentence_list = self.parser.get_sentence_list_without_content()
        # article title only
        self.title_list = self.parser.get_title_list()

        # step 4
        # tokenization with jieba
        self.pipeline = JiebaPipeline()
        # calculate word freq for title + pushes
        self.pipeline \
            .set_custom_dict(self.custom_words) \
            .tokenize(self.sentence_list) \
            .remove_words_from_token_list(self.excludes) \
            .keep_words_from_token_list(self.custom_words) \
            .count_tokens()
        self.word_freq = deepcopy(self.pipeline.token_freq)
        print('<== word freq ==>')
        print(self.word_freq)

        # step 5-1
        # word freq for title only
        self.pipeline \
            .tokenize(self.title_list) \
            .remove_words_from_token_list(self.excludes) \
            .keep_words_from_token_list(self.custom_words) \
            .count_tokens()
        self.title_word_freq = deepcopy(self.pipeline.token_freq)

        # step 5-2
        # if an article's title contains a keyword,
        # add number of pushes of this article to this keyword's word freq
        self.title_word_freq = dict(self.title_word_freq)
        for key, _ in self.title_word_freq.items():
            for article in self.parser.get_articles():
                if key in article.title:
                    self.title_word_freq[key] += article.push_count

        # step 5-3
        # sort title_word_freq
        self.title_word_freq = sorted(self.title_word_freq.items(), key=lambda x: x[1], reverse=True)
        print('<== title word freq ===>')
        print(self.title_word_freq)

        # step 6-1
        # aggregate word_freq and title_word_freq
        self.aggregate_word_freq = {}
        for item in self.word_freq + self.title_word_freq:
            if item[0] in self.aggregate_word_freq:
                self.aggregate_word_freq[item[0]] += item[1]
            else:
                self.aggregate_word_freq[item[0]] = item[1]

        # step 6-2
        # sort aggregate_word_freq
        self.aggregate_word_freq = sorted(self.aggregate_word_freq.items(), key=lambda x: x[1], reverse=True)
        #print(self.aggregate_word_freq)

        # step 7-1
        # normalize word freq
        self.normalize_word_freq = {}
        for item in self.aggregate_word_freq:
            if item[0] in self.custom_dict:
                if item[0] in self.normalize_word_freq:
                    self.normalize_word_freq[item[0]] += item[1]
                else:
                    self.normalize_word_freq[item[0]] = item[1]
            elif item[0] in self.reverse_custom_dict:
                if self.reverse_custom_dict[item[0]] in self.normalize_word_freq:
                    self.normalize_word_freq[self.reverse_custom_dict[item[0]]] += item[1]
                else:
                    self.normalize_word_freq[self.reverse_custom_dict[item[0]]] = item[1]

        # step 7-2
        # sort normalize word freq
        self.normalize_word_freq = sorted(self.normalize_word_freq.items(), key=lambda x: x[1], reverse=True)
        print('<== normalized aggregated word freq ==>')
        print(self.normalize_word_freq)

    def save_to_db(self):
        for index, item in enumerate(self.normalize_word_freq):
            if index > 16 or item[1] < 10:
                break
            else:
                insert(self.session, PttTrend, {
                    'symbol': item[0],
                    'popularity': item[1]
                })
        self.session.commit()
        self.session.close()
