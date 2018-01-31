# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # 书名
    name = scrapy.Field()
    # 大分类
    big_category = scrapy.Field()
    # 大分类url
    big_category_link = scrapy.Field()
    # 小分类
    small_category = scrapy.Field()
    # 小分类链接
    small_category_link = scrapy.Field()
    # 封面url
    cover_link = scrapy.Field()
    # 详情页面的url
    detail_url = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 出版社
    publisher = scrapy.Field()
    # 时间
    pub_date = scrapy.Field()
    # 价格
    price = scrapy.Field()

    pass
