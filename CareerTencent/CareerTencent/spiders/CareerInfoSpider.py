# -*- coding: utf-8 -*-
import scrapy, queue, time, requests, re, logging
from ..items import CareertencentItem
from scrapy.http import HtmlResponse

from selenium import webdriver

logger = logging.getLogger(__name__)


class CareerinfospiderSpider(scrapy.Spider):
    name = 'CareerInfoSpider'
    allowed_domains = ['careers.tencent.com']
    start_urls = ['https://careers.tencent.com/search.html?index=10']

    pages = queue.Queue(1)
    pages.put(start_urls[0])

    def parse(self, response):
        opt = webdriver.ChromeOptions()
        opt.set_headless()
        # opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(chrome_options=opt)
        driver.maximize_window()
        driver.get(self.pages.get())
        time.sleep(1)
        container = driver.find_element_by_class_name("container")
        info_list = container.find_elements_by_xpath(r'.//div[@class = "recruit-list"]')
        logger.warning("当前页面：%s" % (driver.current_url,))
        for info in info_list:
            item = CareertencentItem()
            # driver.execute_script('window.scrollBy(0,500)')
            # 滑动页面到指定元素
            driver.execute_script("arguments[0].scrollIntoView();", info)
            driver.execute_script('window.scrollBy(0,-160)')

            # time.sleep(1)
            item["title"] = info.find_element_by_xpath(r'.//a/h4').text
            item["businessgroup"] = info.find_element_by_xpath(r'.//a/p[1]/span[1]').text
            item["city"] = info.find_element_by_xpath(r'.//a/p[1]/span[2]').text
            item["type"] = info.find_element_by_xpath(r'.//a/p[1]/span[position() > 2 and position() < last()]').text
            item["recruit_date"] = info.find_element_by_xpath(r'.//a/p[1]/span[last()]').text

            item["job_info"] = info.find_element_by_xpath(r'.//a/p[2]').text

            j,f = 0,True
            while j < 3 and f:
                try:
                    info.find_element_by_xpath(r'.//a[@class = "recruit-list-link"]/p[@class = "recruit-tips"]').click()
                    f = False
                    time.sleep(1)
                    driver.switch_to_window(driver.window_handles[-1])

                    # re.S 使 . 匹配换行符
                    patten = re.compile(r'工作要求\s(.*?)\s申请岗位', re.S)
                    item["link"] = driver.current_url
                    i, flag = 0, True
                    while i < 3 and flag:
                        try:
                            item["job_requirement"] = patten.findall(driver.find_element_by_class_name("container").text)[0]
                            flag = False
                            driver.close()
                        except Exception as e:
                            flag = True
                            logger.error("job_requirement : %s refetching..." % (e,))
                            driver.refresh()
                            time.sleep(1)
                            item["job_requirement"] = driver.current_url
                        i += 1
                except Exception as e:
                    logger.error("无法点击：%s,子页面：%s,刷新中" % (e,driver.current_url,))
                    time.sleep(1)
                    driver.refresh()
                    # time.sleep(1)
                    # info.find_element_by_xpath(r'.//').click()
                j += 1



            yield item
            # time.sleep()
            driver.switch_to_window(driver.window_handles[0])

        # 滑动页面至指定元素
        nextpage = container.find_element_by_xpath(
            r'.//div[@class = "main max-center g-clr"]//ul[@class = "page-list"]')
        driver.execute_script("arguments[0].scrollIntoView();", nextpage)

        try:
            # 下一页
            nextpage.find_element_by_xpath(r'.//li[@class = "next"]').click()
        except Exception as e:
            nextpage.find_element_by_xpath(r'.//li[@class = "page-li active"]/following-sibling::*[1]').click()
        time.sleep(1)
        driver.switch_to_window(driver.window_handles[-1])

        self.pages.put(driver.current_url)

        driver.window_handles.clear()

        time.sleep(1)
        yield scrapy.Request(driver.current_url, callback=self.parse)
        driver.quit()
