#!/usr/bin/python
# -*-coding:utf-8-*-
# Author:13yyz
import requests
import time
import json
import redis
import url_spider

class base_Sqli(object):
    """
    使用sqlmapapi的方法进行与sqlmapapi建立的server进行交互
    """
    def __init__(self, target='', server='http://127.0.0.1:8775', data='', referer='', cookie=''):
        super(base_Sqli, self).__init__()
        self.server = server
        if self.server[-1] != '/':
            self.server = self.server + '/'
        self.target = target
        self.taskid = ''
        self.engineid = ''
        self.status = ''
        self.data = data
        self.referer = referer
        self.cookie = cookie
        self.start_time = time.time()
        self.flag = False

    # 新建扫描任务
    def task_new(self):
        self.taskid = json.loads(requests.get(self.server + 'task/new').text)['taskid']
        print('Created new task: %s'%(self.taskid))
        # 得到taskid,根据这个taskid来进行其他的
        if len(self.taskid) > 0:
            return True
        return False


    # 删除扫描任务
    def task_delete(self):
        if json.loads(requests.get(self.server + 'task/' + self.taskid + '/delete').text)['success']:
            print('[%s] Deleted task' % (self.taskid))
            return True
        return False


    # 扫描任务开始
    def scan_start(self):
        headers = {'Content-Type': 'application/json'}
        # 需要扫描的地址
        payload = {'url': self.target}
        url = self.server + 'scan/' + self.taskid + '/start'
        t = json.loads(requests.post(url, data=json.dumps(payload), headers=headers).text)
        #time.sleep(5)
        self.engineid = t['engineid']
        if len(str(self.engineid)) > 0 and t['success']:
            print('Started scan')
            return True
        return False


    # 扫描任务的状态
    def scan_status(self):
        self.status = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/status').text)['status']
        if self.status == 'running':
            return 'running'
        elif self.status == 'terminated':
            return 'terminated'
        else:
            return 'error'


    # 扫描任务的细节
    def scan_data(self):
        self.data = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/data').text)['data']
        if len(self.data) == 0:
            print('not injection:\t')
            self.flag = False

        else:
            print('injection: %s' % (self.target))
            self.flag = True


    # 扫描的设置,主要的是参数的设置
    def option_set(self):
        headers = {'Content-Type': 'application/json'}
        option = {"options": {
                    "smart": True,
                    }
                }
        url = self.server + 'option/' + self.taskid + '/set'
        t = json.loads(requests.post(url, data=json.dumps(option), headers=headers).text)
        print(t)

    # 停止扫描任务
    def scan_stop(self):
       t =  json.loads(requests.get(self.server + 'scan/' + self.taskid + '/stop').text)['success']


    # 杀死扫描任务进程
    def scan_kill(self):
        t = json.loads(requests.get(self.server + 'scan/' + self.taskid + '/kill').text)['success']


    def _run(self):
        if not self.task_new():
            return False
        #self.option_set()
        if not self.scan_start():
            return False
        while True:
            if self.scan_status() == 'running':
                time.sleep(10)
            elif self.scan_status() == 'terminated':
                break
            else:
                break
            alltime = time.time() - self.start_time
            print(alltime)
            if alltime > 3000:
                # error = True
                self.scan_stop()
                self.scan_kill()
                break
        self.scan_data()
        self.task_delete()
        # print(time.time() - self.start_time)

    def redis_connect_get(self):
        #save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
        self.AutoSqli_redis = redis.Redis(connection_pool=self.savepool)
        self.urls_set = self.AutoSqli_redis.hget('Spider_urls', 'full_urls')



class AutoSqli(object):

    def __init__(self,save_pool):
        self.save_pool = save_pool
        self.redis_connect_get()
        self.run()

    def redis_connect_get(self):
        self.AutoSqli_redis = redis.Redis(connection_pool=self.save_pool)
        self.urls_list = list(self.AutoSqli_redis.hget('Spider_urls', 'full_urls'))


    def run(self):
        for url in self.urls_list:
            t = base_Sqli(url)
            t._run()
            if t.flag == True:
                print('I found a url')
                input()


if __name__ == '__main__':
    sqlmap = AutoSqli()


