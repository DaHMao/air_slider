from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from PIL import Image
import random
import numpy as np


class GOODLuck(object):
    def __init__(self, dataInfo):
        self.loginName = dataInfo["loginUser"]
        self.passWord = dataInfo["loginPwd"]
        self.res = ""

    def web_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_argument("headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get("https://passport.juneyaoair.com/?backUrl=http://www.juneyaoair.com/index.aspx")
        # 输入用户名以及密码
        self.driver.find_element_by_id("accountName").send_keys(self.loginName)
        time.sleep(random.randint(1, 3) / 10)
        self.driver.find_element_by_id("pwd").send_keys(self.passWord)
        time.sleep(random.randint(1, 3) / 10)
        # 点击登录
        self.driver.find_element_by_id("checkbox-account").click()
        self.driver.find_element_by_id("accountLoginBtn").click()
        time.sleep(3)

    def match_source(self, quekouimg):
        list = []
        for i in range(1, 5):
            list.append(Image.open(f'img/{i}.png'))
        for img in list:  # 循环遍历图片列表，用缺口图匹配完整图
            pixel1 = quekouimg.getpixel((250, 140))  # 取两张图相同的位置，去RGB值比较
            pixel2 = img.getpixel((250, 140))
            if abs(pixel1[1] - pixel2[1]) < 20 and abs(pixel1[2] - pixel2[2]) < 20:  # 比较值小于5返回完整图
                return self.get_diff_location(img, quekouimg)

    def get_diff_location(self, sourceimg, quekouimg):  # 找出缺口位置，
        judge = 40
        # sourceimg.show()
        # quekouimg.show()
        for i in range(70, 259):
            for j in range(0, 159):
                pixel1 = quekouimg.getpixel((i, j))
                pixel2 = sourceimg.getpixel((i, j))
                print(pixel1, pixel2)
                if abs(pixel1[2] - pixel2[2]) >= judge and abs(pixel1[1] - pixel2[1]) >= judge and abs(
                        pixel1[0] - pixel2[0]) >= judge:
                    print(i, j)
                    return i
        return -1

    def downloadimg(self):
        time.sleep(0.20)
        auth_code = self.driver.find_element_by_class_name("geetest_canvas_slice")
        self.driver.get_screenshot_as_file('bg.png')
        left = int(auth_code.location['x'])
        top = int(auth_code.location['y'])
        right = int(auth_code.location['x'] + auth_code.size['width'])
        bottom = int(auth_code.location['y'] + auth_code.size['height'])
        im = Image.open('bg.png')
        im = im.crop((left, top, right, bottom))

        # 形成图片且保存在本地*
        imgname = time.time()
        dir_path = './image'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        im.save(f'{dir_path}/{imgname}.png')
        return im

    def slider_v(self, i):
        print(i)
        slider = self.driver.find_element_by_class_name("geetest_slider_button")
        mouse = ActionChains(self.driver)
        rand_num = random.randint(20, 25)
        rand_num2 = random.choice([round(random.uniform(-3, -1), 3), round(random.uniform(1, 3), 3)])
        print("rand_num2:", rand_num2)
        get_list5 = self.get_track5(int(i) + rand_num - 7 + rand_num2, 0.5)  # 7 /10
        r_list = self.get_track1(rand_num)  # 超过距离生成变加速-变减速运动轨迹列表
        res_list = []
        for rand in r_list:
            res_list.append(rand - rand * 2)
        time.sleep(0.7)
        mouse.click_and_hold(slider).perform()  # 点击并不放
        for x in get_list5:
            mouse.reset_actions()
            mouse.move_by_offset(xoffset=x, yoffset=random.randint(-1, 5)).perform()

        mouse.reset_actions()
        time.sleep(random.randint(1, 3) / 10)
        mouse.perform()

        for i in res_list:  # 超过距离往回运动
            mouse.reset_actions()
            mouse.move_by_offset(xoffset=i, yoffset=random.randint(-1, 3)).perform()

        time.sleep(random.randint(1, 3) / 10)
        mouse.reset_actions()
        mouse.release().perform()
        mouse.perform()

    # 变加速 + 变减速运动轨迹
    def get_track1(self, distance):
        """
        根据偏移量和手动操作模拟计算移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        tracks = []
        # 当前位移
        current = 0

        # 减速阈值
        mid = distance * 7 / 8
        beyond = random.random() < 1
        # 时间间隔
        t = 0.2
        # 初始速度
        v = 0
        while current < distance:
            if current < mid:
                a = round(random.uniform(10, 12), 2)
            else:
                a = -round(random.uniform(12.5, 13.5), 2)
            v0 = v
            v = v0 + a * t  # 末速度等于初始速度+加速度*时间
            x = v0 * t + 1 / 2 * a * t * t
            current += round(x)
            tracks.append(round(x))
            if current > distance:
                overflow = current - distance
                tracks[-1] = tracks[-1] - overflow
                break
        if beyond:
            beyond_x = random.randint(1, 2)
            tracks.append(beyond_x)
            tracks.append(-beyond_x)

        return tracks

    def get_track5(self, distance, seconds):
        """
        根据轨迹离散分布生成的数学 生成
        :param distance: 缺口位置
        :param seconds:  时间
        :param ease_func: 生成函数
        :return: 轨迹数组
        """
        # ss = random.randint(1, 3)
        tracks = [0]
        offsets = [0]
        for t in np.arange(0.0, seconds, 0.1):  # 从0.0开始以0.1的为单位到seconds，t输出
            # if ss == 1 or ss == 3:
            ease = 1 - pow(1 - t / seconds, 4)  # 11  12 11 18 12
            # else:
            #     ease = 1 - pow(2, -10 * t / seconds)  # 20 18 16
            offset = round(ease * distance)
            tracks.append(offset - offsets[-1])
            offsets.append(offset)
        return tracks

    def main(self):
        self.web_driver()
        quekouimg = self.downloadimg()
        i = self.match_source(quekouimg=quekouimg)
        if i != -1:
            self.slider_v(i)
            time.sleep(1)


if __name__ == '__main__':
    data = {
        'loginUser': '13094928712',
        'loginPwd': '1234568@',
    }
    spi = GOODLuck(data)
    spi.main()
