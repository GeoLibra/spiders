# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from lxml import etree
import re
import json
from dianping.items import DianpingItem
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
    def parseShopList(self,response):
        # print("sadadad",response.request.headers)
        # shoplist=response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a/@*[name()="href" or name()="title"]').extract()

        shopList=response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a/@href').extract()
        # 当前页码
        cur_page=response.xpath('//div[@class="page"]/a[@class="cur"]/text()').extract()
        print(cur_page)
        if len(cur_page)==0 or cur_page[0]!="1":
            # 只有一页或者有多页但当前不在第一页,此时解析店铺页面
            for shop in shopList:
                yield Request(shop, callback=self.parseShop)

        else:
            # 有多页,且第一页,获取所有的页面url
            pageList = response.xpath('//div[@class="page"]/a/@href').extract()
            print(pageList)
            for page in pageList:
                yield Request(page, callback=self.parseShopList)
    def parseShop(self,response):
        shop_info = re.findall('window.shop_config=(.*?)</script>', response.text, re.S)

        shop_info = json.dumps(shop_info[0])
        shop_info=json.loads(shop_info)
        # title=response.xpath('//*[@id="basic-info"]/h1/text()').extract()
        # address=response.xpath('//*[@id="address"]/text()').extract()
        star=response.xpath('//*[@id="basic-info"]/div[1]/span[1]/@title').extract()
        reviewCount=response.xpath('//*[@id="reviewCount"]/text()').extract()
        price=response.xpath('//*[@id="avgPriceTitle"]/text()').extract()
        flavor=response.xpath('//*[@id="comment_score"]/span[1]/text()').extract()
        environment=response.xpath('//*[@id="comment_score"]/span[2]/text()').extract()
        service=response.xpath('//*[@id="comment_score"]/span[3]/text()').extract()
        comm=response.xpath('//*[@id="summaryfilter-wrapper"]/div/label/span/text()').extract()
        print(star,reviewCount,price,flavor,environment,service,comm)
        item=DianpingItem()
        item['shop_info']=shop_info
        return item