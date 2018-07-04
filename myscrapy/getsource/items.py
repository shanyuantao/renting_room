# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlSpiderItem(scrapy.Item):

    title = scrapy.Field()  # 标题
    price = scrapy.Field()  # 房价
    area = scrapy.Field()  # 房屋面积
    house_type = scrapy.Field()  # 房型
    floor = scrapy.Field()  # 所处楼层
    house_head = scrapy.Field()  # 房屋朝向
    metro = scrapy.Field()  # 距离地铁
    community = scrapy.Field()  # 小区
    position = scrapy.Field()  # 大致区域
    real_position = scrapy.Field()  # 细致区域
    community_introduce = scrapy.Field()  # 小区介绍
    surround_facility = scrapy.Field()  # 周边配套
    transportation = scrapy.Field()  # 交通出行

    public_time = scrapy.Field()  # 发布时间
    publisher_name = scrapy.Field()  # 发布者
    publisher_img_url = scrapy.Field()  # 发布者头像url
    publisher_id = scrapy.Field()  # 发布者身份
    publisher_evaluate = scrapy.Field()  # 发布者评分
    evaluate_num = scrapy.Field()  # 评价人数
    publisher_with_checking = scrapy.Field()  # 本房带看人数
    phone_number = scrapy.Field()  # 联系方式
    # serial_number = scrapy.Field()  # 房屋编号
    lease = scrapy.Field()  # 租赁方式
    pay_way = scrapy.Field()  # 付款方式
    house_state = scrapy.Field()  # 房屋状态
    heating_method = scrapy.Field()  # 供暖方式
    house_facility = scrapy.Field()  # 房屋设备
    # look_house_num = scrapy.Field()  # 看房人数
    pic_url = scrapy.Field()  # 图片url(字典格式)
