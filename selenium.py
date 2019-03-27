from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

brower = webdriver.Chrome()

# 1,访问页面
# brower.get("https://www.baidu.com/")
# print(brower.page_source)
# brower.close()

# 2，查找单个元素
# brower.get("http://www.taobao.com")
# print(brower.find_element_by_id("J_SiteFooter"))
# print(brower.find_elements_by_xpath("//*[@id='J_SiteFooter']"))
# print(brower.find_element_by_css_selector("#J_SiteFooter"))
#
# print(brower.find_element(By.ID, 'J_SiteFooter'))
# print(brower.find_element(By.CSS_SELECTOR, '#J_SiteFooter'))
# print(brower.find_element(By.XPATH, "//*[@id='J_SiteFooter']"))
# brower.close()

# 3，多个元素查找
# brower.get("http://www.taobao.com")
# print(brower.find_elements(By.CSS_SELECTOR, '.layer'))
# brower.close()

# 4,元素交互
# brower.get("http://www.taobao.com")
# input_str = brower.find_element(By.ID, 'q')
# input_str.send_keys("ipad")
# time.sleep(1)
# input_str.clear()
# input_str.send_keys("iphone")
# brower.find_element(By.XPATH, "//*[@type='submit']").click()

# 5,动作交互
# brower.get("http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable")
# brower.switch_to.frame("iframeResult")
# source = brower.find_element(By.ID, 'draggable')
# target = brower.find_element(By.ID, 'droppable')
# actions = ActionChains(brower)
#
# actions.drag_and_drop(source, target)
# actions.perform()

# 6,执行js
# brower.get("http://www.zhihu.com/explore")
# # brower.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# # brower.execute_script("alert('to bottom')")
# logo = brower.find_element_by_id('zh-top-link-logo')
# print(logo)
# print(logo.get_attribute('href'))
# print(logo.get_attribute('class'))
# print(logo.text)
# print(logo.location)
# print(logo.size)
# print(logo.tag_name)

# 7,frame

# brower.get("http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable")
# brower.switch_to.frame('iframeResult')
# source = brower.find_element(By.ID, 'draggable')
# print(source)
# try:
#     logo = brower.find_element_by_class_name('logo')
#     print(logo)
# except NoSuchElementException as e:
#     print(e)
# brower.switch_to.parent_frame()
# logo = brower.find_element_by_class_name('logo')
# print(logo, logo.text)

# 8,等待

# 1,隐式等待
# brower.implicitly_wait(10)
# brower.get('https://www.zhihu.com/explore')
# input = brower.find_element_by_class_name('zu-top-add-question')
# print(input)

# 2，显示等待
# brower.get("https://www.taobao.com")
# wait = WebDriverWait(brower, 10)
# input = wait.until(EC.presence_of_element_located((By.ID, 'q')))
# button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
# input.send_keys("ipad")
# button.click()

# 9,浏览器前进后退
# brower.get('https://www.baidu.com/')
# brower.get('https://www.taobao.com/')
# brower.get('https://www.python.org/')
# brower.back()
# time.sleep(1)
# brower.forward()
# brower.close()


# # 10,cookie操作
# brower.get('https://www.zhihu.com/explore')
# print(brower.get_cookies())
# brower.add_cookie({"name": "cjt", "age": 24, "value": "321"})
# print(brower.get_cookies())
# print(brower.delete_all_cookies())
# print(brower.get_cookies())

# 11,选项卡管理
# brower.get('https://www.baidu.com')
# brower.execute_script('window.open()')
# print(brower.window_handles)
# brower.switch_to.window(brower.window_handles[1])
# brower.get("https://www.taobao.com")
# time.sleep(1)
# brower.switch_to.window(brower.window_handles[0])
# brower.get("https://python.org")

# 12,异常处理
try:
    brower.get("http://www.baaidu.com")
except TimeoutException:
    print("time out")

try:
    brower.find_element_by_class_name('class')
except NoSuchElementException:
    print("no such element")
finally:
    brower.close()
