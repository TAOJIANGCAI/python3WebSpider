import requests
from lxml import etree
from multiprocessing import Process, Pool, Manager
from threading import Thread
from queue import Queue
from selenium import webdriver


class Douyu(object):
    def __init__(self):
        self.url = "https://www.douyu.com/directory/all"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        self.html_queue = Queue()
        self.conten_queue = Queue()

    def parse_url(self):
        response = requests.get(self.url, headers=self.headers)
        self.html_queue.put(response.content.decode())

    def get_content_list(self):
        while True:
            html_str = self.html_queue.get()
            html = etree.HTML(html_str)
            li_list = html.xpath("//*[@id='live-list-contentbox']/li")
            content_list = []
            for li in li_list:
                item = {}
                item["title"] = li.xpath("./a/@title")
                item["title"] = item["title"][0] if len(item["title"]) > 0 else None
                item["by_name"] = li.xpath("./a/div/p/span[1]/text()")
                item["by_name"] = item["by_name"][0] if len(item["by_name"]) > 0 else None
                item["by_num"] = li.xpath("./a/div/p/span[2]/text()")
                item["by_num"] = item["by_num"][0] if len(item["by_num"]) > 0 else None
                item["tag"] = li.xpath("./a/div/div/span/text()")
                item["tag"] = item["tag"][0] if len(item["tag"]) > 0 else None

                content_list.append(item)

            self.conten_queue.put(content_list)
            self.html_queue.task_done()
            if self.html_queue.empty():
                break

    def save_content_list(self):
        while True:
            content_list = self.conten_queue.get()
            for i in content_list:
                print(i)
            self.conten_queue.task_done()

            if self.conten_queue.empty():
                break

    def run(self):
        driver = webdriver.Chrome()
        thread_list = []
        for i in range(3):
            t1 = Thread(target=self.parse_url)
            thread_list.append(t1)

        for r in range(3):
            t2 = Thread(target=self.get_content_list)
            thread_list.append(t2)

        t3 = Thread(target=self.save_content_list)
        thread_list.append(t3)

        for t in thread_list:
            t.start()

        for p in thread_list:
            p.join()

        print("end---")


# p1 = Pool(3)
# p1.apply_async(self.parse_url)
# p2 = Pool(3)
# p2.apply_async(self.get_content_list)
# p3 = Pool()
# p3.apply_async(self.save_content_list)
#
# p1.close()
# p2.close()
# p3.close()
# p1.join()
# p2.join()
# p3.join()


if __name__ == "__main__":
    d = Douyu()
    d.run()

# url = "https://www.douyu.com/directory/all"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
#
# response = requests.get(url, headers=headers)
# html = etree.HTML(response.content.decode())
# html = html.xpath("//*[@id='J-pager']/a[text()='下一页']")
#
# print(len(html))
