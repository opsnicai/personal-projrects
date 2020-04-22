# -*- coding: utf-8 -*-
import re

import xlwt, sqlite3, os

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# 在Scrapy中，Item Pipeline是处理数据的组件，
# 一个Item Pipeline就是一个包含特定接口的类，通常只负责一种功能的数据处理，
# 在一个项目中可以同时启用多个Item Pipeline，它们按指定次序级联起来，形成一条数据处理流水线。
# Item Pipeline的几种典型应用：
#
# ●　清洗数据。
# ●　验证数据的有效性。
# ●　过滤掉重复的数据。
# ●　将数据存入数据库。

class BooksspiderPipeline_save2db(object):
    # 将数据写入sqlite3
    def init_db(self):
        db = sqlite3.connect(r"bookinfo.db")
        cur = db.cursor()
        sql = '''
            create table bookinfo(
                id integer primary key autoincrement,
                name text,
                link text,
                price char[20],
                cover text,
                rating_star char[10]
            );
        '''
        db.execute(sql)
        db.commit()
        db.close()

    def process_item(self, item, spider):

        # print(item["name"])
        if os.path.exists("bookinfo.db"):
            db = sqlite3.connect('bookinfo.db')
            cur = db.cursor()

            item["name"] = re.sub(r'"', " ", item["name"])
            item["name"] = '"' + item["name"] + '"'
            item["link"] = '"' + item["link"] + '"'
            item["price"] = '"' + item["price"] + '"'
            item["rating_star"] = '"' + item["rating_star"] + '"'
            item["cover"] = '"' + item["cover"] + '"'

            sql = '''
                insert into bookinfo(name,link,price,rating_star,cover)
                values(%s,%s,%s,%s,%s);
            ''' % (item["name"],item["link"], item["price"], item["rating_star"], item["cover"])

            cur.execute(sql)
            db.commit()
            db.close()
        else:
            self.init_db()
