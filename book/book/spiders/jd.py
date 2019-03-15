# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re
import json


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com', 'c0.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        # 获取大分类列表
        dt_list = response.xpath("//*[@class='mc']/dl/dt")
        for dt in dt_list:
            item = {}
            # 大分类名字
            item["b_cate"] = dt.xpath("./a/text()").extract_first()
            # 小分类列表
            em_list = dt.xpath("./following-sibling::dd[1]/em")

            for em in em_list:
                # 小分类名字
                item["s_cate"] = em.xpath("./a/text()").extract_first()

                # 小分类地址
                item["s_href"] = "https:" + em.xpath("./a/@href").extract_first()

                yield scrapy.Request(
                    item["s_href"],
                    callback=self.parse_list,
                    meta={"item": deepcopy(item)}
                )

    def parse_list(self, response):
        item = response.meta["item"]

        li_list = response.xpath("//*[@class='gl-item']")

        for li in li_list:
            item["photo_href"] = li.xpath(".//div[@class='p-img']//img/@src").extract_first()

            # item["photo_href"] = "https:" + item["photo_href"] if len(item["photo_href"]) > 0 else None

            if item["photo_href"] is None:
                item["photo_href"] = "https:" + li.xpath(".//div[@class='p-img']//img/@data-lazy-img").extract_first()
            else:
                item["photo_href"] = "https:" + item["photo_href"]

            item["book_name"] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first().strip()

            item["book_href"] = "https:" + li.xpath(".//div[@class='p-name']//a//@href").extract_first()

            item["book_author"] = li.xpath(".//span[@class='author_type_1']/a/text()").extract()

            item["book_press"] = li.xpath(".//span[@class='p-bi-store']/a/text()").extract_first()

            item["publish_date"] = li.xpath(".//span[@class='p-bi-date']//text()").extract_first().strip()

            item["vender_id"] = li.xpath("./div/@venderid").extract_first()

            item["sku_id"] = li.xpath("./div/@data-sku").extract_first()

            yield scrapy.Request(
                "https://c0.3.cn/stock?skuId={}&venderId={}&cat=1713,3258,6569&area={}".format(item["sku_id"],
                                                                                               item[
                                                                                                   "vender_id"],
                                                                                               "1_72_2799_0"),
                callback=self.parse_price,
                meta={"item": deepcopy(item)},
            )
        next_url = response.xpath("//*[@class='pn-next']/@href").extract_first()
        if next_url is not None:
            next_url = "https:" + next_url

        yield scrapy.Request(
            next_url,
            self.parse_list,
            meta={"item": deepcopy(item)}
        )

    def parse_price(self, response):
        item = response.meta["item"]

        # item["book_price"] = re.findall(r'"op":(.*?)', response.content)[0]
        # response.content()
        # item["book_price"] = json.loads(response.body.decode())[0].get("op")
        item["book_price"] = json.loads(response.text).get("stock").get("jdPrice").get("op")
        print(item)
