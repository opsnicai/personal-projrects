import requests, lxml, re
from bs4 import BeautifulSoup as bs

url = "https://search.bilibili.com/all?keyword=python&from_source=nav_suggest_new&order=stow&duration=4&tids_1=0&page=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
}

# html = requests.get(url, headers=headers)
html = open("python - bilibili.html", "rb")
html.encoding = "utf-8"
# print(html.text)
soup = bs(html, "lxml")

video_items = soup.find_all(class_="video-item matrix")
# print(type(video_items[0]))

# re.sub(r"\s*","",str(video_items[0]))
print(video_items[0])
print(re.findall(r'<a class="title" href="//(\S*?)\?from=search" target="_blank" title="(\S*?)">', str(video_items[0])))

# <span title="观看" class="so-icon watch-num"><i class="icon-playtime"></i>
     #    856.2万
     #  </span>
# findWatch_num = re.compile(r'<i class="icon-playtime"></i>\s*?(\S*?)\s*?</span>')
# print(findWatch_num.findall(str(video_items[0])))

# findName = re.compile(r'<a class="up-name" href="(\S*?)\?from=search" target="_blank">(.*?)</a>')
# print(findName.findall(str(video_items[0])))