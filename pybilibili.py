from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os


class PyBilibili:
    def __init__(self):
        self.dir = r'C:\Users\{user}\AppData\Local\Google\Chrome\User Data'.format(user=os.getlogin())
        assert os.path.exists(self.dir)

        self.options = Options()
        self.options.add_argument('user-data-dir={dir}'.format(dir=self.dir))
        # self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.options)
        driver = self.driver
        driver.get('https://www.bilibili.com')


if __name__ == '__main__':
    pb = PyBilibili()