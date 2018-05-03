import requests
import threading

class Scanner():
    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
        self.doc_list = ['ASP.txt','ASPX.txt','DIR.txt','JSP.txt','MDB.txt','PHP.txt']

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
        #doc_name = 'ASP.txt'
        print(doc_name)
        with open(r'dictionary\\'+doc_name) as file_obj:
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
        except Exception as e:
            print(e)

    def request(self, test_url):
        '''
        用get方法会请求整个【头部+正文】，浪费资源
        利用head方法，只请求【资源头部】
        '''
        r = requests.head(test_url, headers=self.headers)
        return r

url = 'www.sdlongli.com'
Web_scanner = Scanner(url)
Web_scanner.more_threads()
