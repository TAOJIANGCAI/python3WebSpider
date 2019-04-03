from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

job_list = ['机器学习实习']
driver = webdriver.Chrome()
base_url = "https://www.zhipin.com/job_detail/?query={}&city=101020100&industry=&position="


def login():
    driver.get("https://sao.zhipin.com/")
    print("页面加载完成，请手动验证后输入任意字符")
    input()


def BossItem(href, company, job):
    return href, company, job


def parse_list_page(driver, first_page):
    if first_page:
        li_list = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='main']/div/div[3]/ul/li")))
    else:
        li_list = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='main']/div/div[2]/ul/li")))

    items = []
    for li in li_list:
        href = li.find_element_by_xpath('./div/div[1]/h3/a').get_attribute('href')
        job = li.find_element_by_class_name('job-title').text
        company = li.find_element_by_class_name('company-text').text
        btn = li.find_element_by_xpath('./div/a')
        if '继续沟通' in btn.get_attribute('innerHTML'):
            print('已投递过', company)
        else:
            item = BossItem(href, company, job)
            print(item)
            items.append(item)
    return items


def request_detail_page(url):
    driver.get(url)
    WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[1]/div/div/div[3]/div[1]/a')))
    btn = driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[3]/div[1]/a')
    if btn.text == '立即沟通':
        print("发现目标，立即投递")
        btn.click()
    elif btn.text == "继续沟通":
        print('已投递过', url)


def run():
    login()
    for job in job_list:
        url = base_url.format(job)
        items = []
        first_page = True
        while True:
            driver.get(url)
            try:
                WebDriverWait(driver=driver, timeout=5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@class='page']/a[last()]")))
            except NoSuchElementException as e:
                print(e.msg)
            items.extend(parse_list_page(driver, first_page))
            first_page = False
            for item in items:
                print(item[0])
                request_detail_page(item[0])
            try:
                next_bt = driver.find_element_by_xpath("//*[@class='page']/a[last()]")
                if "disabled" in next_bt.get_attribute('class'):
                    break
                else:
                    url = next_bt.get_attribute('href')
            except NoSuchElementException as e:
                print(e.msg)
                break


if __name__ == "__main__":
    run()
