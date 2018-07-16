from getsource.settings import MONGO_DB, MONGO_URI, MYSQL_CHARSET, MYSQL_DB, \
    MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER, MOMGO_COLLECTION_NAME
import pymysql
from pymongo import MongoClient
from getsource.pipelines import SaveToMysql
import random
import time


def get_data_from_mongo():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    for one_data in db[MOMGO_COLLECTION_NAME].find():
        yield one_data


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


def con_mysql():
    dbcon = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                 passwd=MYSQL_PASSWORD, db=MYSQL_DB,
                                 port=MYSQL_PORT, charset=MYSQL_CHARSET)
    return dbcon


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



if __name__ == '__main__':
    dbcon = con_mysql()
    cursor = dbcon.cursor()
    i = 0
    for item in get_data_from_mongo():
        sql1 = f"insert into `area`(name) select '{dict(item)['position']}' from dual " \
               f"{sql('area_id', 'area', 'name', dict(item)['position'])};"
        print(sql1)
        cursor.execute(sql1)
        dbcon.commit()
        print('完成sql1')

        # 插入房屋类型数据
        sql2 = f"insert into `house_type`(type_name) select '{dict(item)['house_type']}' from dual " \
               f"{sql('type_id', 'house_type', 'type_name', dict(item)['house_type'])};"
        print(sql2)
        cursor.execute(sql2)
        dbcon.commit()
        print('完成sql2')

        # 插入用户信息
        sql3 = f"insert into `user`(role_id, account, password, phone, nick_name, avatar) " \
               f"select '1', '{create_account()}', '123456', '{dict(item)['phone_number']+dict(item)['to_number']}', " \
               f"'{dict(item)['publisher_name']}', '{dict(item)['publisher_img']}' from dual " \
               f"{sql('user_id', 'user', 'nick_name', dict(item)['publisher_name'])};"
        print(sql3)
        cursor.execute(sql3)
        dbcon.commit()
        print('完成sql3')

        # 插入房屋信息
        sql4 = f"insert into `house`(user_id, area_id, type_id, title, price, address, acreage, index_img_url, " \
               f"house_status) select (select user_id from user where nick_name='{dict(item)['publisher_name']}'), " \
               f"(select area_id from area where name='{dict(item)['position']}')," \
               f"(select type_id from house_type where type_name='{dict(item)['house_type'].split(' ')[0].strip()}'), " \
               f"'{dict(item)['title']}', '{dict(item)['price']}', '{dict(item)['real_position']}', " \
               f"'{dict(item)['area'].split('平米')[0]}', '{dict(item)['house_img'][0]}','{dict(item)['house_state']}' " \
               f"from dual {sql('house_id', 'house', 'title', dict(item)['title'])};"
        print(sql4)
        effect_row = cursor.execute(sql4)

        dbcon.commit()
        print('完成sql4')
        if int(effect_row):

            # 插入房屋详细信息
            sql5 = f"insert into `house_detail`" \
                   f"(house_id, lease, pay_way, floor, house_head, community, surround_facility, transportation) " \
                   f"select (select house_id from house where title='{dict(item)['title']}'), " \
                   f"'{dict(item)['lease']}', '{dict(item)['pay_way']}', '{dict(item)['floor']}', " \
                   f"'{dict(item)['house_head']}', '{dict(item)['community']}', '{dict(item)['surround_facility']}', " \
                   f"'{dict(item)['transportation']}';"
            print(sql5)
            cursor.execute(sql5)
            dbcon.commit()
            print('完成sql5')

            # 插入房屋配套信息
            if dict(item)['house_facility']:
                for fac in dict(item)['house_facility']:
                    sql6 = f"insert into `house_facility`(facility_id, house_id) " \
                           f"select (select facility_id from facility where facility_name='{fac}')," \
                           f"(select house_id from house where title='{dict(item)['title']}') from dual;"
                    print(sql6)
                    cursor.execute(sql6)
                    dbcon.commit()
                    print('完成sql6')

            # 插入房屋图片url
            if dict(item)['house_img']:
                for url in dict(item)['house_img']:
                    sql7 = f"insert into `house_img`(house_id, url) " \
                           f"select (select house_id from house where title='{dict(item)['title']}'), '{url}' from dual;"
                    print(sql7)
                    cursor.execute(sql7)
                    dbcon.commit()
                    print('完成sql7')

            i += 1
        print('mysql：完成第%s条数据插入' % i)
    cursor.close()
    dbcon.close()


