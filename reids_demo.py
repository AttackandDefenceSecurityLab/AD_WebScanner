import redis

class base():
    def __init__(self,url):
        '''
        初始化函数
        '''
        self.url = url
        self.save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)#开启本地radis
        self.test1 = redis.Redis(connection_pool=self.save_pool)#创建一个连接实例
        self.test2 = redis.Redis(connection_pool=self.save_pool)#同上，与test1共享一个存储池

        '''
        string操作
        '''

        #set(key,value)
        self.test1.set('set_exp1','aa')
        #set()在Redis中设置值，默认不存在则创建，存在则修改
        '''参数：
        set(name, value, ex=None, px=None, nx=False, xx=False)
        ex，过期时间（秒）
        px，过期时间（毫秒）
        nx，如果设置为True，则只有name不存在时，当前set操作才执行,同setnx(name, value)
        xx，如果设置为True，则只有name存在时，当前set操作才执行
        '''

        #setex(key,value,过期时间（秒）)
        self.test1.setex('set_exp2','bb',60)

        #psetex(key,过期时间（毫秒）value)
        self.test1.psetex('set_exp3',60000,'cc')

        #mset(key1=value1,key2=value2......)批量设置值
        self.test1.mset(mset_exp1='111',mset_exp2='222')

        #取单个值get(key)
        print(self.test1.get('set_exp1'))

        #mget(key1,key2....)取多个值
        print(self.test2.mget('set_exp2','set_exp3'))

        #mget的参数可为list类型
        list1=['mset_exp1','mset_exp2']
        print(self.test2.mget(list1))

        #getset(key,value)设置新值，返回原值
        print(self.test1.getset('set_exp1','ttt'))

        #getrange(key, start, end)根据字节获取子序列
        print(self.test1.getrange('set_exp1',0,1))

        #setrange(name, offset, value)修改字符串内容，从指定字符串索引开始用传入的字串向后替换，如果新值太长时，则向后添加
        self.test2.setrange('set_exp1',1,'asdassaesafasd')
        print(self.test2.get('set_exp1'))

        #strlen(key)返回值的长度
        print(self.test2.strlen('set_exp1'))

        self.test1.set('int',5)
        self.test1.set('float',5.5)

        #incr(key, amount=1)自增mount对应的值，当mount不存在时，则创建mount＝amount，否则，则自增,amount为自增数(整数)
        print(self.test1.incr('int',amount=8))#输出13
        print(self.test1.incr('int_2',amount=2))#创建新key，值为2

        #incrbyfloat(key, amount=1.0)类似于incr
        print(self.test1.incrbyfloat('float',amount=6.666))

        #decr(key,amout=1)自减amout
        print(self.test1.decr('int',amount=2))

        #append(key,value)在value后追加内容
        self.test2.append('set_exp2','aaaaaaa')
        print(self.test2.get('set_exp2'))






base('1')
