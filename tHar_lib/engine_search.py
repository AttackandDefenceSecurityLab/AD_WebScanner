from tHar_lib import myparser
import requests
import time

class Search:
    def __init__(self, word, limit, engine='baidu'):
        self.word = word
        self.total_results = ""
        self.server = "www.baidu.com"
        self.hostname = "www.baidu.com"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        self.limit = limit
        self.counter = 0
        self.quantity = '100'
        self.engine = engine
        if engine == 'baidu':
            self.server = "www.baidu.com"
        else:
            self.server = 'www.google.com'


    def do_search(self):
        if self.engine == 'baidu':
            url = 'http://' + self.server + "/s?wd=%40" + self.word + "&pn=" + str(self.counter) \
                  + "&oq=" + self.word
        else:
            url = "http://" + self.server + "/search?num=" + self.quantity + "&start=" + str(self.counter) \
                  + "&hl=en&meta=&q=%40\"" + self.word + "\""
        r = requests.get(url=url)
        self.total_results += str(r.content)
        return self.total_results


    def process(self):
        while self.counter <= self.limit and self.counter <= 1000:
            self.do_search()
            time.sleep(1)

            print("\tSearching " + str(self.counter) + " results...")
            self.counter += 10

    def get_emails(self):
        rawres = myparser.parser(self.total_results, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.total_results, self.word)
        return rawres.hostnames()

    def get_profiles(self):
        rawres = myparser.parser(self.total_results, self.word)
        return rawres.profiles()