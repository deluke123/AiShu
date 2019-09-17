# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TravelItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content_info = scrapy.Field()
    article_url = scrapy.Field()
    spider_type = scrapy.Field()
    scrawl_time = scrapy.Field()
    source = scrapy.Field()
    type = scrapy.Field()
