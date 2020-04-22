from mysql import connector
import requests,lxml,re,xlwt,time
from bs4 import BeautifulSoup as bs

class Spider:
    # 按收藏量排序，时长60分钟
    url = "https://search.bilibili.com/all?keyword=python&from_source=nav_suggest_new&order=stow&duration=4&tids_1=0&page="
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    }

    # <a title="[小甲鱼]零基础入门学习Python" href="//www.bilibili.com/video/BV1xs411Q799?from=search&amp;seid=16284475408134808463" target="_blank" class="title">[小甲鱼]零基础入门学习<em class="keyword">Python</em></a>
    findTitle_Link = re.compile(r'<a class="img-anchor" href="(.*?)\?from=search" target="_blank" title="(.*?)">')

     # <span title="观看" class="so-icon watch-num"><i class="icon-playtime"></i>
     #    856.2万
     #  </span>
    findWatch_num = re.compile(r'<i class="icon-playtime"></i>\s*?(\S*?)\s*?</span>')

    findDm = re.compile(r'<i class="icon-subtitle"></i>\s*?(\S*?)\s*?</span>')

    findUploadDate = re.compile(r'<i class="icon-date"></i>\s*?(\S*?)\s*?</span>')

    # https: + findUpLink
    findUpLink_Name = re.compile(r'<a class="up-name" href="(\S*?)\?from=search" target="_blank">(.*?)</a>')

    def fetch_content(self):
        video_info_items = []
        for i in range(1,51):
            html = requests.get(Spider.url + str(i), headers=Spider.headers)
            soup = bs(html.text,"lxml")
            video_items = soup.find_all(class_ = "video-item matrix")
            for video_item in video_items:
                video_info_items.append(self.analysis(video_item))
            time.sleep(1)
        item_cols = ["标题","链接","观看量","弹幕量","上传日期","up主","up主个人空间"]
        return video_info_items,item_cols

    def analysis(self, video_item):
        str_video_item = str(video_item)

        link,title = Spider.findTitle_Link.findall(str_video_item)[0]
        link = "https" + link

        watch_num = Spider.findWatch_num.findall(str_video_item)[0]
        dm = Spider.findDm.findall(str_video_item)[0]
        uploadDate = Spider.findUploadDate.findall(str_video_item)[0]
        upLink,upName = Spider.findUpLink_Name.findall(str_video_item)[0]
        upLink = "https:" + upLink
        return [title,link,watch_num,dm,uploadDate,upName,upLink]

    def saveDate2Excel(self,savapath):
        video_info_items,item_cols = self.fetch_content()
        book = xlwt.Workbook(encoding="utf-8",style_compression=0)
        sheet = book.add_sheet("B站python教程——按收藏量排序",cell_overwrite_ok=True)
        for i in range(len(item_cols)):
            sheet.write(0,i,item_cols[i])

        # 行
        for row in range(1,len(video_info_items) + 1):
            # 列
            for i in range(len(item_cols)):
                sheet.write(row,i,video_info_items[row - 1][i])

        book.save(savapath)

    def saveData2Mysql(self,savepath):
        video_info_items,item_cols = self.fetch_content()

if __name__ == "__main__":
    s = Spider()
    # print(s.fetch_content(s.url + "1"))
    s.saveDate2Excel(r"B站python教程——按收藏量排序.xls")
