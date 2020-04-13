import os
import sqlite3

from bs4 import BeautifulSoup as bs
import urllib
from urllib import request
import re
import xlwt


class Spider():
    url = "https://movie.douban.com/top250?start="

    # <img width="100" alt="肖申克的救赎" src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p480747492.webp" class="">
    # 电影名、链接、和图片
    findLink = re.compile(r'<a href="(.*?)">')
    findTitle = re.compile(r'<span class="title">(.*?)</span>')
    findImgSrc = re.compile(r'src="(.*?)"')
    # 排名
    findRace = re.compile(r'<em class="">(\d+)</em>')
    # 评分
    findRating_num = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
    # 评分人数
    findrating_members = re.compile(r'<span>(\d*)人评价</span>')
    # 概述
    findQuote = re.compile(r'<span class="inq">(.*?)</span>')

    def fetchContent(self, url=url):
        headers = {
            # 用户代理，告诉服务器我是什么类型的机器、什么类型的浏览器，本质上是告诉服务器我们能接收什么类型的文件内容
            # 注意：键值对 键 必须和浏览器一致！！！
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        }

        req = request.Request(url, headers=headers)
        try:
            html = request.urlopen(req, timeout=1).read().decode("utf-8")
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)

            if hasattr(e, "reason"):
                print(e.reason)

        return html

    # 第二部筛选，获取数据
    def analysis_getData(self, item):
        # 演员信息
        # content > div > div.article > ol > li:nth-child(1) > div > div.info > div.bd > p:nth-child(1)
        info = item.select("div[class = 'info'] > div[class = 'bd'] > p:nth-child(1)")[0].text

        # 去掉所有空字符
        info = re.sub(r"\s*", "", info)
        # print(info)
        actors, Date, Country, Type = re.findall(r"(\S*?...)(\d{4})\S*/(\S*?)/(\S*?)$", info)[0]

        str_item = str(item)
        title = Spider.findTitle.findall(str_item)[0]
        # titles = []
        # if len(title) < 2:
        #     title.append("")        # 把第二个title留空，方便导入excel
        # else:
        #     title = title[1].replace("/","")        # 出去多余字符
        # titles.extend(title)

        link = Spider.findLink.findall(str_item)[0]
        imgSrc = Spider.findImgSrc.findall(str_item)[0]

        race = Spider.findRace.findall(str_item)[0]
        rating_num = Spider.findRating_num.findall(str_item)[0]
        judge_num = Spider.findrating_members.findall(str_item)[0]

        quote = Spider.findQuote.findall(str_item)

        if len(quote) != 0:
            quote = quote[0].replace("。", "")
        else:
            quote = ""

        return [title, link, imgSrc, race, rating_num, judge_num,
                quote, actors,
                Date, Country, Type]

    # 对爬取的网页进行第一步筛选，获取主要 tags
    def filter(self):
        # 调用获取页面信息，10 页，250 个
        datalist = []
        # 10
        for i in range(10):
            html = self.fetchContent(url=Spider.url + str(i * 25))
            soup = bs(html, "lxml")
            for item in soup.find_all(name="div", attrs={"class": "item"}):
                # print(len(item.contents))
                datalist.append(self.analysis_getData(item))
        col_list = ["title", "link", "封面链接", "排名", "评分", "评分人数", "概述", "演员信息", "上映年份", "国家", "类型"]
        return datalist, col_list

    def saveData2Excel(self, path=r"豆瓣电影Top250.xls"):
        datalist, col_list = self.filter()

        book = xlwt.Workbook(encoding="utf-8", style_compression=0)
        sheet = book.add_sheet(sheetname="豆瓣电影Top250", cell_overwrite_ok=True)

        for i in range(len(col_list)):
            sheet.write(0, i, col_list[i])

        for i in range(1, 251):
            for j in range(len(col_list)):
                sheet.write(i, j, datalist[i - 1][j])

        book.save(path)

    def initDB(self, savepath):
        # 打开或创建数据库
        db = sqlite3.connect(savepath)

        # 获取游标
        c = db.cursor()
        sql = '''
            create table MovieTop250
            (
            id integer primary key autoincrement,
            title varchar not null,
            link text,
            pic_link text,
            race int not null,
            rating_num numeric not null,
            judge_num numeric not null,
            quote varchar not null,
            actors text not null,
            date text not null,
            country text not null,
            type text not null
            );
        '''
        c.execute(sql)
        # 提交数据表
        db.commit()
        # 关闭数据表
        db.close()

    def savaData2Sqlite(self, savepath):
        # 判断数据库是否存在

        self.initDB(savepath)

        # 打开或创建数据库
        db = sqlite3.connect(savepath)
        # 获取游标
        c = db.cursor()

        datalist, col_list = self.filter()
        for data in datalist:
            # index ： 列
            # 将每行变成字符串
            for index in range(len(col_list)):
                if index == 3 or index == 4 or index == 5 or index == 8:
                    continue
                data[index] = '"' + data[index] + '"'

            sqlInfo = '''
                    insert into MovieTop250(
                        title,link,pic_link,race,rating_num,judge_num,quote,actors,date,country,type)
                        values(%s)''' % (",".join(data))

            c.execute(sqlInfo)
            # 提交数据表
            db.commit()
            # 关闭数据表
        c.close()
        db.close()


if __name__ == "__main__":
    s = Spider()
    # print(s.fetchContent())
    # s.saveData2Excel()
    # s.filter()
    # s.initDB(r"doubanTop250.db")
    s.savaData2Sqlite(r"MovieTop250.db")
