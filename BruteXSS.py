#!/usr/bin/env python
#-*-coding:utf8-*-
#!BruteXSS
#!author: Dlangman
'''
GET方法对url进行解析，将url分解出value。然后对value进行XSS，
    检测机制是检查response中是否有插入信息，所以payload很重要，不能乱改payload文件。
'''

import http.client
import urllib.request, urllib.parse, urllib.error
import urllib.parse
import threading
import redis
import sys

class BruteXSS(object):

    def __init__(self, url,savepool):
        self.url = url
        self.redis_out = '' #输出给共享池的''
        self.isfinish = False #是否跑完
        self.save_pool = savepool # 开启本地radis
        self.pool = redis.Redis(connection_pool=self.save_pool)  # 创建一个连接实例

        self.thread_num = 100
        self.thread_max = threading.BoundedSemaphore(self.thread_num)


    def run(self):
        old_url =[]
        while(self.pool.get('finished')=='False'):
            urls = self.pool.smembers("Spider_full_urls")
            for url in urls :
                if url not in old_url:
                    self.thread_max.acquire()
                    url_real = threading.Thread(target=self.GET,args=(url,))
                    url_real.start()
                    url_real.join()
            old_url = urls

        self.Redis_Outputer()
        self.isfinish = True

    def is_finished(self):
        return self.isfinish

    def Redis_Outputer(self):
        '''
        键设置为 :XSS_hole
        :return:
        '''
        self.pool.set('XSS_hole', self.redis_out)


    def wordlistimport(self, file,lst):
        try:
            with open(file,'r') as f:
                '''
                访问payload文件，并将结果存入lst[]中
                '''
                for line in f:
                    final = str(line.replace("\n",""))
                    lst.append(final)
        except IOError:
            print("[!] Wordlist not found!")

    def GET(self, url):
        try:
            try:
                #print(threading.current_thread(),url)
                site = url
                if 'https://' in site or 'http://' in site:
                    pass
                else:
                    site = "http://" +site

                finalurl = urllib.parse.urlparse(site) #分割url为几部分
                domain0 = '{uri.scheme}://{uri.netloc}'.format(uri=finalurl)
                domain = domain0.replace("https://","").replace("http://", "").replace("www.", "").replace("/","")

                #print("[+] Checking if " + domain + " is available")
                connection = http.client.HTTPConnection(domain)
                connection.connect()
                #print("[+] "+ domain +" is available!")

                url = site
                paraname =[]
                wordlist = 'XSS_payload/wordlist.txt'

                payloads = []
                self.wordlistimport(wordlist,payloads) #把payload放进[]里

                parameters = urllib.parse.parse_qs(finalurl.query,keep_blank_values=True)
                path = finalurl.scheme+"://"+finalurl.netloc+finalurl.path  #网址路径
                for para in parameters:
                    paraname.append(para)

                for pn in paraname:
                    # print("[+] Testing "+pn+ " parameter...")
                    for x in payloads:
                        enc = urllib.parse.quote_plus(x)
                        data = path +"?"+pn +"=" +enc  #在网址路径上补上参数
                        page = urllib.request.urlopen(data)
                        sourececode = page.read().decode()
                        if x in sourececode: #如果输入的内容完整在网页里，则认为是存在XSS
                            print(("\n[!] XSS Vulnerability Found!\n"+"value: "+pn +" \npayload: " +x))
                            self.redis_out += url +" "+ pn +" "+ x +'\n'
                            break

            except(http.client.HTTPResponse) as Exit:
                print(("[!] Site"+domain +" is offline"))
        except(KeyboardInterrupt) as Exit:
                print("\nExit...")
        self.thread_max.release()

if __name__ == '__main__':
    url = 'http://localhost/crack_demo.php?value=aaaa&pwd=#'
    savepool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
    brute = BruteXSS(url,savepool)
    print(brute.is_finished())
    brute.run()
    print(brute.is_finished())