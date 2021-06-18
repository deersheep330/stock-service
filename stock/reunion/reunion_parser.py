import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class ReunionParser():

    def __init__(self):
        self.url = 'https://www.cmoney.tw/follow/channel/hot-stock'
        self.xpath = "//*[contains(@id, 'ItemList')]//*[contains(@id, 'Item_')]//*[contains(@class, 'text')]//*[contains(@href, '/follow/channel/stock-')]"
        self.num_xpath = "//*[contains(@id, 'ItemList')]//*[contains(@id, 'Item_')]//*[contains(@class, 'text')]//a[not(@href)]"
        self.list = []
        self.num_list = []

    def parse(self):
        print(f'==> parse page: {self.url}')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

        driver.get(self.url)
        WebDriverWait(driver, 15).until(
            expected_conditions.presence_of_element_located((By.XPATH, self.xpath))
        )
        elements = driver.find_elements_by_xpath(self.xpath)

        pattern = re.compile(r'\([^)]+\)')
        for ele in elements:
            #print(ele.text)
            arr = pattern.findall(ele.text)
            if arr is not None and len(arr) > 0:
                self.list.append(arr[0][1:-1])
            #print(self.list[-1])

        nums = driver.find_elements_by_xpath(self.num_xpath)
        for num in nums:
            _num = int(num.text.replace(',', ''))
            self.num_list.append(_num)

        driver.quit()
