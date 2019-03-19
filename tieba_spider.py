import requests
from lxml import etree
import json


class TiebaSpider(object):
    def __init__(self, tieba_name):
        self.tieba_name = tieba_name
        self.prefix_url = "https://tieba.baidu.com"
        self.prefix_next_ur = "https:"
        self.start_url = "https://tieba.baidu.com/f?kw={}&ie=utf-8&pn=0".format(tieba_name)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

    # 发送请求，获取响应
    def parse_url(self, url):
        print(url)
        response = requests.get(url)
        return response.content.decode()

    # 提取数据
    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        li_list = html.xpath("//*[@class=' j_thread_list clearfix']")
        content_list = []
        for li in li_list:
            item = {}

            item["title"] = li.xpath("./div/div[2]/div/div[1]/a/text()")[0] if len(
                li.xpath("./div/div[2]/div/div[1]/a/text()")) > 0 else None

            item["href"] = self.prefix_url + li.xpath("./div/div[2]/div/div[1]/a/@href")[0] if len(
                li.xpath(".//div/div[2]/div/div[1]/a/@href")) > 0 else None
            item["img_list"] = self.get_img_list(item["href"], [])
            item["img_list"] = [requests.utils.unquote(i) for i in item["img_list"]]
            content_list.append(item)
        # 提取下一页的url地址
        next_url = self.prefix_next_ur + requests.utils.unquote(
            html.xpath("//*[@id='frs_list_pager']//a[text()='下一页>']/@href")[0]) if len(
            html.xpath("//*[@id='frs_list_pager']//a[text()='下一页>']/@href")) > 0 else None

        return content_list, next_url

    # 获取帖子中的所有的图片
    def get_img_list(self, detail_url, total_img_list):
        # 请求列表页的url地址，获取详情页的第一页
        detail_html_str = self.parse_url(detail_url)
        detail_html = etree.HTML(detail_html_str)

        # 提取详情页第一页的图片，提取下一页的地址
        img_list = detail_html.xpath("//img[@class='BDE_Image']/@src")
        total_img_list.extend(img_list)

        # 请求详情页下一页的地址
        detail_next_url = detail_html.xpath("//*[@class='l_pager pager_theme_5 pb_list_pager']//a[text()='下一页']/@href")

        if len(detail_next_url) > 0:
            detail_next_url = self.prefix_url + detail_next_url[0]
            return self.get_img_list(detail_next_url, total_img_list)

        return total_img_list

    # 保存数据
    def save_content_list(self, content_list):
        file_path = self.tieba_name + ".txt"
        with open(file_path, "a", encoding="utf-8") as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=2))
                f.write("\n")

    def run(self):
        next_url = self.start_url
        while next_url is not None:
            # 发送请求，获取响应
            html_str = self.parse_url(next_url)
            # 获取内相应内容,下一页地址
            content_list, next_url = self.get_content_list(html_str)
            self.save_content_list(content_list)


t = TiebaSpider("做头发")
t.run()

# url = "https://tieba.baidu.com/f?kw=%E5%81%9A%E5%A4%B4%E5%8F%91&ie=utf-8&pn=0"
# ret = requests.get(url)
# html = etree.HTML(ret.content.decode())
# li_list = html.xpath("//*[@class=' j_thread_list clearfix']")
# next_url = requests.utils.unquote(
#     html.xpath("//*[@id='frs_list_pager']//a[text()='下一页>']/@href")[0]) if len(
#     html.xpath("//*[@id='frs_list_pager']//a[text()='下一页>']/@href")) > 0 else None
# print(next_url)
# # print(html.xpath("//*[@class=' j_thread_list clearfix'][1]/div/div[2]/div/div[1]/a/@href"))
# content_list = []
# for li in li_list:
#     item = {}
#     item["title"] = li.xpath("./div/div[2]/div/div[1]/a/text()")[0] if len(
#         li.xpath("./div/div[2]/div/div[1]/a/text()")) > 0 else None
#     item["href"] = li.xpath("./div/div[2]/div/div[1]/a/@href")[0] if len(
#         li.xpath(".//div/div[2]/div/div[1]/a/@href")) > 0 else None
#     content_list.append(item)
