# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CoverBoxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    artistName = scrapy.Field()
    collectionName = scrapy.Field()
    artistViewUrl = scrapy.Field()
    store = scrapy.Field()
    input = scrapy.Field()
    collectionPrice = scrapy.Field()
    releaseDate = scrapy.Field()

class ImageItem(scrapy.Item):
	    # define the fields for your item here like:
	    # name = scrapy.Field()
    image_urls = scrapy.Field()
    Band = scrapy.Field()
    collectionName = scrapy.Field()
 
