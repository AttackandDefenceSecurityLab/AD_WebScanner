import url_spider

class base:
    '''
    参数：扫描网址
    '''
    def __init__(self,url):
        self.save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)#开启本地radis
        self.url = url
        '''各模块初始化'''
        self.SpiderMain(self.url, 100)
        #...
