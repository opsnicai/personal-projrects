# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AcfunspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # data = {}
    video_link = scrapy.Field()
    video_cover = scrapy.Field()
    video_title = scrapy.Field()
    video_up = scrapy.Field()
    video_view_count = scrapy.Field()
    video_create_time = scrapy.Field()
    # pass
