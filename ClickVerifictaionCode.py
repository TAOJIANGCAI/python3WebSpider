from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from spider.chaojiying import Chaojiying
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from PIL import Image
from io import BytesIO
from selenium.webdriver import ActionChains

CHAOJIYING_USERNAME = 'ccjjtt'
CHAOJIYING_PASSWORD = ''
CHAOJIYING_SOFT_ID = 898900
CHAOJIYING_KIND = 9102


class ClickVerificationCode(object):
    def __init__(self):
        self.url = "https://auth.geetest.com/login/"
        self.brower = webdriver.Chrome()
        self.wait = WebDriverWait(self.brower, 20)
        self.mail = "826907729@qq.com"
        self.password = ""
        self.chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)

    def __del__(self):
        self.brower.close()

    def open(self):
        """
        打开网页输入用户名密码
        :return:
        """
        self.brower.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@type="email"]')))
        password = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@type="password"]')))
        email.send_keys(self.mail)
        password.send_keys(self.password)

    def get_click_button(self):
        """
        获取初始验证按钮
        :return:
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button

    def get_click_element(self):
        """
        获得验证图片对象
        :return:
        """
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_widget')))
        return element

    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        element = self.get_click_element()
        time.sleep(2)
        location = element.location
        size = element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获得网页截图
        :return:
        """
        screenshot = self.brower.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_click_image(self, name="captcha.png"):
        """
        获取验证码图片
        :param name:
        :return:
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def get_result(self, captcha_result):
        """
        解析识别结果
        :param captcha_result:
        :return:
        """
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click_words(self, locations):
        """
        点击验证图片
        :param location: 点击的位置
        :return:
        """
        for location in locations:
            print(location)
            ActionChains(self.brower).move_to_element_with_offset(self.get_touclick_element(), location[0],
                                                                  location[1]).click().perform()
            time.sleep(1)

    def touch_click_verify(self):
        """
        点击验证按钮
        :return: None
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_commit_tip')))
        button.click()

    def login(self):
        """
        登录
        :return: None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@type="button"]')))
        submit.click()
        time.sleep(10)
        print('登录成功')

    def crack(self):
        self.open()

        # 获取验证按钮
        button = self.get_click_button()
        button.click()

        # 获取验证码图片
        image = self.get_click_image()
        bytes_arry = BytesIO()
        image.save(bytes_arry, format('PNG'))

        # 识别验证码
        result = self.chaojiying.post_pic(bytes_arry.getvalue(), CHAOJIYING_KIND)
        print(result)

        locations = self.get_result(result)
        self.touch_click_words(locations)
        self.touch_click_verify()
        success = self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
        print(success)

        if not success:
            self.crack()
        else:
            self.login()


if __name__ == "__main__":
    crack = ClickVerificationCode()
    crack.crack()
