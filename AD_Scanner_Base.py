#Author:Chernobyl   2018/5/2
from url_spider import *
from Burp_force_directory import *
import re
import os
import sys
import getopt
import argparse
import redis
import _thread
import time

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
        -B : 目录爆破参数
        --cookie : 手动输入cookie
        --file : 输出文件名

    '''
    ter_opt={}
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    parser = argparse.ArgumentParser(description='AnD Web Scanner',add_help=True)
    parser.add_argument('-u','--url',help='目标url')
    parser.add_argument('--cookie',default=None,help='扫描器cookie')
    parser.add_argument('-F','--file',default=None,help='输出目标文件')
    parser.add_argument('-S','--spider_args',default=None,help='全站爬虫模块方法')
    parser.add_argument('--spider_threads',default=10,help='全站爬虫模块线程数',type=int)
    parser.add_argument('-I','--sqli_args',default=None,help='SQL注入漏洞扫描模块方法')
    parser.add_argument('-B','--burp_args',default=None,help='路径爆破模块方法')
    parser.add_argument('--burp_threads',default=10,help='路径爆破模块线程数',type=int)
    parser.add_argument('--debug',default=None,help='开启Debug模式')
    args = parser.parse_args()
    for x,y in args._get_kwargs():
        ter_opt[x]=y
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
            print(x+':'+self.base_redis.hget('base',x))
        self.output_dict={}
        if self.info['spider_args'] == 'craw':
            self.output_dict['Url_Spider'] = 'Spider_full_urls'
        if self.info['burp_args'] == 'run':
            self.output_dict['Burp_force_directory'] = 'Burp_force_directory_url'
        print('go')
        time.sleep(1)

        '''处理输出文件'''
        if self.info['file'] != None:
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

        print('URL:'+self.url+'\n')
        if self.file_status:
            print('URL:'+self.url+'\n',file=self.data_file)

        for x in self.output_dict.keys():
            num = 0
            print('\n\n'+x+':\n--------------------------------------')
            if self.file_status:
                print('\n\n'+x+':\n--------------------------------------',file=self.data_file)
            for y in ma.base_redis.smembers(self.output_dict[x]):
                print(str(num+1)+':'+y)
                if self.file_status:
                    print(str(num+1)+':'+y,file=self.data_file)
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
        #对传入的URL进行处理，增加http://前缀
        if self.url_type == '2' or self.url_type == '3':
            self.url = 'http://'+self.url
        self.spider = SpiderMain(self.url,self.save_pool)
        self.burp_force_diectory = Scanner(self.url,self.save_pool)

    def start_modules(self):
        '''多线程执行模块的运行方法'''
        _thread.start_new_thread(self.spider.run,())
        _thread.start_new_thread(self.burp_force_diectory.more_threads,())

    def module_check(self):
        '''查询模块的线程是否执行完成'''
        return_list=[]
        if self.info['spider_args'] == 'craw':
            return_list.append(self.spider.is_finished())
        if self.info['burp_args'] == 'run':
            return_list.append(self.burp_force_diectory.is_finished())
        return return_list


#if '__name__' == '__main__':
ma = base()
ma.start_modules()
timer=0
while False in ma.module_check() :
    print('time=%d  stat:'%(timer),end=' ')
    for x in ma.output_dict.keys():
        print('  '+x+':',end='')
        if x == 'Url_Spider':
            print(ma.spider.is_finished(),end='')
        elif x == 'Burp_force_directory':
            print(ma.burp_force_diectory.is_finished(),end='')
    print(' ',end='\r')
    time.sleep(5)
    timer+=5
    continue
os.system('cls')
print('finished')
ma.print_data()
input()
