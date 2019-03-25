from ProxyPool.utils import get_page
from pyquery import PyQuery as pq
import re
from lxml import etree


class ProxyMetaClass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaClass):
    def get_proxies(self, callback):
        proxies = []

        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)

        return proxies

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return:
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]

        for url in urls:
            print('crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ":".join([ip, port])

    def crawl_ip336(self):
        for page in range(1, 4):
            start_url = "http://www.ip3366.net/free/?stype=1&page={}".format(page)
            html_str = get_page(start_url)
            # if html_str:
            #     html = etree.HTML(html_str)
            #     tr_list = html.xpath('//*[@id="list"]/table/tbody/tr')
            #     for tr in tr_list:
            #         ip = tr.xpath(".//td[1]/text()")[0]
            #         port = tr.xpath(".//td[2]/text()")[0]
            #         yield ":".join([ip, port])
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html_str)
            for ip, port in re_ip_address:
                result = ip + ":" + port
                yield result.replace(' ', '')

    def crwal_kuaidaili(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Cookie": "channelid=0; sid=1552453215605710; _ga=GA1.2.1976991072.1552454708; _gid=GA1.2.1280637029.1553239774; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1552454708,1553239774; _gat=1; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1553241731",
            'Host': 'www.kuaidaili.com',
            "Accept-Language": "zh-CN,zh;q=0.9",
            'Referer': 'https://www.kuaidaili.com/free/inha/3',
            'Upgrade-Insecure-Requests': '1',
        }
        for i in range(1, 4):
            start_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url, options=headers)
            if html:
                ip = re.compile('<td data-title="IP">(.*?)</td>')
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_ip = ip.findall(html)
                re_port = port.findall(html)

                for ip, port in zip(re_ip, re_port):
                    result = ip + ":" + port
                    yield result.replace(' ', '')

    def crawl_xicidaili(self):
        for i in range(1, 3):
            start_url = "https://www.xicidaili.com/nn/{}".format(i)
            html_str = get_page(start_url)
            if html_str:
                html = etree.HTML(html_str)
                tr_list = html.xpath("//*[@id='ip_list']//tr")[1:]
                for tr in tr_list:
                    ip = tr.xpath(".//td[2]/text()")[0]
                    port = tr.xpath(".//td[3]/text()")[0]

                    yield ":".join([ip, port])

    def crawl_ip3366(self):
        for i in range(1, 4):
            start_url = "http://www.ip3366.net/?stype=1&page={}".format(i)
            html_str = get_page(start_url)
            if html_str:
                html = etree.HTML(html_str)
                tr_list = html.xpath("//*[@id='list']/table//tbody/tr")
                for tr in tr_list:
                    ip = tr.xpath("./td[1]/text()")[0]
                    port = tr.xpath("./td[2]/text()")[0]
                    result = ip + ":" + port
                    yield result.replace(' ', '')

    def crawl_iphai(self):
        start_url = "http://www.iphai.com/"
        html = get_page(start_url)
        if html:
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html)
            for tr in range(1, len(trs)):
                find_ip = re.compile('<td>\s*(\d+\.\d+\.\d+\.\d+)\s*</td>', re.S)
                find_port = re.compile('<td>\s*(\d+)\s*</td>', re.S)

                re_ip = find_ip.findall(trs[tr])
                re_port = find_port.findall(trs[tr])

                for ip, port in zip(re_ip, re_port):
                    ip_port = ip + ":" + port
                    yield ip_port.replace(' ', '')

    def crawl_data5u(self):
        start_url = "http://www.data5u.com/free/gngn/index.shtml"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Origin': 'http://www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        html = get_page(start_url, options=headers)
        if html:
            ip_port = re.compile('<span>\s*<li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?\">(\d+)</li>', re.S)
            re_ip_port = ip_port.findall(html)
            for ip, port in re_ip_port:
                result = ip + ":" + port
                yield result.replace(' ', '')
