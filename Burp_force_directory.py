import requests
import threading

class Scanner():
    def __init__(self):
        #self.url = input("请输入要检测的网址(包括http://或https://)：")
        self.url = 'http://www.sdlongli.com'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
        self.doc_list = ['ASP.txt','ASPX.txt','DIR.txt','JSP.txt','MDB.txt','PHP.txt']

    def more_threads(self):
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
        #doc_name = 'ASP.txt'
        print(doc_name)
        with open(r'dictionary\\'+doc_name) as file_obj:
            for line in file_obj:
                test_url = self.url + line
                #print(test_url)
                self.judge(test_url.rstrip())

    def judge(self, test_url):
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

Web_scanner = Scanner()
Web_scanner.more_threads()
#Web_scanner.combine_url()
#Web_scanner.judge('http://www.sdlongli.com/index1.asp')  #200
'''
try:
    t = threading.Thread(target=Web_scanner.combine_url,args=(Web_scanner.doc_list[1],))
    t.run()
    t.start()
    t.join()
except Exception as e:
    print(e)
'''