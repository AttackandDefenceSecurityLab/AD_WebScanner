#coding ='utf-8'

import urllib.request,urllib.error,urllib.parse
from Sqliscan import useragents

def gethtml(url, lastURL=False):
    """
    给定url返回html
    :param url:
    :param lastURL:
    :return: HTML或False
    """
    #对url的预处理
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "http://"+url
    header = useragents.get()
    request = urllib.request.Request(url, None, header)
    html = None

    try:
        response = urllib.request.urlopen(request,timeout=10)
    except urllib.HTPPError as e:
        #返回500
        if e.getcode() == 500:
            html = e.read()
        pass
    except urllib.URLError as e:
        pass

    except KeyboardInterrupt:
        raise  KeyboardInterrupt

    except:
        pass

    else:
        html = response.read()
        if html:
            if lastURL == True:
                return (html, response.url)
            else:
                return html
    return False


if __name__ == '__main__':
    html = gethtml("http://testphp.vulnweb.com:80/listproducts.php?cat=1")
    print(html)