import urllib
from urllib import request, parse

# # urllib.parse url解析器，使用 utf-8 编码，在转成 二进制 流
# data = bytes(parse.urlencode({"hello":"world"}),encoding = "utf-8")
#
# url = "http://httpbin.org/post"
#
# # post 请求
# # response = request.urlopen(url,data = data)
#
# # 超时处理
# try:
#     # get 方法
#     # response = request.urlopen("http://httpbin.org/get",timeout= 1)
#
# except urllib.error.URLError as e:
#     print("time out!")
#
# # 对获取到的网页源码进行 utf-8 解码,支持中文，按原格式输出
# # print(response.read().decode('utf-8'))
#
# # 打印状态码 200、404
# print(response.status)
#
# # 打印响应头,将信息作为列表返回
# print(response.getheaders())
#
# # 只要 响应头中的 Data 信息
# print(response.getheader("Date"))

url = "https://movie.douban.com/top250"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
data = bytes(parse.urlencode({"hello": "world"}), encoding="utf-8")

# request.Request 对 访问 进行封装，包括 get\post 方法
req = request.Request(url, data=data, headers=headers)
response = request.urlopen(req,timeout = 1)

# 对获取到的网页源码进行 utf-8 解码,支持中文，按原格式输出
# print(response.read().decode('utf-8'))

# 打印状态码 200、404
print(response.status)

# 打印响应头,将信息作为列表返回
print(response.getheaders())

# 只要 响应头中的 Data 信息
print(response.getheader("Date"))

print(response.read().decode("utf-8"))