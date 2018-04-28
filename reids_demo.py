import redis


save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)#开启本地radis
test1 = redis.Redis(connection_pool=save_pool)#创建一个连接实例
test2 = redis.Redis(connection_pool=save_pool)#同上，与test1共享一个存储池

'''
string操作(key:value)
'''

#set(key,value)
test1.set('set_exp1','aa')
#set()在Redis中设置值，默认不存在则创建，存在则修改
'''参数：
set(name, value, ex=None, px=None, nx=False, xx=False)
ex，过期时间（秒）
px，过期时间（毫秒）
nx，如果设置为True，则只有name不存在时，当前set操作才执行,同setnx(name, value)
xx，如果设置为True，则只有name存在时，当前set操作才执行
'''

#setex(key,value,过期时间（秒）)
test1.setex('set_exp2','bb',60)

#psetex(key,过期时间（毫秒）value)
test1.psetex('set_exp3',60000,'cc')

#mset(key1=value1,key2=value2......)批量设置值
test1.mset(mset_exp1='111',mset_exp2='222')

#取单个值get(key)
print('get(key):'+test1.get('set_exp1'))

#mget(key1,key2....)取多个值
print('mget(keys):'+str(test2.mget('set_exp2','set_exp3')))

#mget的参数可为list类型
list1=['mset_exp1','mset_exp2']
print('mget(key_list):'+str(test2.mget(list1)))

#getset(key,value)设置新值，返回原值
print('getset(key,value):'+test1.getset('set_exp1','ttt'))

#getrange(key, start, end)根据字节获取子序列
print('getrange(key, start, end):'+test1.getrange('set_exp1',0,1))

#setrange(name, offset, value)修改字符串内容，从指定字符串索引开始用传入的字串向后替换，如果新值太长时，则向后添加
test2.setrange('set_exp1',1,'asdassaesafasd')
print('setrange(name, offset, value):'+test2.get('set_exp1'))

#strlen(key)返回值的长度
print('strlen(key):'+str(test2.strlen('set_exp1')))

test1.set('int',5)
test1.set('float',5.5)

#incr(key, amount=1)自增mount对应的值，当mount不存在时，则创建mount＝amount，否则，则自增,amount为自增数(整数)
print('incr(key, amount=8):'+str(test1.incr('int',amount=8)))#输出13
print('incr(key,amount=2):'+str(test1.incr('int_2',amount=2)))#创建新key，值为2

#incrbyfloat(key, amount=1.0)类似于incr
print('incrbyfloat(key, amount=6.666)'+str(test1.incrbyfloat('float',amount=6.666)))

#decr(key,amout=1)自减amout
print('decr(key,amout=1)'+str(test1.decr('int',amount=2)))

#append(key,value)在value后追加内容
test2.append('set_exp2','aaaaaaa')
print('append(key,value)'+test2.get('set_exp2'))

#setbit(name, offset, value)对二进制表示位进行操作

#getbit(name, offset)获取name对应值的二进制中某位的值(0或1)

#bitcount(key, start=None, end=None)获取对应二进制中1的个数

'''
hash操作(key:dict)
'''

#hset(name, key, value)name对应的hash中设置一个键值对（不存在，则创建，否则，修改）
test1.hset('hs_test1','dict1','val1')

#hget(name,key)在name对应的hash中根据key获取value
print('hget(name,key):'+test1.hget('hs_test1','dict1'))

#hmset(name, mapping)在name对应的hash中批量设置键值对,mapping为dict组
test1.hmset('hs_test1',{'k1':'aa','k2':'bb'})

#hgetall(name)获取name对应hash的所有键值
print('hgetall(name):'+str(test1.hgetall('hs_test1')))

#hmget(name, keys)在name对应的hash中获取多个key的值
li = ['k1','k2']
print('hmget(name, keys, *args):'+str(test1.hmget('hs_test1','k1','k2')))
print('hmget(name,key_list):'+str(test1.hmget('hs_test1',li)))

#hlen(name) 获取hash中键值对的个数
print('hlen(name):'+str(test1.hlen('hs_test1')))

#hkeys(name) 获取hash中所有的key的值
print('hkeys(name):'+str(test1.hkeys('hs_test1')))

#hvals(name) 获取hash中所有的value的值
print('hvals(name):'+str(test1.hvals('hs_test1')))

#hexists(name, key)检查name对应的hash是否存在当前传入的key
print('hexists(name, key):'+str(test1.hexists('hs_test1','dict2')))

#hdel(name,*keys)删除指定name对应的key所在的键值对
test1.hdel('hs_test1','dict1')

