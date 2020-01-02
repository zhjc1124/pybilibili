from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
from time import sleep
from selenium.webdriver import ActionChains
import requests


class PyBilibili:
    def __init__(self, headless=True):

        options = Options()
        # options.set_headless(headless)

        self.judgement = 0
        chrome_dir = r'C:\Users\{user}\AppData\Local\Google\Chrome\User Data'.format(user=os.getlogin())
        # chrome_dir = 'profile'
        options.add_argument('user-data-dir={dir}'.format(dir=chrome_dir))

        # 添加插件
        # option.add_extension()
        self.driver = webdriver.Chrome(options=options, executable_path='driver/chromedriver.exe')

        self.driver.implicitly_wait(5)
    def wait(self, xpath, time=60):
        driver = self.driver
        WebDriverWait(driver, time).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    def get_silver(self):
        driver = self.driver
        driver.get('https://live.bilibili.com/5269')
        # self.mute()
        print('mute sucess')
        info_xpath = '//*[@id="bilibili-helper-treasure"]/div[1]/div'
        self.wait(info_xpath)
        while driver.find_element_by_xpath(info_xpath).text not in ['已领完', '领完啦']:
            pass


    def mute(self):
        driver = self.driver
        # 音量按钮
        mute_xpath = '//*[@id="js-player-decorator"]/div/div[6]/div/div/div[1]/div[3]/div/div[1]/button'

        # 等待页面加载完毕
        self.wait(mute_xpath)
        button_icon = driver.find_element_by_xpath(mute_xpath)

        # 判断是否已经静音
        if button_icon.get_attribute('data-title') == '静音':
            button_icon.click()

    def change_coin(self):
        driver = self.driver
        driver.get('https://live.bilibili.com/exchange')
        # 兑换按钮
        xpath = '//*[@id="silver-to-coin-btn"]'
        self.wait(xpath)
        self.click_xpath(xpath)
        message = driver.find_elements_by_class_name("m_layer")
        if message:
            message[0].click()

    def click_xpath(self, xpath):
        driver = self.driver
        driver.find_element_by_xpath(xpath).click()

    def judge(self):
        driver = self.driver
        sleep(10)
        print('inits')
        driver.get('https://www.bilibili.com/judgement/index')

        try: 
            close_class = 'dialog-close'
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, close_class)))
            close_button = driver.find_element_by_class_name(close_class)
            close_button.click()
        except:
            pass
        

        # 开始仲裁按钮
        begin_xpath = "//*[text()='开始众裁']"
        self.click_xpath(begin_xpath)
        print("点击开始众裁")
        # 下拉众议观点
        down_class = "down-arrow"
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, down_class)))
        except Exception:
            pass
        
        try:
            down_buttons = driver.find_elements_by_class_name(down_class)
            down_buttons[-1].click()
        except Exception:
            print("没有众议观点")
            info_xpath = '/html/body/div[2]/div/div[2]/div/div/div[1]/h3'
            info = driver.find_element_by_xpath(info_xpath).text
            if info == '真给力 , 移交众裁的举报案件已经被处理完了':
                return -1
            else:
                return 1
        print("点击下拉观点按钮")
        # 观点页码
        page_xpath = '/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[4]/div/div/div[2]'
        page = driver.find_element_by_xpath(page_xpath)
        l = page.find_elements_by_class_name('pag-l')
        r = page.find_elements_by_class_name('pag-r')

        # 计算哪个的观点多
        judge_value = -1
        l_page = 1
        r_page = 1
        if l:
            l_page = int(l[0].text.split('/')[-1])
        if r:
            r_page = int(r[0].text.split('/')[-1])

        # 观点多的直接封禁或者放弃
        if l_page > r_page:
            print("赞同观点多")
            judge_value = -1
        elif l_page < r_page:
            print("反对观点多")
            judge_value = 1
        # 中间状态
        else:
            print("中间观点多")
            # 支持观点
            cnt_left = '/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[4]/div/div/div[3]'
            left = driver.find_element_by_xpath(cnt_left)
            # 得到支持数
            pros = 0
            if left.text:
                pros = len(left.text.split())

            # 反对观点
            cnt_right = '/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[4]/div/div/div[4]'
            right = driver.find_element_by_xpath(cnt_right)
            # 得到反对数
            cons = 0
            if right.text:
                cons = len(right.text.split())

            # 比较
            if pros > cons:
                judge_value = -1
            elif pros < cons:
                judge_value = 1
            else:
                judge_value = 0
        if judge_value == 1:
            no_xpath = '/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[5]/div/div[1]/div/div[3]'
            self.wait(no_xpath)
            self.click_xpath(no_xpath)
            print("点击否")
        else:
            yes_xpath = '/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[5]/div/div[1]/div/div[1]'
            self.wait(yes_xpath)
            self.click_xpath(yes_xpath)
            x = '/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[5]/div/div[2]/div[2]/div[2]/div/div/div[3]/p/label[1]'
            if judge_value == 0:
                x = '/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[5]/div/div[2]/div[2]/div[2]/div/div/div[3]/p/label[2]'
            self.click_xpath(x)
            print("点击同意按钮")
        final_xpath = '/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[5]/div/div[2]/div[2]/div[3]/div/button'
        self.wait(final_xpath)
        self.click_xpath(final_xpath)
        print("返回上一级")
        # 正常返回0
        return 0

    def auto_judge(self):
        while True:
            print('judge')
            r = self.judge()
            # 已经审核完毕
            if r == -1:
                sleep(3600)
                print('sleep 3600')
            # 已达到今日审核上限
            elif r == 1:
                print('over')
                break


if __name__ == '__main__':
    pb = PyBilibili(headless=False)
    pb.change_coin()
    # auto_ssr('qwerty762@163.com', 'qwerty7620')
    pb.auto_judge()
    pb.get_silver()
    pb.driver.close()
