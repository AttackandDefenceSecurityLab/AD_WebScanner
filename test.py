import redis

save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)#开启本地radis
test1 = redis.Redis(connection_pool=save_pool)#创建一个连接实例

data = 'aa'
test1.sadd('data',data)
data = 'bb'
test1.sadd('data',data)

data = ['dd','ff']
test1.sadd('data',data)
for x in test1.smembers('data'):
    print(type(x),x)
