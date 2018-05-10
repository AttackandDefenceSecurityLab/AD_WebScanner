#Burp_force_directory by xuxu
import requests
import threading
import redis
import os
import time
from urllib.parse import urlparse

class Scanner():
    def __init__(self, url, save_pool):
        self.burp_redis = redis.Redis(connection_pool=save_pool)
        self.url = self.Urlparse(url)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
        self.dic_list = []      #字典名目录
        self.get_url = []       #获取到的所存在的url
        self.get_url_len = 0    #获取到的有效url数量（可重复）
        self.len = 0            #获取到的有效url数量（不重复）
        self.threads_max = self.get_threads()   # 最大线程数
        self.check = False      #线程运行状态

    def Urlparse(self, url):
        '''
        把传入的url进行截取，只要scheme + netloc部分
        :return:
        '''
        k = urlparse(url)
        l = (k[0] + '://' + k[1])
        return l.rstrip()

    def get_threads(self):
        '''
        从redis中取线程数，如果返回为None，则默认50
        '''
        return int(self.burp_redis.hget('base','burp_threads'))

    def run(self):
        '''
        获取base模块的参数，决定是否运行
        :return:
        '''
        key = self.burp_redis.hget('base','burp_arg')
        if key == 'run':
            self.more_threads()


    def get_dic(self):
        '''
        获取字典目录下的文件名到self.dic_list
        增加把相对路径换成绝对路径的功能
        :return:
        '''
        for root, files, self.dic_list in os.walk('./Burp_force_directory/dictionary'):
            pass

    def more_threads(self):
        self.get_dic()
        threads = []
        self.check = False
        for k in range(0,len(self.dic_list)):
            print(self.dic_list[k])
            #t = threading.Thread(target=self.combine_url,args=(self.dic_list[k],))
            #threads.append(t)
            self.combine_url(self.dic_list[k])

        for k in threads:
            k.start()

        #for k in threads:
            #k.join()

        self.check = True

    def combine_url(self,doc_name):
        '''
        从字典中逐行取出子目录，并将其与传入的网址组合
        '''
        print(doc_name)
        with open(r'Burp_force_directory\dictionary\\'+doc_name,'r') as file_obj:
            for line in file_obj:
                test_url = self.url + line
                # print(test_url)
                if threading.activeCount() >= self.threads_max:
                    time.sleep(0.7)
                else:
                    t = threading.Thread(target=self.judge, args=(test_url.rstrip(),))
                    t.start()
                    # t.join()
                    # print(threading.activeCount())
                    # self.judge(test_url.rstrip())

    def judge(self, test_url):
        '''
        判断所传入的连接是否存在
        '''
        try:
            #print(test_url)
            k = self.request(test_url)
            #print(k.status_code)
            if k.status_code == 200:

                print(test_url)
                self.get_url.append(test_url)
                self.len = len(set(self.get_url))
                print(self.len,self.get_url_len)
                if self.len > self.get_url_len:
                    self.get_url_len = self.len
                    try:
                        self.burp_redis.hset('Burp_force_directory_scanned_url','scanned_url',set(self.get_url))
                        print(self.burp_redis.hget('Burp_force_directory','scanned_url'))
                    except Exception as p:
                        pass
                        #测试模式下开启报错
                        #print(p)


                try:
                    print(test_url)
                    self.burp_redis.sadd('Burp_force_directory_url',test_url)
                except Exception as e:
                    print(e)

        except requests.exceptions.Timeout:
            pass
        except Exception as e:
            pass
            #测试模式下开启报错输出
            #print(e)


    def request(self, test_url):
        '''
        用get方法会请求整个【头部+正文】，浪费资源
        利用head方法，只请求【资源头部】
        '''
        r = requests.head(test_url, headers=self.headers, timeout=1)
        return r

    def print_get_url(self):
        self.print_get_url = set(self.print_get_url)
        print(self.get_url)

    def is_finished(self):
        return self.check


if __name__ == '__main__':
    save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)#开启本地radis
    url = 'http://www.sdlongli.com'
    Web_scanner = Scanner(url,save_pool)
    Web_scanner.more_threads()
    print(Web_scanner.burp_redis.hget('Burp_force_directory','scanned_url'))
    #print(Web_scanner.module_redis.hget('Burp_force_directory','scanned_url'))
