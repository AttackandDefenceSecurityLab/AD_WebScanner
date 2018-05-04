import nmap
import socket
from urllib import parse

ports = '21, 22, 23, 25, 53, 80, 161, 162, 443, 445, 1080, 1433, 3306, 3389, 8080'

class PortScanner:
    global ports

    def __init__(self, url):
        name = parse.urlparse(url).hostname
        self.host = socket.gethostbyname(name)

    def ports_scan(self):
        host = self.host
        try:
            nm = nmap.PortScanner()
            nm.scan(host, ports)

            print('----------------------------------------------------')
            print('Host: %s (%s)' % (host, nm[host].hostname()))
            print('State: %s' % nm[host].state())

            for proto in nm[host].all_protocols():
                print('-------------')
                print('Protocol: %s' % proto)
                list_ports = nm[host][proto].keys()
                for port in list_ports:
                    print('port: %-6s\tname: %-12s\tstate: %-8s\tproduct: %-16s\textrainfo: %-12s\tversion: %-6s'
						% (port, nm[host][proto][port]['name'], nm[host][proto][port]['state'], nm[host][proto][port]['product'], nm[host][proto][port]['extrainfo'], nm[host][proto][port]['version']))
        except Exception as e:
            raise e

if __name__ == '__main__':
    url = 'https://www.baidu.com'
    portscanner = PortScanner(url)
    portscanner.ports_scan()
