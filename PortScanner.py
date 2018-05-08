# -*- coding: utf-8 -*- 
import nmap
import socket
from urllib import parse

ports = '21, 22, 23, 25, 53, 80, 161, 162, 443, 445, 1080, 1433, 3306, 3389, 8080'
'''
21      ftp
22      ssh
23      telnet
25      smtp
53      domain
80      http
139     netbios-ssn
161/162 snmp
443     https
445     microsoft-ds
1080    socks
1433    mssql
1521    oracle
3306    mysql
3389    ms-wbt-server
8080    http-proxy
'''

class PortScanner:
    global ports

    def __init__(self, url):
        '''
        从url中获取主机名，并将其解析为对应的ip地址
        '''
        name = parse.urlparse(url).hostname
        self.host = socket.gethostbyname(name)

    def ports_scan(self):
        '''
        使用nmap对指定的端口进行扫描，并将每个端口的扫描结果逐一输出
        '''
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
