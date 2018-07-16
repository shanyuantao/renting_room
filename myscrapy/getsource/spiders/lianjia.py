# -*- coding: utf-8 -*-
from scrapy import Selector
import scrapy
from time import sleep
# from scrapy.linkextractors.sgml import SgmlLinkExtractor
# from scrapy.spiders import Rule, CrawlSpider
# from scrapy.linkextractors import LinkExtractor
from getsource.items import CrawlSpiderItem


class LianjiaSpider(scrapy.Spider):

    name = 'lianjia'
    allowed_domains = ['cd.lianjia.com']
    # start_urls = ['https://cd.lianjia.com/zufang/']

    # rules = (
    #     Rule(LinkExtractor(allow=(r'pg\d+/')), follow=True),
    #     Rule(LinkExtractor(allow=(r'\d+.html')), callback='parse_item')
    # )
    def start_requests(self):
        base_url  = 'https://cd.lianjia.com/zufang/'
        for i in range(101):
            # sleep(15)
            full_url = base_url + 'pg%s' % i
            yield scrapy.Request(url=full_url, callback=self.parse_item)



    def parse_item(self, response):

        sel = Selector(response)
        goods_list = sel.xpath('//*[@id="house-lst"]/li/div[2]/h2/a/@href').extract()
        for url in goods_list:
            # sleep(1)
            yield scrapy.Request(url, callback=self.parse_mypage)


    def parse_mypage(self, response):

        sel = Selector(response)
        item = CrawlSpiderItem()
        item['title'] = sel.xpath('//h1/text()').extract_first()
        item['price'] = sel.xpath('/html/body/div[4]/div[2]/div[2]/div[1]/span[1]/text()').extract_first()
        item['area'] = sel.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[1]/text()').re('\d+')[0]
        item['house_type'] = \
        sel.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[2]/text()').extract_first().split(' ')[0]
        item['floor'] = sel.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[3]/text()').extract_first()
        item['house_head'] = sel.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[4]/text()').extract_first()
        item['metro'] = sel.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[5]/text()').extract_first()
        item['community'] = sel.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[6]/a[1]/text()').extract_first()
        item['position'] = sel.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[7]/a[1]/text()').extract_first()
        item['real_position'] = sel.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[7]/a[2]/text()').extract_first()
        item['community_introduce'] = sel.xpath(
            '//*[@id="introduction"]/div/div[2]/div[2]/div[3]/ul/li[1]/span[2]/text()').extract_first()
        item['transportation'] = sel.xpath(
            '//*[@id="introduction"]/div/div[2]/div[2]/div[3]/ul/li[2]/span[2]/text()').extract_first()
        item['surround_facility'] = sel.xpath(
            '//*[@id="introduction"]/div/div[2]/div[2]/div[3]/ul/li[3]/span[2]/text()').extract_first()

        item['public_time'] = sel.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[8]/text()').extract_first()
        item['publisher_name'] = sel.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[3]/div/div[1]/a[1]/text()').extract_first()
        item['publisher_img_url'] = sel.xpath('/html/body/div[4]/div[2]/div[2]/div[3]/a/img/@src').extract_first()
        item['publisher_id'] = sel.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[3]/div/div[1]/span/text()').extract_first()
        item['publisher_evaluate'] = '-'.join(
            sel.xpath('/html/body/div[4]/div[2]/div[2]/div[3]/div/div[2]/span[1]/text()').re(':(.*)/'))
        item['evaluate_num'] = '-'.join(
            sel.xpath('/html/body/div[4]/div[2]/div[2]/div[3]/div/div[2]/span[1]/a/text()').re(r'\d+'))
        item['publisher_with_checking'] = '-'.join(
            sel.xpath('/html/body/div[4]/div[2]/div[2]/div[3]/div/div[2]/span[2]/text()').re(r"\d+"))
        item['phone_number'] = '-'.join(
            sel.xpath('/html/body/div[4]/div[2]/div[2]/div[3]/div/div[3]/text()').re('\d+'))
        item['lease'] = sel.xpath(
            '//*[@id="introduction"]/div/div[2]/div[1]/div[2]/ul/li[1]/text()').extract_first()
        item['pay_way'] = '-'.join(
            sel.xpath('//*[@id="introduction"]/div/div[2]/div[1]/div[2]/ul/li[2]/text()').re(r'\w+'))
        item['house_state'] = sel.xpath(
            '//*[@id="introduction"]/div/div[2]/div[1]/div[2]/ul/li[3]/text()').extract_first()
        item['heating_method'] = sel.xpath(
            '//*[@id="introduction"]/div/div[2]/div[1]/div[2]/ul/li[4]/text()').extract_first()
        item['house_facility'] = [tem.strip() for tem in sel.css(
            '#introduction > div > div.introContent > div.feature > div.zf-tag > ul > li.tags::text').extract() if
                                  tem.strip()]
        # item['look_house_num'] = sel.xpath('//*[@id="record"]/div[2]/div[3]/span/text()').extract()
        item['pic_url'] = sel.xpath('//*[@id="topImg"]/div[2]/ul/li/img/@src').extract()
        yield item
        # return item
