#Author:Chernobyl   2018/5/2
from url_spider import SpiderMain
import re
import os
import sys
import getopt
import redis
from AutoSqli import AutoSqli

def terminal_input():
    '''
    命令行输入处理函数
    传入参数：无
    返回值：包含参数和对应值的dict

    命令行参数：
        -u/--url= : 传入的URL
        -h ：帮助
        --spider-threads : 爬虫线程
    '''
    ter_opt={}
    url = ''
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hu:S:I:",['url=','spider-threads='])
    except getopt.GetoptError:
      print("Command Error, type -h for usage")
      sys.exit(2)
    if len(sys.argv) == 1:
        print('AD_Scanner\nType -h for help')
        sys.exit(0)
    for opt,arg in opts:#获取参数
        if opt == '-h':
            print("Usage:")
            print("-u/--url= : URL for scanning")
            print("-h : help")
            print('--spider-thread= : Threads num of url_spider module')
            sys.exit(0)
        elif opt in ('-u','--url'):
            ter_opt['url'] = arg
        elif opt in ('--spider-threads'):
            ter_opt['spider_threads'] = int(arg)
        elif opt in ('-S'):
            ter_opt['spider_args'] = arg
        elif opt in ('-I'):
            ter_op['sqlmap_args'] = arg
    return ter_opt

class base:
    '''
    参数：扫描网址
    '''
    def url_check(self,url):
        '''
        URL检测函数
        传入参数：待检测的URL
        返回值：无

        URL类型：
        Case0:http://www.test.com/...||https://www.test.com/...
        Case1:http://test.com/...||https://test.com/...
        Case1:www||aaa.test.com/.....
        Case2:test.com/...
        other:error
        '''
        if re.match('(http|https)://(.*?)\.(.*?)\.(.*)',url) != None: #Case0:
            self.url = url
            self.base_redis.hset('base','url',url)
            self.base_redis.hset('base','url_type',0)

        if re.match('(http|https)://(.*?)\.(.*)',url) != None: #Case1:
            self.url = url
            self.base_redis.hset('base','url',url)
            self.base_redis.hset('base','url_type',1)

        elif re.match('(.*?)\.(.*?)\.(.*)',url) != None:#case 2
            self.url = url
            self.base_redis.hset('base','url',url)
            self.base_redis.hset('base','url_type',2)
        elif re.match('(.*?)\.(.*)',url) != None:#case 3:
            self.url = url
            self.base_redis.hset('base','url',url)
            self.base_redis.hset('base','url_type',3)
        else:
            print('URL Type Error!')
            sys.exit(1)#URL_ERROR

    def opt_handler(self):
        '''命令行参数处理
        针对各模块特有设置项，设置相应键值对，用于初始化和存储信息
        '''

        '''url_spider'''
        for x in self.info.keys():
            self.base_redis.hset('base',x,self.info[x])
            print(self.base_redis.hget('base',x))
        if 'spider_threads' in self.info.keys():
            self.spider_threads = self.info['spider_threads']
        else:
            self.spider_threads = 100
            self.base_redis.hset('base','input_opt_spider_threads', self.spider_threads)

    def __init__(self):
        self.info = terminal_input()
        self.url = self.info['url']
        self.save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)#开启本地radis
        self.base_redis = redis.Redis(connection_pool=self.save_pool)
        self.url_check(self.url)
        self.opt_handler()
        print('URL:'+self.base_redis.hget('base','url')+'   URL_Type:'+str(self.base_redis.hget('base','url_type')\
        +'   Spider_threads : '+str(self.base_redis.hget('base','input_opt_spider_threads'))))
        '''各模块初始化'''
        self.Spider = SpiderMain(self.url, self.save_pool, self.spider_threads)
        self.AutoSQli = AutoSqli(self.save_pool)


    def module_check(self):
        '''模块状态检查'''
        self.Spider.check()


base()
