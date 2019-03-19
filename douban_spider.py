import requests
import json


class DoubanSpider(object):
    def __init__(self):
        self.url_temp_list = [{
            "url_temp": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?start={}&count=18&loc_id=108288",
            "country": "US"
        },
            {
                "url_temp": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_english_hot/items?start={}&count=18&loc_id=108288",
                "country": "UK"
            },
            {
                "url_temp": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_domestic_hot/items?start={}&count=18&loc_id=108288",
                "country": "CN"
            }]

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"}

    # 发送请求，获取响应
    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    # 提取数据
    def get_content_list(self, json_str):
        dict_ret = json.loads(json_str)
        content_list = dict_ret["subject_collection_items"]
        total = dict_ret["total"]
        return content_list, total

    # 保存
    def save_content_list(self, content_list, country):
        with open("douban.txt", "a", encoding="utf-8") as f:
            for content in content_list:
                content["country"] = country
                f.write(json.dumps(content, ensure_ascii=False, indent=4))
                f.write("\n")

    def run(self):
        for url_temp in self.url_temp_list:
            num = 0
            total = 100
            while num < total + 18:
                # 1.start_url
                url = url_temp["url_temp"].format(num)
                # 2.发送请求，获取响应
                json_str = self.parse_url(url)
                # 3.提取数据
                content_list, total = self.get_content_list(json_str)
                # 4.保存
                self.save_content_list(content_list, url_temp["country"])

                num += 18
