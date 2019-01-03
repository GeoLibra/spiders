# -*- coding: utf-8 -*-
import scrapy


class DpspiderSpider(scrapy.Spider):
    name = 'dpSpider' # 爬虫名称
    allowed_domains = [] # 搜索的域名范围,规定爬虫只爬取这个域名下的网页
    start_urls = ['http://www.dianping.com/']

    def parse(self, response):
        # 获取网站标题
        context = response.xpath('/html/head/title/text()')
        # 提取网站标题
        title = context.extract_first()
        print(title)
        pass
