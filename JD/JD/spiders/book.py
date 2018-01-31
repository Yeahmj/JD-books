# -*- coding: utf-8 -*-
import scrapy
import json
from JD.items import JdItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['jd.com', '3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        # 获取所有大分类节点列表
        big_categroy_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt/a')
        # print(len(big_categroy_list))

        # 遍历所有的大节点列表
        for big_node in big_categroy_list[:1]:
            big_category = big_node.xpath('./text()').extract_first()
            big_category_link = 'https:' + big_node.xpath('./@href').extract_first()

            # 获取同胞节点的xpath
            node_list = big_node.xpath('../following-sibling::dd/em/a')
            for node in node_list[:1]:
                temp = {}
                temp['big_category'] = big_category
                temp['big_category_link'] = big_category_link
                temp['small_category'] = node.xpath('./text()').extract_first()
                temp['small_category_link'] = 'https:' + node.xpath('./@href').extract_first()
                # print(temp)

                # 点击小分类，进入到小分类的搜过结果列表页面
                yield scrapy.Request(
                    temp['small_category_link'],
                    callback=self.parse_book_list,
                    meta={'meta_1':temp}
                )

    def parse_book_list(self,response):
        temp = response.meta['meta_1']
        # print(temp['big_category'])

        # print(temp)

        # 获取所有图书节点
        book_list = response.xpath('//*[@id="plist"]/ul/li/div')
        # print(len(book_list))

        # 编列所有的图书节点列表
        for book in book_list:
            # 构建item实例
            item = JdItem()

            # 抽取数据
            item['big_category'] = temp['big_category']
            item['big_category_link'] = temp['big_category_link']
            item['small_category'] = temp['small_category']
            item['small_category_link'] = temp['small_category_link']

            item['name'] = book.xpath('./div[3]/a/em/text()').extract_first()
            item['cover_link'] = 'https:' + book.xpath('./div[1]/a/img/@src').extract_first()
            item['detail_url'] =  'https:'+ book.xpath('./div[1]/a/@href').extract_first()
            item['author'] = book.xpath('./div[4]/span[1]/span/a/text()').extract_first()
            item['publisher'] = book.xpath('/div[4]/span[2]/a/text()').extract_first()
            item['pub_date'] = book.xpath('./div[4]/span[3]/text()').extract_first()
            # item['price'] = book.xpath('./div[4]/span[3]/text()').extract_first()

            # 构建价格请求
            skuid = book.xpath('./@data-sku').extract_first()
            if skuid is not None:
                url = 'https://p.3.cn/prices/mgets?skuIds=J_' + skuid
                yield scrapy.Request(
                    url,
                    callback=self.parse_price,
                    meta={'meta_2':item}
                )

    def parse_price(self,response):
        item = response.meta['meta_2']
        dict_data = json.loads(response.text)
        item['price'] = dict_data[0]['op']
        # print(item)
        yield item

