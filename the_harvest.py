from tHar_lib.engine_search import Search
from tHar_lib import hostchecker
import redis
import tldextract

class TheHarvester():
    def __init__(self, url, savepool, limit=200, engine='baidu'):
        val = tldextract.extract(url)
        self.word = "{0}.{1}".format(val.domain, val.suffix)
        self.limit = limit
        self.engine = engine
        self.savepool = savepool
        self.finished = False
        self.redis_connect()
        
        
    def is_finished(self):
        return self.finished
    
    def redis_connect(self):
        self.harvest_redis = redis.Redis(connection_pool=self.savepool)
             
        
    def start_search(self):
        search = Search(self.word, self.limit, self.engine)
        search.process()
        self.all_emails = search.get_emails()
        self.all_hosts = search.get_hostnames()
        self.host_check()
        self.harvest_redis.sadd('Harvest_subdomain', self.all_hosts)
        self.harvest_redis.sadd('Harvest_emails', self.all_emails)
        self.finished = True
        
        
        // print(self.all_hosts, self.all_emails)

    def host_check(self):
        self.total_length = len(self.all_hosts)
        self.all_hosts = sorted(set(self.all_hosts))
        self.hosts = hostchecker.Checker(self.all_hosts).check()


if __name__ == '__main__':
    save_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
    Harvester = TheHarvester('baidu.com',savepool=save_pool)

    Harvester.start_search()

