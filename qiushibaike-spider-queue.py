import requests
from lxml import etree
import json, time
from threading import Thread
from queue import Queue


class Qiushi(object):
    def __init__(self):
        self.url = "https://www.qiushibaike.com/hot/page/{}/"
        self.prefix_img_url = "https:"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        self.url_queue = Queue()
        self.response_queue = Queue()
        self.content_queue = Queue()

    def get_url_list(self):
        for i in range(3):
            self.url_queue.put(self.url.format(i))

    # 发送请求
    def parse_url(self):
        while True:
            url = self.url_queue.get()
            print(url)
            response = requests.get(url, headers=self.headers)
            self.response_queue.put(response.content.decode())
            self.url_queue.task_done()

    def get_content_list(self):
        while True:
            response_content = self.response_queue.get()
            html = etree.HTML(response_content)
            div_list = html.xpath("//*[@id='content-left']/div")

            content_list = []
            for div in div_list:
                item = {}
                item["content"] = div.xpath(".//div[@class='content']/span/text()")
                item["content"] = [i.replace("\n", "") for i in item["content"]]
                item["author_gender"] = div.xpath(".//div[contains(@class,'articleGender')]/@class")
                item["author_gender"] = item["author_gender"][0].split(" ")[-1].replace("Icon", "") if len(
                    item["author_gender"]) > 0 else None

                item["auhtor_age"] = div.xpath(".//div[contains(@class,'articleGender')]/text()")
                item["auhtor_age"] = item["auhtor_age"][0] if len(item["auhtor_age"]) > 0 else None

                item["content_img"] = div.xpath(".//div[@class='thumb']/a/img/@src")
                item["content_img"] = self.prefix_img_url + item["content_img"][0] if len(
                    item["content_img"]) > 0 else None
                item["author_img"] = div.xpath(".//div[contains(@class,'author clearfix')]/a/img/@src")
                item["author_img"] = self.prefix_img_url + item["author_img"][0] if len(
                    item["author_img"]) > 0 else None
                item["stats_vote"] = div.xpath(".//span[contains(@class,'stats-vote')]/i/text()")
                item["stats_vote"] = item["stats_vote"][0] if len(item["stats_vote"]) > 0 else None

                content_list.append(item)

            self.content_queue.put(content_list)
            self.response_queue.task_done()

    # 保存数据
    def save_content_list(self):
        while True:
            content_list = self.content_queue.get()
            for content in content_list:
                print(content)
            self.content_queue.task_done()

    def run(self):
        thread_list = []
        t4 = Thread(target=self.get_url_list)
        thread_list.append(t4)
        for i in range(10):
            t1 = Thread(target=self.parse_url)
            thread_list.append(t1)
        for i in range(3):
            t2 = Thread(target=self.get_content_list)
            thread_list.append(t2)
        for i in range(2):
            t3 = Thread(target=self.save_content_list)
            thread_list.append(t3)

        for t in thread_list:
            # 设置为守护线程，当主线程结束，子线程结束
            t.setDaemon(True)
            t.start()

        for p in [self.url_queue, self.content_queue, self.response_queue]:
            # 让主线程阻塞，当队列任务完成，主线程才结束
            p.join()

        print("主线程结束")


if __name__ == "__main__":
    q = Qiushi()
    q.run()
