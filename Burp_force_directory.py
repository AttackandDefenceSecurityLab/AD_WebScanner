#Burp_force_directory
import requests
import threading
import redis

class Scanner():
    def __init__(self, url, save_pool):
        self.module_redis = redis.Redis(connection_pool=save_pool)
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
        self.doc_list = ['ASP.txt','ASPX.txt','DIR.txt','JSP.txt','MDB.txt','PHP.txt']
        #self.doc_list = ['ASP.txt']
        #获取到的所存在的url
        self.get_url = []
        self.get_url_len = 0
        self.len = 0

    def more_threads(self):
        '''
        为每个字典创建一个线程
        '''
        threads = []
        for k in range(0,len(self.doc_list)):
            print(self.doc_list[k])
            t = threading.Thread(target=self.combine_url,args=(self.doc_list[k],))
            threads.append(t)

        for k in threads:
            k.start()

        for k in threads:
            k.join()


    def combine_url(self,doc_name):
        '''
        从字典中逐行取出子目录，并将其与传入的网址组合
        '''
        print(doc_name)
        with open(r'Brup_force_directory\dictionay\\'+doc_name,'r') as file_obj:
            for line in file_obj:
                test_url = self.url + line
                #print(test_url)
                self.judge(test_url.rstrip())

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
                        self.module_redis.hset('Burp_force_diectory','scanned_url',set(self.get_url))
                        print(self.module_redis.hget('Burp_force_diectory','scanned_url'))
                    except Exception as p:
                        print(p)

        except requests.exceptions.Timeout:
            pass
        except Exception as e:
            #pass
            #测试模式下开启报错输出
            print(e)


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




if __name__ == '__main__':
    save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)#开启本地radis
    url = 'http://www.sdlongli.com'
    Web_scanner = Scanner(url,save_pool)
    Web_scanner.more_threads()
    print(Web_scanner.module_redis.hget('Burp_force_diectory','scanned_url'))
    #print(Web_scanner.module_redis.hget('Burp_force_diectory','scanned_url'))
