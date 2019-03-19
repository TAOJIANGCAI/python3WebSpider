from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import time
from selenium.webdriver import ActionChains


class SlidVerificationCode(object):
    def __init__(self):
        self.url = "https://auth.geetest.com/login"
        self.brower = webdriver.Chrome()
        self.wait = WebDriverWait(self.brower, 20)
        self.mail = "826907729@qq.com"
        self.password = "95jiangtao121"
        self.BORDER = 6
        self.INIT_LEFT = 60

    def get_button(self):
        """
        获取初始验证码按钮
        :return:
        """
        return self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "geetest_radar_tip")))

    def get_screen_shot(self):
        """
        获取网页截图
        :return:
        """
        screen_shot = self.brower.get_screenshot_as_png()
        screen_shot = Image.open(BytesIO(screen_shot))
        return screen_shot

    def get_position(self):
        """
        获取验证码位置
        :return:验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))

        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)

    def get_slider(self):
        """
        获取滑块
        :return:
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_geetest_img(self, name='captcha.png'):
        """
        获取验证码图片
        :param name:
        :return:
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screen_shot()

        captcha = screenshot.crop(left, top, right, bottom)
        captcha.save(name)
        return captcha

    def open(self):
        """
        打开网站输入用户名和密码
        :return:
        """
        self.brower.get(self.url)
        eamil = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
        password = self.wait.until(EC.presence_of_element_located(By.ID, 'password'))
        eamil.send_keys(self.mail)
        password.send_keys(self.password)

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1:不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider:滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.brower).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.brower).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.brower).release().perform()

    def login(self):
        """
        登录
        :return:
        """
        sumbit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
        sumbit.click()
        time.sleep(10)
        print('login success')

    def crack(self):
        # 打开浏览器，输入用户名密码
        self.open()

        # 点击验证按钮
        button = self.get_button()
        button.click()

        # 获取初始验证码图片
        img1 = self.get_geetest_img('captcha1.png')

        # 点击呼出缺口
        slider = self.get_slider()
        slider.click()

        # 获取带缺口的验证码图片
        img2 = self.get_geetest_img('captcha2.png')

        # 获取缺口的位置
        gap = self.get_gap(img1, img2)
        print('缺口位置', gap)

        # 减去缺口位移
        gap -= self.BORDER

        # 获取移动轨迹
        track = self.get_track(gap)
        print('滑动轨迹', track)

        # 拖动滑块
        self.move_to_gap(slider, track)

        success = self.wait.until(EC.text_to_be_present_in_element(By.CLASS_NAME, 'geetest_success_radar_tip_content'),
                                  '验证成功')
        print(success)

        if not success:
            self.crack()
        else:
            self.login()


if __name__ == "__main__":
    sfc = SlidVerificationCode()
    sfc.crack()
