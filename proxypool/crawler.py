import json
import re
from .utils import get_page
from bs4 import BeautifulSoup


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self,page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        pattern = re.compile('<td>(.*?)</td>')
        header = {
            'Cookie': 'UM_distinctid=16498a494ca35e-03efbfd4a2a419-3c604504-1fa400-16498a494cb68; _ydclearance=b8fa8f0fcec80d45d5825c29-6ae4-4365-9bb0-b651b38b41d6-1531724888; yd_cookie=7a2e0031-afec-4be9bfb69d4ee303553c98b8843b775738d5; CNZZDATA1253901093=1159170338-1531566038-null%7C1531712845; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1531634012,1531634017,1531634020,1531717690; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1531717729',
            'Host': 'www.66ip.cn',
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
            'Upgrade-Insecure-Requests': '1',
        }
        for url in urls:
            print('Crawling', url)
            html = get_page(url, options=header)
            if html:
                doc = BeautifulSoup(html, 'lxml')
                trs = doc.select('div.container table tr')
                for tr in trs[1::]:
                    content = re.findall(pattern, str(tr))
                    ip, port = content[0], content[1]
                    yield ':'.join([ip, port])

    def crawl_xicidaili(self):
        for i in range(1,3):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
                'Host': 'www.xicidaili.com',
                'Referer': 'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests': '1',
            }
            html = get_page(start_url, options=headers)
            if html:
                find_trs =re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ', '')
