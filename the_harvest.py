from tHar_lib.engine_search import Search
from tHar_lib import hostchecker


class TheHarvester():
    def __init__(self, word,limit=200, engine='baidu'):
        self.word = word
        self.limit = limit
        self.engine = engine

    def start_search(self):
        search = Search(self.word, self.limit, self.engine)
        search.process()
        self.all_emails = search.get_emails()
        self.all_hosts = search.get_hostnames()
        self.host_check()
        print(self.all_hosts, self.all_emails)

    def host_check(self):
        self.total_length = len(self.all_hosts)
        self.all_hosts = sorted(set(self.all_hosts))
        self.hosts = hostchecker.Checker(self.all_hosts).check()


if __name__ == '__main__':
    Harvester = TheHarvester('baidu.com')
    Harvester.start_search()

