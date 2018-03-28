from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from os import getlogin
from os.path import exists
from time import sleep
from selenium.webdriver import ActionChains


class PyBilibili:
    def __init__(self):
        self.dir = r'C:\Users\{user}\AppData\Local\Google\Chrome\User Data'.format(user=getlogin())
        assert exists(self.dir)

        self.options = Options()
        self.options.add_argument('user-data-dir={dir}'.format(dir=self.dir))
        # self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.implicitly_wait(30)

    def get_silver(self):
        driver = self.driver
        driver.get('https://live.bilibili.com/5269')
        self.mute()
        sleep(55 * 60)

    def mute(self):
        driver = self.driver
        mute_xpath = '//*[@id="js-player-decorator"]/div/div[6]/div/div/div[1]/div[3]/div/div[1]/button'

        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, mute_xpath)))
        box_icon = driver.find_element_by_xpath(mute_xpath)

        if box_icon.get_attribute('data-title') == '静音':
            actions = ActionChains(driver)
            actions.move_to_element(box_icon)
            actions.click(box_icon)
            actions.perform()

    def change_coin(self):
        driver = self.driver
        driver.get('https://live.bilibili.com/exchange')
        change_icon = driver.find_element_by_xpath('//*[@id="silver-to-coin-btn"]')
        self.click(change_icon)

    def click(self, elem):
        actions = ActionChains(self.driver)
        actions.move_to_element(elem)
        actions.click(elem)
        actions.perform()


if __name__ == '__main__':
    pb = PyBilibili()
    pb.get_silver()
    pb.change_coin()

