import json
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Pinterest:
    def __init__(self, linux: bool):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        chromeOptions.add_argument("--no-sandbox")
        chromeOptions.add_argument("--disable-setuid-sandbox")

        chromeOptions.add_argument("--remote-debugging-port=9222")  # this

        chromeOptions.add_argument("--disable-dev-shm-using")
        chromeOptions.add_argument("--disable-extensions")
        chromeOptions.add_argument("--disable-gpu")
        chromeOptions.add_argument("start-maximized")
        chromeOptions.add_argument("disable-infobars")
        chromeOptions.add_argument(r"user-data-dir=.\cookies\\test")
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        if linux:
            self.driver = webdriver.Chrome('/root/pinterests/chromedriver', chrome_options=chromeOptions)
        else:
            self.driver = webdriver.Chrome()

    def login(self):
        try:
            self.driver.get("https://pinterest.com/login")

            wait_time = 0.2
            email = 'dxsuawguuzudgfctoz@upived.online'
            password = 'Abramlsk21'
            driver = self.driver
            WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.ID, 'email')))

            driver.find_element_by_id("email").send_keys(email)
            driver.find_element_by_id("password").send_keys(password)

            logins = driver.find_elements_by_xpath("//*[contains(text(), 'Log in')]")

            for login in logins:
                login.click()

            print('tut')
            wait_to_load = 30
            for i in range(wait_to_load):
                if driver.current_url == 'https://www.pinterest.com/':
                    return True
                time.sleep(2)
            return False

        except Exception as e:
            print(e)
            return False

    def get_pin_info_by_short_link(self, link):

        self.driver.get(link)
        url_temp = self.driver.current_url
        url_temp = url_temp[:str(url_temp).find('feedback')]
        self.driver.get(url_temp)

        if self.driver.current_url == 'https://www.pinterest.ru/?show_error=true':
            return

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        scripts = soup.findAll('script')
        print('len', len(scripts))
        pin_data = {}
        for s in scripts:
            if 'id' in s.attrs and s.attrs['id'] == 'initial-state':
                pinJsonData = json.loads(s.contents[0])['resources']['data']['PinResource']
                pinJsonData = pinJsonData[list(pinJsonData.keys())[0]]['data']
                pin_data = (pinJsonData)
                # return pinJsonData
                break
        data = pin_data['pinner']
        username = data['username']
        follower_count = data['follower_count']
        with open('link_username.txt', 'a') as f:
            f.write(f'{link},{username}\n')
        with open('username_followers_count.txt', 'a') as f:
            f.write(f'{username},{follower_count}\n')
