# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CareertencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    businessgroup = scrapy.Field()
    city = scrapy.Field()
    type = scrapy.Field()
    recruit_date = scrapy.Field()
    job_info = scrapy.Field()
    job_requirement = scrapy.Field()
    # pass
