import requests
import threading
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import redis


def turn_num(url, length):
    '''
    转化为特征向量
    :param url: url
    :param length: 域名和协议的长度，我们只需要后面的部分，前面的部分每个url都一样，节省计算
    :return: url的特征向量
    '''
    url = url[length:]
    dim = 75

    char_index = [i for i in range(len(url)) if url[i] == '/']
    char_index.insert(0, 0)

    char_weight = []
    for i in range(len(char_index)):
        try:
            char_weight.append(url[char_index[i]:char_index[i + 1]])
        except:
            char_weight.append(url[char_index[i]:])

    num = len(char_weight)

    url_weight = [ord(j)*(num-i)*(num-i) for i in range(len(char_weight)) for j in char_weight[i]]

    for i in range(len(url_weight), dim):
        url_weight.append(0)
    return url_weight


def cos(vector1,vector2):
    '''
    余弦相似度计算
    :param vector1: url1
    :param vector2: url2
    :return: 相似度大小
    '''
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a,b in zip(vector1,vector2):
        dot_product += a*b
        normA += a**2
        normB += b**2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product / ((normA*normB)**0.5)


def similarities(data, url, length):
    '''
    将url与一组url比较相似度
    :param data: 数据集
    :param url: 目标url
    :param length: 长度
    :return: 判定结果
    '''
    url_list = [turn_num(i, length) for i in data]
    target_url = turn_num(url, length)
    for i in url_list:
        try:
            if cos(target_url, i) > 0.999:
                return 1
        except:
            return 0
    return 0


class Downloader:   # 发起请求，获取内容
    def get(self, url, content):
        try:
            r = requests.get(url, timeout=5)
            if r.status_code != 200:
                print('Something Error')
                return None
            content.append(r.text)
            return content
        except:
            print("ERROR")


class UrlManager: # 管理url
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self, url, length):
        if url is None or similarities(self.old_urls, url, length):  # 判断爬过的url中有没有相似的url，如果有就跳过
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self,urls, length):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
             self.add_new_url(url, length)

    def has_new_url(self):
        return len(self.new_urls) != 0

    def get_new_url(self):
         new_url = self.new_urls.pop()
         self.old_urls.add(new_url)
         return new_url


class SpiderMain:
    def __init__(self, root, savepool):
        self.urls = UrlManager()
        self.down = Downloader()
        self.root = root
        self.domain = urlparse(root).hostname
        self.rootlength = len(self.root)
        self.savepool = savepool
        self.redis_connect()

    def run(self):
        self.redis_get()
        self.function_action(self.action)
        self.redis_set()

    def redis_get(self):
        self.action = self.spider_redis.hget('base', 'spider_args')
        self.threadnum = self.spider_redis.hget('base', 'input_opt_spider_threads')

    def redis_set(self):
        self.spider_redis.hset('Spider_urls', 'full_urls', self.urls.old_urls)

    def redis_connect(self):
        #save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
        self.spider_redis = redis.Redis(connection_pool=self.savepool)

    def judge(self, domain, url):  # 判断链接的域名
        if(url.find(domain) != -1):
            return True
        else:
            return  False

    def parse(self, page_url, content):  # 解析页面
        if content is None:
            return
        print('123123--------', page_url)
        input()
        soup = BeautifulSoup(content, 'lxml')
        news = self.get_new_urls(page_url, soup)
        return news

    def get_new_urls(self, page_url, soup):  # 从页面里面获得a标签列表，并组成新地址
        new_urls = set()
        links = soup.find_all('a')
        for link in links:
            new_url = link.get('href')
            new_full_url = urljoin(page_url, new_url)
            if self.judge(self.domain, new_full_url):
                new_urls.add(new_full_url)
        return new_urls

    def craw(self):    # 控制流程，利用多线程发起请求
        self.urls.add_new_url(self.root, self.rootlength)
        while self.urls.has_new_url():
            content = []
            th = []
            for _ in list(range(int(self.threadnum))):
                if self.urls.has_new_url() is False:
                    break
                new_url = self.urls.get_new_url()

                print("craw: " + new_url)
                t = threading.Thread(target=self.down.get, args=(new_url, content))
                t.start()
                th.append(t)
            for t in th:
                t.join()
            for _str in content:
                if _str is None:
                    print("Nothing here")
                    continue

                new_urls = self.parse(new_url, _str)
                self.urls.add_new_urls(new_urls, self.rootlength)

    def all(self):
        print('[+] ALL ' + str(len(self.urls.old_urls)))

    def check(self):
        reponse = requests.get(self.root)
        if reponse == 200:
            if len(self.urls.old_urls) > 1:
                print('the status of spider [success]')
                return 1
            else:
                print('the status of spider [fail]')
                return 0
        else:
            print('target url error')
            return 0

    def function_action(self, action):
        if action == 'craw':
            self.craw()


if __name__ == '__main__':
    url = 'http://www.leslie2018.com'
    save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
    spider = SpiderMain(url, save_pool)
    spider.run()
    print('[+]  All ' + str(len(spider.urls.old_urls)))
