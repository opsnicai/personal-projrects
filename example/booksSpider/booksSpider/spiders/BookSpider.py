# -*- coding: utf-8 -*-
import scrapy
from ..items import BooksspiderItem

class BookspiderSpider(scrapy.Spider):
    name = 'BookSpider'
    # allowed_domains = ['http://books.toscrape.com/']
    start_urls = ['http://books.toscrape.com/']

    # response 方法：
    # extract 将 response 中的 text/string 提取出来，返回列表；extract_first()则返回列表第一项
    # re 正则匹配，返回列表
    # re_first() 返回匹配的列表中的第一项
    def parse(self, response):
        bookinfo = BooksspiderItem()
        # <article class="product_pod">
        for book in response.css("article.product_pod"):
            bookinfo["name"] = book.xpath('./h3/a/@title').extract_first()

            bookinfo["link"] = response.urljoin(book.xpath('./h3/a/@href').extract_first())
            # <p class="price_color">£51.77</p>
            bookinfo["price"] = book.css('p.price_color::text').extract_first()

            #
            bookinfo["rating_star"] = book.xpath(r'./p/@class').extract_first().split()[-1]

            # div a href
            bookinfo["cover"] = response.urljoin(book.css(r'div.image_container a img::attr(src)').extract_first())

            yield bookinfo

        next_page = response.css(r'ul.pager li.next a::attr(href)').extract_first()
        if next_page:
            # 如果找得到下一页，得到绝对路径，构造新的request 对象
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
