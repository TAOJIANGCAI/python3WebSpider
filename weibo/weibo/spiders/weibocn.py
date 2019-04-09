# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Spider
import json
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from weibo.items import UserItem, UserRealationItem, WeiboItem


class WeibocnSpider(scrapy.Spider):
    name = 'weibocn'
    allowed_domains = ['m.weibo.cn']

    # 个人主页
    user_url = "https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}"
    # 关注
    follw_url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}"
    # 粉丝
    fans_url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&page={page}"
    # 微博
    weibo_url = "https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&page={page}&containerid=107603{uid}"

    users = ["2970779124"]

    cookies = "SINAGLOBAL=6119796817307.841.1551683796444; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=3361814508095.3135.1554691609637; ULV=1554691609725:4:2:1:3361814508095.3135.1554691609637:1554340261892; TC-V5-G0=07e0932d682fda4e14f38fbcb20fac81; wb_view_log_2970779124=1366*7681; Ugrow-G0=968b70b7bcdc28ac97c8130dd353b55e; login_sid_t=96c480db3d575328af4cbbf57a35d1f4; cross_origin_proto=SSL; wb_view_log=1366*7681; SCF=AvuNCH1VwlOIJJtZ6TwKMGEQ2zykbz2DIVPREUXYNA6vrlFz9CG0fUCk38HTNn-lb754sDlRDrg63AHD2sjPpT4.; SUB=_2A25xrrzoDeRhGeRH7FIW9yfNyTiIHXVS3akgrDV8PUNbmtAKLUbikW9NTdFnC4fJTvZrI4Afu1PwnxAYNSEUznhu; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhIK-6EUGdbbozD-p41mO.N5JpX5KzhUgL.Foz4S05NS0.peoB2dJLoIf2LxKqL1hnL1K2LxKqLBozLBK2LxK.L1KzLBo2LxK-L12qLB-qLxKqL1hnL1K2LxKqL1heLBoeLxK-L1hMLB.2LxK-L12-LB.zLxKML12-LBK.t; SUHB=0rr7qr5Q1feWIw; ALF=1586233400; SSOLoginState=1554697400; wvr=6; TC-Page-G0=8dc78264df14e433a87ecb460ff08bfe|1554697447|1554697404; YF-V5-G0=73b58b9e32dedf309da5103c77c3af4f; YF-Page-G0=3d0866500b190395de868745b0875841|1554697472|1554697472; webim_unReadCount=%7B%22time%22%3A1554697804229%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D"

    def start_requests(self):
        for uid in self.users:
            yield Request(self.user_url.format(uid=uid),
                          cookies={i.split("=")[0]: i.split("=")[1] for i in self.cookies.split(" ")},
                          callback=self.parse_user)

    # def parse_login(self, response):
    #     self.driver.get(self.login_url)
    #     print("页面加载完成，请手动验证后输入任意字符")
    #     qr_btn = WebDriverWait(driver=self.driver, timeout=5).until(
    #         EC.presence_of_element_located((By.XPATH, "//*[@action-data='type=qrcode']")))
    #     html = etree.HTML(response.text)
    #     qr_btn.click()
    #     yield Request(self.user_url, callback=self.parse_user)

    def parse_user(self, response):
        """
        解析用户信息
        :param response:
        :return:
        """
        self.logger.debug(response)
        # print(response.text)
        result = json.loads(response.text)
        if result.get("data").get("userInfo"):
            user_info = result.get("data").get("userInfo")
            user_item = UserItem()

            field_map = {'id': 'id', 'name': 'screen_name', 'avatar': 'profile_image_url', 'cover': 'cover_image_phone',
                         'gender': 'gender', 'description': 'description', 'fans_count': 'followers_count',
                         'follows_count': 'follow_count', 'weibos_count': 'statuses_count', 'verified': 'verified',
                         'verified_reason': 'verified_reason', 'verified_type': 'verified_type'}
            for field, attr in field_map.items():
                user_item[field] = user_info.get("attr")

            yield user_item

            # 关注
            uid = user_info.get("id")
            yield Request(self.follw_url.format(uid=uid, page=1), callback=self.parse_follows,
                          meta={"uid": uid, "page": 1})

            # 粉丝
            yield Request(self.fans_url.format(uid=uid, page=1), callback=self.parse_fans,
                          meta={"uid": uid, "page": 1})

            # 微博
            yield Request(self.weibo_url.format(uid=uid, page=1), callback=self.parse_weibo,
                          meta={"uid": uid, "page": 1})

    def parse_fans(self, response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and \
                result.get('data').get('cards')[-1].get('card_group'):
            fans = result.get('data').get('cards')[-1].get('card_group')
            for fan in fans:
                if fan.get('user'):
                    uid = fan.get('user').get('id')
                    yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

            uid = response.meta.get('uid')
            # 粉丝列表
            user_relation_item = UserRealationItem()
            fans = [{"id": fan.get('user').get('id'), "name": fan.get('user').get("screen_name")} for fan in fans]
            user_relation_item["id"] = uid
            user_relation_item["fans"] = fans
            user_relation_item["follows"] = []
            # 下一页粉丝
            page = response.meta.get("page") + 1
            yield Request(self.fans_url.format(uid=uid, page=page), callback=self.parse_fans,
                          meta={"uid": uid, "page": page})

    def parse_follows(self, response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and \
                result.get('data').get('cards')[-1].get('card_group'):
            follows = result.get('data').get('cards')[-1].get('card_group')
            for follow in follows:
                if follow.get('user'):
                    uid = follow.get('user').get('id')
                    yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

            uid = response.meta.get('uid')
            # 关注列表
            user_relation_item = UserRealationItem()
            follows = [{"id": follow.get('user').get('id'), "name": follow.get('user').get("screen_name")} for follow in
                       follows]
            user_relation_item["id"] = uid
            user_relation_item["fans"] = []
            user_relation_item["follows"] = follows
            # 下一页关注
            page = response.meta.get("page") + 1
            yield Request(self.follw_url.format(uid=uid, page=page), callback=self.parse_follows,
                          meta={"uid": uid, "page": page})

    def parse_weibo(self, response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards'):
            weibos = result.get('data').get('cards')
            for weibo in weibos:
                mblog = weibo.get('mblog')
                if mblog:
                    weibo_item = WeiboItem()
                    field_map = {
                        'id': 'id', 'attitudes_count': 'attitudes_count', 'comments_count': 'comments_count',
                        'reposts_count': 'reposts_count', 'picture': 'original_pic', 'pictures': 'pics',
                        'created_at': 'created_at', 'source': 'source', 'text': 'text', 'raw_text': 'raw_text',
                        'thumbnail': 'thumbnail_pic',
                    }
                    for field, attr in field_map.items():
                        weibo_item[field] = mblog.get(attr)
                    weibo_item['user'] = response.meta.get('uid')
                    yield weibo_item
            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1
            yield Request(self.weibo_url.format(uid=uid, page=page), callback=self.parse_weibo,
                          meta={'uid': uid, 'page': page})
