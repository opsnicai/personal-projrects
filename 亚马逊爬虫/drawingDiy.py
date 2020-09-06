import requests, time, json, lxml
import pandas as pd
import numpy as np
from lxml import etree
# from bs4 import BeautifulSoup as bs
from sqlalchemy import create_engine


class Spider():
    def __init__(self):
        self.url = "https://www.amazon.cn/s?i=toys-and-games&rh=n%3A647070051%2Cn%3A647071051%2Cn%3A1982067051&page=48&qid=1599315672&ref=sr_pg_48"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
                        "Cookie": "cookie"}
        self.item_info_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
            "Cookie": "session-id=460-7874303-9019444; i18n-prefs=CNY; ubid-acbcn=458-9410244-5234424; session-token=SwpM3YAUX5O/69H28KkbfSbDJwRcfMdqAACo55oLV+YhUHe//y6JHdqd3udKHkNUG38fZ5ucE55AqRAiIKsImTIkVfXXaX17kKa3txJiy6M7cwiEXrWuwe5Kmt62Tgz4PCLJ+ZpfL0o3jfrMHkBPrhFDGVqTz8wVKHaN8vqckqrWG/gPF+cpbut/E4nFGDSi; session-id-time=2082729601l; csm-hit=tb:ED2666R084C52JQCK8RF+s-NHNPEM92MTVYFTDC2JNH|1598741910656&t:1598741910656&adb:adblk_no"
            }
        self.db_host = "localhost"
        self.db_port = 3306
        self.db_user = "root"
        self.db_passwd = "passwd"
        self.db = "amazon_cn"
        self.db_dialect_driver = "mysql+mysqlconnector"
        self.page_flag = True
        self.item_flag = True
        self.n_pages = 3
        self.items = []
        


    def to_db(self, info_list):
        # engine = create_engine('dialect+driver://username:password@host:port/database')
        eng_str = '{dialect_driver}://{username}:{password}@{host}:{port}/{database}'.format(
            dialect_driver=self.db_dialect_driver,
            username=self.db_user,
            password=self.db_passwd,
            host=self.db_host,
            port=self.db_port,
            database=self.db
            )
        engine = create_engine(eng_str)
        df = pd.DataFrame([info_list], columns=["url", "title", "price", "score", "prod_details", "reviews"])
        df.to_sql(name="drawing_diy_temp2", con=engine, if_exists="append")



    def controler(self,url):
        while self.item_flag and self.page_flag:
            for i in self.fetch_item_url_list(url):
                if type(i) == list:
                    self.items.extend(i)
                elif callable(i):
                    # self.pages.append(self.url)
                    i()
                else:
                    print("Error !!!!")
        

    def fetch_single_item_review(self, item_url):
        print(item_url)
        # product info,review
        item_info = []
        item_info.append(item_url)
        f = True
        for _ in range(5):
            # time.sleep(int(10 * np.random.rand()))
            resp = requests.get(url=item_url, headers=self.item_info_headers)
            if resp.raise_for_status != None:
                resp.encoding = resp.apparent_encoding
                tree = etree.HTML(resp.text)
                # soup = bs(resp.text, "lxml")
                # soup = ""
                break
            else:
                f = False
        if not f:
            print(None)
            return None

        item_title = tree.xpath(r'//*[@id="productTitle"]/text()')[0].strip()
        
        try:
            item_price = tree.xpath(r'//*[@id="priceblock_ourprice"]/text()')[0].strip()
        except:
            try:
                item_price = tree.xpath(r'//*[@id="price_inside_buybox"]/text()')[0].strip()
            except:
                item_price = tree.xpath(r'//*[@id="soldByThirdParty"]/span/text()')[0].strip()

        item_info.append(item_title)
        item_info.append(item_price)
        

        try:
            score = tree.xpath(r'//*[@id="acrPopover"]/@title')[0].strip().split()[0]
        except:
            score = -999
        item_info.append(score)
        
        # basic_info
        info_list = []
        try:
            tech_details = tree.xpath(r'//*[@id="productDetails_techSpec_section_1"]')[0]
            for tr in tech_details:
                info_key = tr.xpath(r'./th/text()')[0].strip()
                info_value = tr.xpath(r'./td/text()')[0].strip()
                info_list.append({info_key: info_value})

        except:
            try:
                basic_info = tree.xpath(r'//*[@id="detailBullets_feature_div"]/ul//span[@class="a-list-item"]')
                for i in basic_info:
                    info_key = i.xpath(r'./span[@class="detail-bullet-label a-text-bold"]/text()')[0].strip().split()[0]
                    info_value = i.xpath(r'./span[last()]/text()')[0].strip()
                    info_list.append({info_key: info_value})
            except:
                pass

        finally:
            item_info.append(json.dumps(info_list))

        review_list = []
        try:
            for i in tree.xpath(r'//*[@class="a-section review aok-relative"]'):
                star = i.xpath(r'.//span[@class="a-icon-alt"]/text()')[0].split()[0]
                review_title = i.xpath(r'.//span[@data-hook="review-title"]/span/text()')[0]
                review_date = i.xpath(r'.//span[@data-hook="review-date"]/text()')[0]
                review_collapsed = i.xpath(r'.//div[@data-hook="review-collapsed"]/span/text()')[0].strip()
                review_list.append(json.dumps({"star": star, "review_title": review_title, "review_date": review_date,
                                               "review_collapsed": review_collapsed}))
        except:
            # review_info = soup.find_all(class_="a-section review aok-relative")[0]
            # star = [i.get_text().split()[0] for i in review_info.find_all(class_="a-icon-alt")]
            # review_title = [i.get_text().strip() for i in review_info.find_all(attrs={'data-hook': "review-title"})]
            # review_date = [i.get_text().strip() for i in review_info.find_all(attrs={"data-hook": "review-date"})]
            # review_collapsed = [i.get_text().strip() for i in
            #                     review_info.find_all(attrs={"data-hook": "review-collapsed"})]

            review_list = []
            for i in range(len(star)):
                review_list.append(json.dumps(
                    {"star": star[i], "review_title": review_title[i], "review_date": review_date[i],
                     "review_collapsed": review_collapsed[i]}))

        finally:
            item_info.append(json.dumps(review_list))

        if len(item_info) > 0:
            self.to_db(item_info)
            print("To DB done~~~")
        else:
            print("None data!!")

    def fetch_item_url_list(self,url):
        print(self.url.split("_")[-1])
        for _ in range(5):
            resp = requests.get(url=url, headers=self.headers)
            if resp.raise_for_status != None:
                resp.encoding = resp.apparent_encoding
            else:
                time.sleep(10 * np.random.rand())

        tree = etree.HTML(resp.text)

        item_url_list = []
        for i in tree.xpath(r'//a[@class="a-link-normal a-text-normal"]/@href'):
            if i.startswith("/dp"):
                item_url_list.append("https://www.amazon.cn/" + i)

        try:
            page_args = tree.xpath(r'//*[@id="bottomBar"]/div/span[last()]/a/@href')[0]
        except:
            try:
                page_args = tree.xpath(r'//*[@id="search"]//div[@class="a-section a-spacing-none a-padding-base"]//li[@class="a-normal"]/a/@href')[-1]
            except:
                page_args = ""
        if page_args != "":
            next_page = "https://www.amazon.cn" + page_args
            self.url = next_page
            self.n_pages = self.n_pages - 1
            self.page_flag = self.n_pages > 0
            print("next page:" + self.url)

        flag = len(item_url_list) > 0
        if flag:
            self.item_flag = flag
            yield item_url_list
            yield self.fetch_item_url_list
        else:
            print("None")
            yield None



