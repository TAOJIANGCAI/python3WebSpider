import requests
import random
from urllib.parse import urlencode
import json
import math
import time
import pandas as pd
from threading import Thread
from queue import Queue
import pymysql


def create_table():
    db = pymysql.connect("localhost", "root", "123456", "lagou")  # 连接数据库
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS JOB")

    sql = """CREATE TABLE JOB (
                ID INT PRIMARY KEY AUTO_INCREMENT,
                companyFullName  CHAR(255),
                companyShortName CHAR(255),
                companySize CHAR(255), 
                financeStage CHAR(255), 
                district CHAR(255), 
                positionName CHAR(255), 
                workYear CHAR(255), 
                education CHAR(255), 
                salary CHAR(255), 
                positionAdvantage CHAR(255)              
                )"""

    cursor.execute(sql)

    db.close()


def insert(results):
    db = pymysql.connect(host="localhost", port=3306, user="root", password="123456", db="lagou",
                         charset='utf8')

    cursor = db.cursor()
    # sql = "INSERT INTO JOB(companyFullName,companyShortName,companySize,financeStage,district,positionName,workYear,education,salary,positionAdvantage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,)"
    try:
        for j in range(len(results)):

            sql = "INSERT INTO JOB(companyFullName,companyShortName,companySize,financeStage,district,positionName,workYear,education,salary,positionAdvantage) VALUES ("
            for i in range(len(results[j])):
                sql = sql + "'" + results[j][i] + "',"
            sql = sql[:-1] + ")"

            sql = sql.encode('utf-8')
            cursor.execute(sql)

            db.commit()
            print('插入数据成功')
    except:
        db.rollback()
        print("插入数据失败")
    db.close()


def get_json(url, page):
    url_start = "https://www.lagou.com/jobs/list_python?px=default&city=%E4%B8%8A%E6%B5%B7#filterBox"
    agent = [
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    ]

    agents = random.sample(agent, 1)
    my_headers = {
        'User-Agent': str(agent),
        'Referer': 'https://www.lagou.com/jobs/list_python?px=default&city=%E4%B8%8A%E6%B5%B7#filterBox'
    }

    # data = urlencode([
    #     ('first', 'true'),
    #     ('pn', page),
    #     ('kd', 'python')
    # ])
    data = {
        "first": "true",
        "pn": page,
        "kd": "python"
    }
    s = requests.session()
    s.get(url_start, headers=my_headers, timeout=3)
    cookie = s.cookies  # 为此次获取的cookies
    response = s.post(url, data=data, headers=my_headers, cookies=cookie, timeout=3)  # 获取此次文本

    # response.raise_for_status()
    # response.encoding = 'utf-8'
    # # 得到包含职位信息的字典
    # page = response.json()
    # print(page)
    return json.loads(response.text)


def get_page_num(totalCount):
    total_page = math.ceil(totalCount / 15)
    if total_page > 30:
        return 30
    else:
        return total_page


def get_page_info(info_list):
    total_job_list = []
    for i in info_list:
        job_list = []
        job_list.append(i['companyFullName'])
        job_list.append(i['companyShortName'])
        job_list.append(i['companySize'])
        job_list.append(i['financeStage'])
        job_list.append(i['district'])
        job_list.append(i['positionName'])
        job_list.append(i['workYear'])
        job_list.append(i['education'])
        job_list.append(i['salary'])
        job_list.append(i['positionAdvantage'])

        total_job_list.append(job_list)

    return total_job_list


def main():
    create_table()
    page_list_queue = Queue()
    url = "https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false"
    # 先设定页数为1,获取总的职位数
    # t1 = Thread(target=get_json, args=(url, 1, page_list_queue))
    # t1.start()
    page_1 = get_json(url, 1)
    # page_1 = page_list_queue.get()
    total_count = page_1['content']['positionResult']['totalCount']
    num = get_page_num(total_count)
    total_info = []
    time.sleep(20)
    print('职位总数:{},页数:{}'.format(total_count, num))

    for n in range(1, num+1):
        # 对每个网页读取JSON, 获取每页数据
        # t = Thread(target=get_json, args=(url, n, page_list_queue))
        # t.start()
        page = get_json(url, n)
        # page = page_list_queue.get()
        jobs_list = page['content']['positionResult']['result']
        page_info = get_page_info(jobs_list)
        total_info += page_info
        print('已经抓取第{}页, 职位总数:{}'.format(n, len(total_info)))
        # 每次抓取完成后,暂停一会,防止被服务器拉黑
        time.sleep(30)

    insert(total_info)


if __name__ == "__main__":
    main()
