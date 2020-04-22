# -*- coding: utf-8 -*-
import scrapy, time,queue
from ..items import AcfunspiderItem
from selenium import webdriver


class VideoinfoSpider(scrapy.Spider):
    name = 'videoInfo'
    allowed_domains = ['www.acfun.cn']
    start_urls = ['https://www.acfun.cn/search?sortType=2&channelId=0&type=video&keyword=python']
    pages = queue.Queue(1)
    pages.put(start_urls[0])

    # findLink = re.compile(r'<a href="(\S*?)" target="_blank"')
    # find_cover = re.compile(r'<img src="(\S*?)" alt')
    # find_title = re.compile(r'''<div class="video__main__title ellipsis2"><a.*?\'>(.*?)</a>''')
    # find_up = re.compile(r'UP：<span class="user-name">(.*?)</span>')
    # find_view_count = re.compile(r'<span class="info__view-count">(.*?)</span>')
    # find_create_time = re.compile(r'<span class="info__create-time">(.*?)</span>')

    # scrapy会请求 start_urls 中的 url，该函数用来处理响应
    def parse(self, response):
        # <class 'scrapy.selector.unified.SelectorList'> scrapy 自己定义的列表
        # text = response.xpath(r'//div[@class = "search-video-card"]//text()')
        # print(type(text))
        # <class 'list'>
        # text = text.extract()
        # print(type(text))
        # //*[@id="video-list"]/div[2]/div[4]

        video_cards = response.xpath(r'//div[@class = "search-video-card"]')

        # 将每条数据以字符串格式 提取出来，用于正则匹配
        # video_cards = response.xpath(r'//div[@class = "search-video-card"]').extract()
        # data is str
        # data = video_cards.get()
        for i in range(len(video_cards)):
            # # extract()[0]
            # Xpath 规则，必须指明 . 表示当前这一层级
            item = AcfunspiderItem()
            # item["video_link"] = "https://www.acfun.cn" + video_cards[i].xpath(
            #     r'.//div[@class = "video__cover"]/a/@href').extract_first()
            item["video_link"] = response.urljoin(
                video_cards[i].xpath(r'.//div[@class = "video__cover"]/a/@href').extract_first())
            item["video_cover"] = video_cards[i].xpath(r'.//div[@class = "video__cover"]/a/img/@src').extract_first()
            item["video_title"] = video_cards[i].xpath(
                r'.//div[@class = "video__main__title ellipsis2"]/a/text()').extract_first()
            item["video_up"] = video_cards[i].xpath(r'.//span[@class = "user-name"]/text()').extract_first()
            item["video_view_count"] = video_cards[i].xpath(
                r'.//div[@class = "video__main__info"]//span[@class = "info__view-count"]/text()').extract_first()
            item["video_create_time"] = video_cards[i].xpath(
                r'.//span[@class = "info__create-time"]/text()').extract_first()

            # video_link = self.findLink.findall(video_cards[i])[0]
            # video_title = self.find_title.findall(video_cards[i])[0]
            # video_cover = self.find_cover.findall(video_cards[i])[0]
            # video_up = self.find_up.findall(video_cards[i])[0]
            # video_view_count = self.find_view_count.findall(video_cards[i])[0]
            # video_create_time = self.find_create_time.findall(video_cards[i])[0]
            #  Spider must return Request, BaseItem, dict or None,
            yield item


        # 模拟点击，获得下一页url
        opt = webdriver.ChromeOptions()
        # 无窗口模式
        opt.set_headless()
        # 不输出日志
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=opt)
        driver.get(self.pages.get())
        time.sleep(2)

        try:
            driver.find_element_by_xpath(
                r'/html/body/div[3]/div[4]/div[2]/div/div[4]/div//a[@class = "pager__btn pager__btn__next"]').click()
        except Exception as e:
            # print(e)
            pass
        next_page_url = driver.current_url
        print(driver.current_url)
        self.pages.put(driver.current_url)

        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            print("Done!")
