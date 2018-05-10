#Author:Chernobyl   2018/5/2
from url_spider import *
#from AutoSqli import *
from Burp_force_directory import *
import re
import os
import sys
import getopt
import redis
import _thread
import time
#from AutoSqli import AutoSqli

def terminal_input():
    '''
    命令行输入处理函数
    传入参数：无
    返回值：包含参数和对应值的dict

    命令行参数：
        -u/--url= : 传入的URL
        -h ：帮助
        --spider-threads : 爬虫线程
        --burp-threads : 目录爆破线程
        -S : 爬虫参数
        -I : SQLMAP参数
        --cookie : 手动输入cookie
        --file : 输出文件名
    '''
    ter_opt={}
    url = ''
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hu:S:I:",['url=','spider-threads=','cookie=','file=','burp-threads='])
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
            print('-S : spider args')
            print('-I : sqlmap_args')
            print('--cooie : input cooikes')
            print('--file : output file')
            print('--burp-threads : Threads of burp_force_diectory module')
            sys.exit(0)
        elif opt in ('-u','--url'):
            ter_opt['url'] = arg
        elif opt in ('--spider-threads'):
            ter_opt['input_opt_spider_threads'] = int(arg)
        elif opt in ('-S'):
            ter_opt['spider_args'] = arg
        elif opt in ('-I'):
            ter_opt['sqlmap_args'] = arg
        elif opt in ('--cookie'):
            ter_opt['cookie'] = arg
        elif opt in ('--file'):
            ter_opt['file'] = arg
        elif opt in ('--burp-threads'):
            ter_opt['burp_threads'] = arg
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
        #所有参数传入redis
        for x in self.info.keys():
            self.base_redis.hset('base',x,self.info[x])
        print('optiopns:\n')
        for x in self.base_redis.hkeys('base'):
            print(x+':'+self.base_redis.hget('base',x),end = '    ')
        print('go')
        time.sleep(1)

        '''Url_Spider的线程数'''
        if 'input_opt_spider_threads' in self.info.keys():
            self.spider_threads = self.info['input_opt_spider_threads']
        else:
            self.spider_threads = 100
            self.base_redis.hset('base','input_opt_spider_threads', self.spider_threads)

        '''处理输出文件'''
        if 'file' in self.info.keys():
            self.file_status = True

    def print_data(self):
        '''格式化输出模块返回的数据
        格式：模块名
             --------
             数据
        '''

        #如果传入了输出文件的参数则打开相应的文件
        if self.file_status :
            self.data_file = self.info['file']
            self.data_file = open(self.data_file,'w')
        num = 0

        print('URL:'+self.url+'\n')
        if self.file_status:
            print('URL:'+self.url+'\n',file=self.data_file)

        #爬虫模块数据输出
        print('Burp_force_directory:\n--------------------------------------')
        if self.file_status:
            print('URL_Spider:\n--------------------------------------',file=self.data_file)
        for x in ma.base_redis.smembers('Burp_force_directory_url'):
            print(str(num+1)+':'+x)
            if self.file_status:
                print(str(num+1)+':'+x,file=self.data_file)

            num+=1
        num = 0

        #目录爆破模块的数据输出
        print('\n\nURL_Spider:\n---------------------------------')
        if self.file_status:
            print('URL_Spider:\n--------------------------------------',file=self.data_file)
        for x in ma.base_redis.smembers('Spider_full_urls'):
            print(str(num+1)+':'+x)
            if self.file_status:
                print(str(num+1)+':'+x,file=self.data_file)
            num+=1
        if self.file_status :
            self.data_file.close()

    def __init__(self):
        self.info = terminal_input()
        self.url = self.info['url']
        self.save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)#开启本地radis
        self.base_redis = redis.Redis(connection_pool=self.save_pool)
        self.base_redis.flushdb()
        self.url_check(self.url)
        self.url_type = self.base_redis.hget('base','url_type')
        self.opt_handler()
        '''各模块初始化'''
        print(self.url_type)
        #对传入的URL进行处理，增加http://前缀
        if self.url_type == '2' or self.url_type == '3':
            self.url = 'http://'+self.url
        print(self.url)
        self.spider = SpiderMain(self.url,self.save_pool)
        self.burp_force_diectory = Scanner(self.url,self.save_pool)

    def start_modules(self):
        '''多线程执行模块的运行方法'''
        _thread.start_new_thread(self.spider.run,())
        _thread.start_new_thread(self.burp_force_diectory.more_threads,())

    def module_check(self):
        '''查询模块的线程是否执行完成'''
        return [self.spider.is_finished() ,self.burp_force_diectory.is_finished()]

#if '__name__' == '__main__':
ma = base()
ma.start_modules()
while False in ma.module_check() :
    time.sleep(5)
    print('stat:',ma.spider.is_finished(),ma.burp_force_diectory.is_finished())
    continue
print('finished')
input()
ma.print_data()
input()
