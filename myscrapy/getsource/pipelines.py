# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import random
import time

import pymongo
import pymysql


class SaveToMongodbPipeline(object):
    """得到的数据插入mongodb数据库"""

    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.j = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_collection=crawler.settings.get('MOMGO_COLLECTION_NAME')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        print('mongo：连接mongo')

    def close_spider(self, spider):
        self.client.close()
        print('mongo：断开mongo')

    def process_item(self, item, spider):
        collection_name = self.mongo_collection
        self.db[collection_name].insert(dict(item))
        self.j += 1
        print('mongo：完成第%s条数据插入' % self.j)
        return item


class SaveToMysql(object):
    """得到的数据插入mysql数据库"""

    def __init__(self, mysql_db, mysql_host, mysql_user, mysql_port, mysql_password, mysql_charset):

        self.mysql_charset = mysql_charset
        self.mysql_db = mysql_db
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_password = mysql_password
        self.mysql_user = mysql_user
        self.i = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_db=crawler.settings.get('MYSQL_DB'),
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_port=crawler.settings.get('MYSQL_PORT'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_charset=crawler.settings.get('MYSQL_CHARSET'),
        )

    def open_spider(self, spider):
        """连接mysql"""
        self.dbcon = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                     passwd=self.mysql_password, db=self.mysql_db,
                                     port=self.mysql_port, charset=self.mysql_charset)
        self.cursor = self.dbcon.cursor()
        print('mysql：连接mysql')
        print(self.dbcon)
        print(self.cursor)

    def process_item(self, item, spider):
        """执行对应的插入语句"""

        # 插入区域表数据
        sql1 = f"insert into `area`(name) select '{dict(item)['position']}' from dual " \
               f"{self.sql('area_id', 'area', 'name', dict(item)['position'])};"
        # print(sql1)
        self.cursor.execute(sql1)
        self.dbcon.commit()
        # print('完成sql1')

        # 插入房屋类型数据
        sql2 = f"insert into `house_type`(type_name) select '{dict(item)['house_type']}' from dual " \
               f"{self.sql('type_id', 'house_type', 'type_name', dict(item)['house_type'])};"
        # print(sql2)
        self.cursor.execute(sql2)
        self.dbcon.commit()
        # print('完成sql2')

        # 插入用户信息
        sql3 = f"insert into `user`(role_id, account, password, phone, nick_name, avatar) " \
               f"select '1', '{self.create_account()}', '123456', '{dict(item)['phone_number']}', " \
               f"'{dict(item)['publisher_name']}', '{dict(item)['publisher_img_url']}' from dual " \
               f"{self.sql('user_id', 'user', 'nick_name', dict(item)['publisher_name'])};"
        # print(sql3)
        self.cursor.execute(sql3)
        self.dbcon.commit()
        # print('完成sql3')

        # 插入房屋信息
        sql4 = f"insert into `house`(user_id, area_id, type_id, title, price, address, acreage, index_img_url, " \
               f"house_status) select (select user_id from user where nick_name='{dict(item)['publisher_name']}'), " \
               f"(select area_id from area where name='{dict(item)['position']}')," \
               f"(select type_id from house_type where type_name='{dict(item)['house_type']}'), '{dict(item)['title']}', " \
               f"'{dict(item)['price']}', '{dict(item)['real_position']}', '{dict(item)['area']}', " \
               f"'{dict(item)['pic_url'][0]}','{dict(item)['house_state']}' " \
               f"from dual {self.sql('house_id', 'house', 'title', dict(item)['title'])};"
        # print(sql4)
        effect_row = self.cursor.execute(sql4)
        self.dbcon.commit()
        # print('完成sql4')

        if int(effect_row):
            # 插入房屋详细信息
            sql5 = f"insert into `house_detail`" \
                   f"(house_id, lease, pay_way, floor, house_head, community, surround_facility, transportation) " \
                   f"select (select house_id from house where title='{dict(item)['title']}'), " \
                   f"'{dict(item)['lease']}', '{dict(item)['pay_way']}', '{dict(item)['floor']}', '{dict(item)['house_head']}', " \
                   f"'{dict(item)['community']}', '{dict(item)['surround_facility']}', '{dict(item)['transportation']}';"
            # print(sql5)
            self.cursor.execute(sql5)
            self.dbcon.commit()
            # print('完成sql5')

            # 插入房屋配套信息
            if dict(item)['house_facility']:
                for fac in dict(item)['house_facility']:
                    sql6 = f"insert into `house_facility`(facility_id, house_id) " \
                           f"select (select facility_id from facility where facility_name='{fac}')," \
                           f"(select house_id from house where title='{dict(item)['title']}') from dual;"
                    # print(sql6)
                    self.cursor.execute(sql6)
                    self.dbcon.commit()
                    # print('完成sql6')

            # 插入房屋图片url
            if dict(item)['pic_url']:
                for url in dict(item)['pic_url']:
                    sql7 = f"insert into `house_img`(house_id, url) " \
                           f"select (select house_id from house where title='{dict(item)['title']}'), '{url}' from dual;"
                    # print(sql7)
                    self.cursor.execute(sql7)
                    self.dbcon.commit()
                    # print('完成sql7')

            self.i += 1

        print('mysql：完成第%s条数据插入' % self.i)

    @staticmethod
    def create_account():
        """
        生成随机且唯一的用户账号
        :return: 用户账户
        """
        a = ''
        b = 'abcdefghijklmnopqrstuvwxyz0123456789_'
        for _ in range(3):
            a += random.choice(b)
        now = str(int(time.time()))
        a += now
        return a

    @staticmethod
    def sql(col_id, table, col, value):
        """
        生成sql语句(判断数据库是否存在相应的值)
        :param col_id: 数据id
        :param table: 数据表
        :param col: 查询字段
        :param value: 查询字段值
        :return:
        """
        return f"where not exists(select {col_id} from {table} where {col}='{value}')"

    def close_spider(self, spider):
        self.cursor.close()
        self.dbcon.close()
        print('mysql：断开mysql连接')