#hincrby(name, key, amount=1)自增hash中key对应的值，不存在则创建key=amount(amount为整数)

#hincrbyfloat(name, key, amount=1.0)自增hash中key对应的值，不存在则创建key=amount(amount为浮点数)

#hscan(name, cursor=0, match=None, count=None)

#hscan_iter(name, match=None, count=None)

'''
List操作(key:list)
'''

#lpush(name,value(s))在name对应的list中添加元素，每个新的元素都添加到列表的最左边
test1.lpush("list_name",2)
test1.lpush("list_name",3,4,5)#保存在列表中的顺序为5，4，3，2

#rpush(name,values)同lpush，但每个新的元素都添加到列表的最右边

#lpushx(name,value)在name对应的list中添加元素，只有name已经存在时，值添加到列表的最左边

#rpushx(name,value)在name对应的list中添加元素，只有name已经存在时，值添加到列表的最右边

#llen(name)name对应的list元素的个数
print('llen(name):'+str(test1.llen('list_name')))

#linsert(name, where, refvalue, value))在name对应的列表的某一个值前或后插入一个新值
'''参数：
name: redis的name
where: BEFORE（前）或AFTER（后）
refvalue: 列表内的值
value: 要插入的数据
'''
test1.linsert("list_name","BEFORE","2","SS")#在列表内找到第一个元素2，在它前面插入SS

#lset(name, index, value)对list中的某一个索引位置重新赋值
test1.lset("list_name",0,"bbb")

#lrem(name, value, num)删除name对应的list中的指定值
''' 参数：
name:  redis的name
value: 要删除的值
num: num=0 删除列表中所有的指定值；
     num=2 从前到后，删除2个；
     num=-2 从后向前，删除2个
'''
test1.lrem("list_name","SS",num=0)

#lpop(name)移除列表的左侧第一个元素，返回值则是该元素
print('lpop(name):'+test1.lpop("list_name"))

#lindex(name, index)根据索引获取列表内元素
print('lindex(name, index)'+str(test1.lindex("list_name",1)))

#lrange(name, start, end)分片获取元素
print('lrange(name, start, end)'+str(test1.lrange("list_name",0,-1)))

#ltrim(name, start, end)移除列表内没有在该索引之内的值
test1.ltrim("list_name",0,2)

#rpoplpush(src, dst)从一个列表取出最右边的元素，同时将其添加至另一个列表的最左边
'''参数：
src 要取数据的列表
dst 要添加数据的列表
'''

#brpoplpush(src, dst, timeout=0)同rpoplpush，多了个timeout, timeout：取数据的列表没元素后的阻塞时间，0为一直阻塞

#blpop(keys, timeout)当给定多个 key 参数时，按参数 key 的先后顺序依次检查各个列表，自左向右弹出第一个非空列表的头元素。

#brpop(keys, timeout)同blpop，弹出顺序自右向左

'''
Set操作（key:set)
'''

#sadd(name,values)给name对应的集合中添加元素
test1.sadd("set_name","aa")
test1.sadd("set_name","aa","bb")

#smembers(name)获取name对应的集合的所有成员

#scard(name)获取name对应的集合中的元素个数

#sdiff(keys, *args)第一个name对应的集合中且不在其他name对应的集合的元素集合
test1.sadd("set_name1","bb","cc","dd")
print('sdiff(keys, *args):'+str(test2.sdiff("set_name","set_name1")))

#sdiffstore(dest, keys, *args)相当于把sdiff获取的值加入到dest对应的集合中

#sinter(keys, *args)获取多个name对应集合的交集
print('sinter(keys, *args):'+str(test2.sinter("set_name","set_name1")))

#sinterstore(dest, keys, *args)获取多个name对应集合的交集，再讲其加入到dest对应的集合中

#sunion(keys, *args)获取多个name对应的集合的并集
print('sunion(keys, *args):'+str(test1.sunion("set_name","set_name1")))

#sunionstore(dest,keys, *args)获取多个name对应的集合的并集，并将结果保存到dest对应的集合中

#sismember(name, value)检查value是否是name对应的集合内的元素

#smove(src, dst, value)将某个元素从一个集合中移动到另外一个集合

#spop(name)从集合的右侧移除一个元素，并将其返回

#srandmember(name, numbers)从name对应的集合中随机获取numbers个元素
print('srandmember(name, numbers):'+str(test2.srandmember("set_name2",2)))


#srem(name, values)删除name对应的集合中的某些值
print('srem(name, values):'+str(test1.srem("set_name2","bb","dd")))
