# -*- coding: utf-8 -*-
import re
import sqlite3, os


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class AcfunspiderPipeline_sava2db(object):
    def clean(self, item):
        item["video_view_count"] = re.findall(r"(.*?)次播放", item["video_view_count"])[0]
        if "万" in item["video_view_count"]:
            item["video_view_count"] = float(re.findall(r"(.*?)万", item["video_view_count"])[0]) * 10000
        else:
            item["video_view_count"] = int(item["video_view_count"])

        item["video_title"] = '"' + item["video_title"] + '"'
        item["video_link"] = '"' + item["video_link"] + '"'
        item["video_up"] = '"' + item["video_up"] + '"'
        item["video_create_time"] = '"' + item["video_create_time"] + '"'
        item["video_cover"] = '"' + item["video_cover"] + '"'
        return item

    def process_item(self, item, spider):
        item = self.clean(item)
        self.init_db()

        db = sqlite3.connect(r"videoinfo.db")
        cur = db.cursor()
        sql = """
           INSERT INTO videoinfo(title,link,view_count,up,create_time,cover)
           VALUES(%s,%s,%s,%s,%s,%s);
        """ % (item["video_title"], item["video_link"], item["video_view_count"], item["video_up"],
               item["video_create_time"], item["video_cover"])
        try:
            cur.execute(sql)
            db.commit()
        except Exception as e:
            print("插入数据错误：%s" % (e,))

    def init_db(self):
        if os.path.exists(r"videoinfo.db"):
            pass
        else:
            db = sqlite3.connect(r"videoinfo.db")
            cur = db.cursor()
            sql = """
                create table videoinfo(
                    id integer primary key autoincrement,
                    title varchar, 
                    link text,
                    view_count  numeric,
                    up char[10],
                    create_time  char[20],
                    cover text
                );
            """
            try:
                cur.execute(sql)
                db.commit()
            except Exception as e:
                print(e)
