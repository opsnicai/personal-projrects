from bs4 import BeautifulSoup as bs
import re

'''
    - Tag                   标签
    - NavigableString       导航文字
    - BeautifulSoup         文档
    - Comment               
'''

file = open("豆瓣电影.html", "rb")
html = file.read().decode('utf-8')
soup = bs(html, "html.parser")

# print(type(soup.a),"\n",soup.title,"\n",soup.title.string.split())

# <class 'bs4.element.Tag'> <class 'bs4.element.NavigableString'>
# print(type(soup.a),type(soup.title.string))

# 将标签 a 中的所有等式转换为 键值对
# print(soup.a.attrs)

# <class 'bs4.BeautifulSoup'>
# print(type(soup),soup.name)


# 文档的 遍历
# print(soup.head.contents)       # 把 head 中的 tag 按照列表返回
# print(soup.head.contents[1])



# 文档的 搜索字符串过滤，查找与字符串完全匹配的内容
# t_list = soup.find_all("a")

# 正则表达式：使用 search 来匹配内容

# t_list = re.findall("<a.*</a>",html)

# 1. 正则表达式
# t_list = soup.find_all(re.compile("a"))
# t_list = soup.find_all("a")


# def name_is_exists(tag):
#     return tag.has_attr("name")
#
# 2. 传入一个 函数
# t_list = soup.find_all(name_is_exists)
# print(t_list)

# 3. kwargs 参数
# t_list = soup.find_all(id="a")

# 匹配所有 class
# t_list = soup.find_all(class_ = True)
# for i in t_list:
#     print(i)

# 查找文本
# t_list = soup.find_all(text = "电影")
# t_list = soup.find_all(text = re.compile("\d"))

# t_list = soup.find_all("a",limit= 3)
# for i in t_list:
#     print(i)

# 4.css 选择器 定位 id/class

# 通过标签、类名、id 查找
# t_list = soup.select("title")
# t_list = soup.select("a")


# t_list = soup.select("a[href]")

# 筛选含有特定 属性 的 tag
# t_list = soup.select("div[class = 'gaia gaia-lite gaia-movie']")

# 通过层级结构 寻找子标签
# t_list = soup.select("div > ul > li > a[href]")

t_list = soup.select("#more")
for i in t_list:
    print(i)