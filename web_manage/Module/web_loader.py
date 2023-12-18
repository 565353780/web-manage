import os
from time import sleep

import requests
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tqdm import tqdm

from web_manage.Config.info import INFO

class WebLoader(object):
    def __init__(self, driver_path=None, url_key=None):
        self.headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        }

        self.driver_path = None
        self.url_info = None

        self.driver = None
        self.url = None
        self.xpath_dict = {}
        self.print_progress = False
        self.print_result = False
        self.wait_time = 0

        if driver_path is not None and url_key is not None:
            self.loadWeb(driver_path, url_key)
        return

    def reset(self):
        self.driver_path = None
        self.url_info = None

        self.driver = None
        self.url = None
        self.xpath_dict = {}
        self.print_progress = False
        self.print_result = False
        self.wait_time = 0
        return True

    def getRequestsResponse(self, url):
        response = requests.get(url, headers=self.headers)
        return response.text

    def getUrlLib3Response(self, url):
        http = urllib3.PoolManager()
        response = http.request('GET', url, headers=self.headers)
        return response.data

    def getResponse(self, url):
        response = self.getRequestsResponse(url)
        if response is not None:
            return response

        response = self.getUrlLib3Response(url)
        if response is not None:
            return response

        print('[ERROR][WebLoader::getResponse]')
        print('\t request the web failed!')
        return None

    def loadWebInfo(self):
        if self.print_progress:
            print('[INFO][WebLoader::loadWebInfo]')
            print('\t start load web info...')
            print('\t url:', self.url)

        response = self.getResponse(self.url)

        if response is None:
            print('[ERROR][WebLoader::loadWebInfo]')
            print('\t getResponse failed!')
            return False

        soup = BeautifulSoup(response)
        if self.print_progress:
            print('[INFO][WebLoader::loadWebInfo]')
            print('\t load web success! web info is:')
            print('-' * 20)
            print(soup.prettify())
            print('-' * 20)
        return True

    def startWebUI(self):
        if not os.path.exists(self.driver_path):
            print('[ERROR][WebLoader::openWeb]')
            print('\t the chrome driver not exist!')
            print('\t please install [chrome] and [chromedriver] first!')
            print('\t and then update the driver_path in:')
            print('\t\t ./web-manage/Demo/web_loader.py')
            print('\t and then re-run the demo.py script')
            return False

        chrome_options = ChromeOptions()

        chrome_options.add_argument('headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('enable-automation')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('enable-features=NetworkServiceInProcess')
        chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])

        service = Service(executable_path=self.driver_path)
        service.creationflags = 0x8000000
        try:
            self.driver = webdriver.Chrome(
                service=service, options=chrome_options)
        except Exception as e:
            print('[ERROR][WebLoader::startWebUI]')
            print('\t chrome can not open!')
            print(e)
            self.quitWeb()
            return False

        self.driver.set_window_size(1920, 1080)

        self.driver.get(self.url)
        return True

    def loadInfoValues(self):
        if self.url_info is None:
            return False

        self.url = self.url_info['url']
        self.xpath_dict = self.url_info['xpath_dict']
        self.print_progress = self.url_info['print_progress']
        self.print_result = self.url_info['print_result']
        self.wait_time = self.url_info['wait_time']
        return True

    def loadWeb(self, driver_path, url_key):
        if url_key not in INFO.keys():
            print('[ERROR][WebLoader::loadWeb]')
            print('\t url key not found!')
            print('\t valid url keys are:')
            print(INFO.keys())
            return False

        self.driver_path = driver_path
        self.url_info = INFO[url_key]

        self.loadInfoValues()

        self.loadWebInfo()

        self.startWebUI()
        return True

    def outputWebInfo(self):
        html_source = self.driver.page_source
        print('[INFO][WebLoader::outputWebInfo]')
        print('\t web info is:')
        print('-' * 20)
        print(html_source)
        print('-' * 20)
        return True

    def quitWeb(self):
        try:
            self.driver.quit()
        except Exception:
            pass
        return True

    def openTab(self, wait_time=0):
        js = "window.open('{}','_blank');"
        self.driver.execute_script(js.format(self.url))
        self.driver.switch_to.window(self.driver.window_handles[-1])
        if wait_time > 0:
            sleep(wait_time)
        return True

    def setValue(self, xpath, value):
        elem = self.driver.find_element(By.XPATH, xpath)
        self.driver.execute_script(
            "arguments[0].setAttribute('value',arguments[1])", elem, value)
        return True

    def clickButton(self, xpath):
        elem = self.driver.find_element(By.XPATH, xpath)
        elem.click()
        return True

    def getAlertText(self):
        try:
            alert = self.driver.switch_to.alert
        except:
            return 'Finished'
        text = alert.text
        alert.dismiss()
        return text

    def closeTab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        return True

    def runStep(self, teacher, page):
        self.openTab(self.wait_time)
        self.outputWebInfo()
        exit()
        self.setValue(self.xpath_dict['paper'], '')
        self.clickButton(self.xpath_dict['next_page'])
        # self.outputWebInfo()
        # exit()
        alert_text = self.getAlertText()
        if self.print_result:
            print(f' {alert_text} --> {teacher} {page}')
        success = alert_text not in ['用户名已存在', '邀请码无效']
        self.closeTab()
        return success

    def autoRun(self, teacher, page_num):
        success_num = 0

        print('[INFO][WebLoader::autoRun]')
        print('\t start auto run...')
        for i in tqdm(range(page_num)):
            success = self.runStep(teacher, i)
            if success:
                success_num += 1

        self.quitWeb()
        print('[INFO][WebLoader::autoReg]')
        print('\t auto reg finished! success num: ' +
              str(success_num) + '/' + str(page_num))
        return True
