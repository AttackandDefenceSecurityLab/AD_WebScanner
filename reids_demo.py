import redis

class base():
    def __init__(self,url):
        '''
        初始化函数
        '''
        self.url = url
        self.save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
        self.test1 = redis.Redis(connection_pool=self.save_pool)
        self.test2 = redis.Redis(connection_pool=self.save_pool)
        self.test1.lpush("list1", "123312312")
        self.test2.lpush("list1","43232")
        print(type(self.test1.lrange('list1',0,-1)))
        print(set(self.test1.lrange('list1',0,-1)))
base('1')

