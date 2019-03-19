from multiprocessing import Process, Queue, Pool, Manager
from lxml import etree
import requests


class Wangyiyun(object):
    def __init__(self):
        self.start_url = "https://music.163.com/#/discover/playlist/?order=hot&cat={}&limit=35&offset={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        self.url_queue = Manager().Queue()
        self.html_queue = Manager().Queue()
        self.content_queue = Manager().Queue()

    # 获取url地址
    def get_url_list(self, cat):
        for i in range(2):
            self.url_queue.put(self.start_url.format(cat, i * 35))

    # 请求url地址，获取响应
    def parse_url(self):
        while True:
            if self.url_queue.empty():
                break
            url = self.url_queue.get()
            print(url)
            response = requests.get(url, headers=self.headers)
            print(response.content.decode())
            self.html_queue.put(response.content.decode())

    def get_content(self):
        while True:
            if self.html_queue.empty():
                break
            html_str = self.html_queue.get()
            html = etree.HTML(html_str)
            li_list = html.xpath("//*[@id='m-pl-container']/li")
            content_list = []
            for li in li_list:
                item = {}
                item["by_author"] = li.xpath("./p[2]/a/text()")
                item["by_author"] = item["by_author"][0] if len(item["by_author"]) > 0 else None
                item["name"] = li.xpath("./p[1]/a/text()")
                item["name"] = item["name"][0] if len(item["name"]) > 0 else None
                item["url"] = li.xpath("./p[1]/a/@href")
                item["url"] = item["url"][0] if len(item["url"]) > 0 else None
                content_list.append(item)

            self.content_queue.put(content_list)


if __name__ == "__main__":
    url = "https://music.163.com/#/discover/playlist/?order=hot&cat=%E6%AC%A7%E7%BE%8E&limit=35&offset=0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    response = requests.get(url, headers=headers)
    print(response.content.decode())
    html = etree.HTML(response.content.decode())
    print(html)
    li_list = html.xpath("//*[@id='m-pl-container']/li")
    print(li_list)
    # w = Wangyiyun()
    # # p1 = Process(target=w.get_url_list, args=("欧美",))
    # # p2 = Process(target=w.parse_url)
    # # p1.start()
    # # p2.start()
    # # p1.join()
    # # p2.join()
    # po = Pool(1)
    # po1 = Pool(3)
    # po2 = Pool(3)
    # po.apply(w.get_url_list, args=("欧美",))
    # po1.apply_async(w.parse_url)
    # po2.apply_async(w.get_content)
    #
    # po.close()
    # po1.close()
    # po2.close()
    #
    # po.join()
    # po1.join()
    # # po2.join()
    #
    # # while True:
    # #     if not w.url_queue.empty():
    # #         print(w.url_queue.get())
    # #     if w.url_queue.qsize() < 1:
    # #         break
