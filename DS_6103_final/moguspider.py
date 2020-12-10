# -*- coding: utf-8 -*-
from time import sleep
from lxml import etree
import scrapy
import sys
sys.path.append("..")
from Mogu.items import MoguItem
from selenium import webdriver
from scrapy.http import Request

base_url = "https://shop.mogu.com/detail/"

class MoguSpider(scrapy.Spider):
    name = 'mogu'
    allowed_domains = ['mogujie.com']
    start_urls = ['https://www.mogujie.com/']

    def parse(self, response):
        item = MoguItem()
        mogu_urls = response.xpath("//div[@class='item-wrap']/div[1]//a[@class='cate-item-link']//@href").extract()

        for mogu_url in mogu_urls:
            # i+=1
            opt = webdriver.ChromeOptions()
            opt.add_argument('--headless')
            driver = webdriver.Chrome('/Users/zhouxueqi/Downloads/chromedriver')  # 创建驱动时从本地加载驱动文件路径
            driver.get(mogu_url)
            for i in range(50):
                distance = i * 1000
                js = 'document.documentElement.scrollTop=%d' % distance
                driver.execute_script(js)
                sleep(0.5)
                html = driver.page_source
                print(html)
                res = etree.HTML(html)
                goods_list = res.xpath('//div[@class="goods_list_mod clearfix J_mod_hidebox J_mod_show"]//div[@class="iwf goods_item ratio3x4"]')

                print(goods_list)
                for i in goods_list:

                    name = i.xpath(".//p[@class='title yahei fl']//text()")
                    print('-------------------')
                    item['name'] = name

                    price = i.xpath(".//a[3]/div/b//text()")
                    item['price'] = price

                    fav_num = i.xpath(".//a[3]/div/span/text()")
                    item['fav_num']=fav_num

                    indi_url = i.xpath("./a[2]//@href")
                    item['product_url'] = indi_url
                    yield item