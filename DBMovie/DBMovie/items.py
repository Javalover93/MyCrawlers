# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DbmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    actors =scrapy.Field()
    genre = scrapy.Field()
    production_region = scrapy.Field()
    language = scrapy.Field()
    show_time = scrapy.Field()
    duration = scrapy.Field()
    IMDb_link = scrapy.Field()
    rating = scrapy.Field()
    rate_number = scrapy.Field()
