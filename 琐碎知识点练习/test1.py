import re

s = '<span class = "title" > 肖申克的救赎 < /span ><span class = "title" > &nbsp; / &nbsp; The Shawshank Redemption < /span ><span class="other">&nbsp;/&nbsp;月黑高飞(港)  /  刺激1995(台)</span> </a>'

# print(re.findall(r'>\s*?.*?;.*?;\s*?(.*?)\s*?<\s*?/span\s*?>', s))


# s = '<a href="https://movie.douban.com/subject/1292052/"><img width="100" alt="肖申克的救赎" src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p480747492.webp" class=""></a>'
# r = re.compile(r'<a href="(.*?)">\s*?<img width="100" alt="(.*?)" src="(.*?)" class="">\s*?</a>')
# print(r.findall(s))

# s = '导演:奥利维·那卡什OlivierNakache/艾力克·托兰达EricToledano主...2011/法国/剧情喜剧'
# print(re.findall(r"(\S*?...)(\d{4})/(\S*?)/(\S*?)$", s))
# for i in range(0, 250, 25):
#     print(i)

# for i in range(10):
#     url = "https://movie.douban.com/top250?start=" + str(i * 25)
#     print(url)

# s = "导演:万籁鸣LaimingWan/唐澄ChengTang主演:邱岳峰YuefengQiu/...1961(中国大陆)/1964(中国大陆)/1978(中国大陆)/2004(中国大陆)/中国大陆/动画奇幻"
# print(re.findall(r"(\S*?...)(\d{4})\S*/(\S*?)/(\S*?)$", s))


