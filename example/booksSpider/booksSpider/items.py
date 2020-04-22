# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 用于封装数据
class BooksspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # pass

    # scrapy 定义的 Item类，用于对数据进行封装
    # 这里定义的 变量 相当于 字典中的 键
    # BookSpider.py 则要导入该包，并将数据导入
    # Book = BooksspiderItem()
    # Book["name"] = ...
    name = scrapy.Field()
    link = scrapy.Field()
    rating_star = scrapy.Field()
    price = scrapy.Field()
    cover = scrapy.Field()
