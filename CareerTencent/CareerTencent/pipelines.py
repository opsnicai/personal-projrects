# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3, os, logging

logger = logging.getLogger(__name__)


class CareertencentPipeline(object):
    # 将数据保存到sqlite3
    def process_item(self, item, spider):
        self.init_db()
        db = sqlite3.connect("careerinfo.db")
        cur = db.cursor()

        item["title"] = '"' + item["title"] + '"'
        item["link"] = '"' + item["link"] + '"'
        item["businessgroup"] = '"' + item["businessgroup"] + '"'
        item["city"] = '"' + item["city"] + '"'
        item["type"] = '"' + item["type"] + '"'
        item["recruit_date"] = '"' + item["recruit_date"] + '"'
        item["job_info"] = '"' + item["job_info"] + '"'
        item["job_requirement"] = '"' + item["job_requirement"] + '"'

        sql = '''
            INSERT INTO careerinfo(
                title,link,city,type,recruit_date,businessgroup,job_info,job_requirement
            )
            values(%s,%s,%s,%s,%s,%s,%s,%s);
        ''' % (
            item["title"], item["link"],item["city"], item["type"], item["recruit_date"], item["businessgroup"], item["job_info"],
            item["job_requirement"])
        try:
            cur.execute(sql)
            db.commit()
        except Exception as e:
            logger.error(e)
        return item

    def init_db(self):
        if os.path.exists("careerinfo.db"):
            pass
        else:
            db = sqlite3.connect(r"careerinfo.db")
            cur = db.cursor()
            sql = '''
                create table careerinfo(
                    id integer primary key autoincrement,
                    title varchar,
                    link text,
                    city varchar,
                    type char[50],
                    recruit_date char[20],
                    businessgroup varchar,
                    job_info text,
                    job_requirement text
                );
            '''
            cur.execute(sql)
            db.commit()
            db.close()
            logger.warning("创建数据库成功！")
