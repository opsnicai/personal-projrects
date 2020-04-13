# __author:泷蔚
# __date:2018/9/13

import multiprocessing
import os
import re
import requests
import urllib
from multiprocessing import Pool

from bs4 import BeautifulSoup as bs

# Pool = multiprocessing.Pool()
session = requests.session()


def img_download(url):
    try:
        request = urllib.request.Request(url, headers=girls_spider.headers)
        html = urllib.request.urlopen(request).read()
    except Exception as e:
        print('出现异常》》》》%s,' % str(e))
    finally:
        print('正在重试...')

    child_soup = bs(html, features='lxml')
    imgs = child_soup.find_all(class_='swi-hd')
    child_dir = './秀色女神/' + url[-5:]
    os.mkdir(child_dir)
    for i in imgs:
        url = i.img.get('src')
        print('开始下载。。。', url[-7:])
        img = 'http:' + url
        img = session.get(img, headers=girls_spider.headers)
        with open(child_dir + '/' + url[-7:], 'wb') as f:
            f.write(img.content)
        print('完成')


class girls_spider(object):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
    url = 'https://www.xsnvshen.com/album/'

    def __fetch_content(self, url):  # 获取任意网站内容，并转为 beautifulsoup 格式
        try:
            request = urllib.request.Request(url, headers=girls_spider.headers)
            html = urllib.request.urlopen(request).read()
        except Exception as e:
            print('出现异常》》%s' % str(e))
        finally:
            print('正在重试...')

        s = bs(html, features='lxml')
        return s

    def __session_get(self, url):
        request = urllib.request.Request(url, headers=girls_spider.headers)
        html = urllib.request.urlopen(request).read()
        soup = bs(html, features='lxml')
        return soup

    def __creat_dir(self, d):  # 判断目录是否存在，若不存在则创建一个
        if os.path.exists(d) == True:
            print('目录已存在：', d)
        else:
            os.mkdir(d)
            print('已创建目录：', d)

    def __home_page_analysis(self, url):
        soup = self.__fetch_content(girls_spider.url)
        sort_box = soup.find_all(class_="sort-nav clearfix")
        sort_box_items = sort_box[0].text
        titles = re.findall('\S{2}', sort_box_items)

        sort_item_box = soup.find_all(class_='relative sort-item-box lnavmenuW')
        general_list = []
        for i, j in enumerate(sort_item_box):
            sort_items = j.find_all('a')
            val = []  # 将标题、链接放到字典中，并作为模块字典中的值
            for k in sort_items:
                val.append({k.get('title'): 'https://www.xsnvshen.com' + k.get('href')})
            general_list.append({titles[i]: val})
        return general_list

    def __show_dir(self):
        general_list = self.__home_page_analysis(girls_spider.url)
        for j, i in enumerate(general_list):
            print(j, ''.join(i.keys()))
        inp = input('在以上六类中选择一个,并输入其序号：')
        if inp.isdigit() == True:
            child_dir = general_list[int(inp)].values()
            for j, i in enumerate(list(child_dir)[0]):
                print(j, i)
        pic_inp = input('在以上类型中选择一个，并输入其序号,输入之后开始下载对应网址中的所有图片集：')
        if pic_inp.isdigit() == True:
            url = ''.join(list(child_dir)[0][int(pic_inp)].values())  # 要爬取的网页
            print(url)
        return url

    def __get_album_urls(self):  # 返回相册链接
        url = self.__show_dir()
        soup = self.__session_get(url)
        img_album = soup.find_all(class_='min-h-imgall_300')
        album_urls = []
        for i in img_album:
            album_url = 'https://www.xsnvshen.com' + i.a.get('href')
            print(album_url)
            album_urls.append(album_url)
        return album_urls

    # def __img_download(url):
    #     for i in range(10):
    #         try:
    #             htmls = session.get(url, headers=girls_spider.headers, timeout=1)
    #         except Exception as e:
    #             print('出现异常》》%s,正在重试...' % str(e))
    #
    #     child_soup = bs(htmls.text, features='lxml')
    #     imgs = child_soup.find_all(class_='swi-hd')
    #     child_dir = 'C:/秀色女神/' + url[-5:]
    #     os.mkdir(child_dir)
    #     for i in imgs:
    #         url = i.img.get('src')
    #         print('开始下载。。。', url[-7:])
    #         img = 'http:' + url
    #         img = session.get(img, proxies={'http': '192.161.48.29:80'}, headers=girls_spider.headers)
    #         with open(child_dir + '/' + url[-7:], 'wb') as f:
    #             f.write(img.content)
    #         print('完成')

    def __mp_download(self):
        album_urls = self.__get_album_urls()
        # p = Pool(16)
        # for i in album_urls:
        #     p.apply_async(img_download, args = (i,))
        # p.close()
        # p.join()
        with Pool(16) as p:
            p.map(img_download, album_urls)

    def go(self):
        self.__creat_dir('./秀色女神/')
        self.__mp_download()


test_spider = girls_spider()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    print('程序显示重试仅仅因为网页加载缓慢,程序重新加载而已。')
    test_spider.go()
