from url_spider import SpiderMain
import re
import os
import sys
import getopt
import redis

def terminal_input():
    '''
    命令行输入处理函数
    参数：
        -u/--url= : 传入的URL
        -h ：帮助
    '''
    ter_opt={}
    url = ''
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hu:",['url=','spider-threads='])
    except getopt.GetoptError:
      print("Command Error, type -h for usage")
      sys.exit(2)
    if len(sys.argv) == 1:
        print('AD_Scanner\nType -h for help')
        sys.exit(0)
    for opt,arg in opts:
        if opt == '-h':
            print("Usage:")
            print("-u/--url= : URL for scanning")
            print("-h : help")
            print('--spider-thread= : Threads num of url_spider module')
            sys.exit(0)
        elif opt in ('-u','--url'):
            ter_opt['url'] = arg
        elif opt in ('--spider-threads'):
            ter_opt['spider_threads'] = arg
    return ter_opt

class base:
    '''
    参数：扫描网址
    '''
    def url_check(self,url):
        '''
        URL检测函数
        Case0:http://www.test.com/...||https://www.test.com/...
        Case1:http://test.com/...||https://test.com/...
        Case1:www||aaa.test.com/.....
        Case2:test.com/...
        other:error
        '''
        if re.match('(http|https)://(.*?)\.(.*?)\.(.*)',url) != None: #Case0:
            self.url = url
            self.base_linker.hset('input_url','url',url)
            self.base_linker.hset('input_url','url_type',0)

        if re.match('(http|https)://(.*?)\.(.*)',url) != None: #Case1:
            self.url = url
            self.base_linker.hset('input_url','url',url)
            self.base_linker.hset('input_url','url_type',1)

        elif re.match('(.*?)\.(.*?)\.(.*)',url) != None:#case 2
            self.url = url
            self.base_linker.hset('input_url','url',url)
            self.base_linker.hset('input_url','url_type',2)
        elif re.match('(.*?)\.(.*)',url) != None:#case 3:
            self.url = url
            self.base_linker.hset('input_url','url',url)
            self.base_linker.hset('input_url','url_type',3)
        else:
            print('URL Type Error!')
            sys.exit(1)#URL_ERROR

    def opt_handler(self):
        '''命令行参数处理
        针对各模块特有设置项，设置相应键值对，用于初始化和存储信息
        '''

        '''url_spider'''
        if 'spider_threads' in self.info.keys():
            self.base_linker.hset('input_opt','spider_threads',self.info['spider_threads'])
            self.spider_threads = self.info['spider_threads']
        else:
            self.spider_threads = 100
            self.base_linker.hset('input_opt','spider_threads',self.info['spider_threads'])

    def __init__(self):
        self.info = terminal_input()
        self.url = self.info['url']
        self.save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)#开启本地radis
        self.base_linker = redis.Redis(connection_pool=self.save_pool)
        self.url_check(self.url)
        self.opt_handler()
        print('URL:'+self.base_linker.hget('input_url','url')+'   URL_Type:'+str(self.base_linker.hget('input_url','url_type')\
        +'   Spider_threads : '+str(self.base_linker.hget('input_opt','spider_threads'))))
        '''各模块初始化'''
        self.Spider = SpiderMain(self.url, self.spider_threads)

    def module_check(self):
        '''模块状态检查'''
        pass

base()
