import requests, lxml, time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from scrapy.http import HtmlResponse


class Spider():
    url = "https://careers.tencent.com/search.html"
    DEFAULT_REQUEST_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
    }

    def fetch_content(self):
        opt = webdriver.ChromeOptions()
        # opt.set_headless()
        # opt.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(chrome_options=opt)
        driver.maximize_window()
        driver.get(self.url)
        time.sleep(2)
        # body > div
        container = driver.find_element_by_class_name("container")
        info_list = container.find_elements_by_xpath(r'.//div[@class = "recruit-list"]')
        for info in info_list:
            # print(info.find_element_by_xpath(r'./a/h4').text)
            try:
                info.find_element_by_class_name("recruit-list-link").click()
                # driver.switch_to_window(driver.window_handles[-1])
                # print(driver.current_url)
                # x1 = driver.find_element_by_class_name("container").text
                # print(x1)
            except Exception as e:
                print(e)
        #
        #     driver.switch_to_window(driver.window_handles[0])
        #     time.sleep(1)

        # /html/body/div/div[4]/div[3]/div[2]/div[3]/ul/li[10]
        # @class = "next"

        # driver.execute_script("arguments[0].scrollIntoView();", info_list)
        # info_list.click()
        # 滑动页面至指定元素
        # page = container.find_element_by_xpath(
        #     r'.//div[@class = "main max-center g-clr"]//ul[@class = "page-list"]')
        # driver.execute_script("arguments[0].scrollIntoView();", page)

        # /a/following-sibling::*  # a同级下所有标签
        # /a/following-sibling::*[1]  # a同级下第一个标签
        # /a/following-sibling::ul[1]  # a同级下第一个ul标签
        # preceding-sibling  # 选取当前节点之前的所有同级节点

        # nextpage = page.find_element_by_xpath(r'.//li[@class = "page-li active"]/following-sibling::*[1]')

        time.sleep(10)
if __name__ == "__main__":
    s = Spider()
    s.fetch_content()
