# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from lxml import etree
import re
class DpspiderSpider(scrapy.Spider):
    name = 'dpSpider' # 爬虫名称
    allowed_domains = [] # 搜索的域名范围,规定爬虫只爬取这个域名下的网页
    start_urls = ['http://www.dianping.com/shenzhen']

    def parse(self, response):
        # 类别名称
        class_names = response.xpath('//*[@id="nav"]/div/ul/li/div[1]/span/a[1]/text()').extract()
        class_urls = response.xpath('//*[@id="nav"]/div/ul/li/div[1]/span/a[1]/@href').extract()
        for i in range(0,len(class_urls)):
            # print(class_names[i])
            yield Request(class_urls[i], callback=self.parseClass)
            break


    # 解析每一个类对应内容
    def parseClass(self,response):
        place = re.findall('<div class="fpp_business">(.*?)</div>', response.text, re.S)
        dish = re.findall('<div class="fpp_cooking">(.*?)</div>', response.text, re.S)

        place_selector = etree.HTML(place[0])
        dish_selector = etree.HTML(dish[0])
        # url=selector.xpath('//dl/dt/a/@href')
        # name=selector.xpath('//dl/dt/a/text()')
        # print(url)
        # print(name)
        # 地点
        place_urls = place_selector.xpath('//dl/dd/ul/li/a/@href')
        place_names = place_selector.xpath('//dl/dd/ul/li/a/text()')
        # 菜系
        dish_urls = dish_selector.xpath('//ul/li/a/@href')
        dish_names = dish_selector.xpath('//ul/li/a/text()')
        # print(place_urls)
        # print(place_names)
        # print(dish_urls)
        # print(dish_names)
        for place_url in place_urls:
            p_url=place_url.split('/')
            for dish_url in dish_urls:
                d_url=dish_url.split('/')
                url=self.start_urls[0]+'/'+p_url[-2]+'/'+d_url[-1]+p_url[-1]
                print(place_names[place_urls.index(place_url)],dish_names[dish_urls.index(dish_url)])
                yield Request(url, callback=self.parseShopList)
                break
            break
    def parseShopList(self,response):
        # shoplist=response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a/@*[name()="href" or name()="title"]').extract()

        shopList=response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a/@href').extract()
        # 页码
        pageList=response.xpath('//div[@class="page"]/a/@href')
        if pageList:
            pass
