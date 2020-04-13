'''
    ^               ^abc 表示字符串开头必须是 abc
                    [^abc] 表示 字符串 不包括 abc 里任何一个

    $               abc$ 表示 字符串结尾 必须是 abc

'''

'''
函数：
    re.search()         搜索匹配的第一个位置，返回 match 对象
    re.match()          从字符串的开头匹配正则表达式，返回 match
    re.findall()        搜索字符串，返回全全部匹配的子串列表
    
模式：
 !  re.I                忽略大小写
    re.L                做本地化识别匹配
 !  re.M                多行匹配，影响 ^ 和 $
 !  re.S                使 . 匹配包括换行在内的所有字符
    re.U                根据 unicode 字符集解析字符，这个标志影响 \w \W \b \B
    re.X                该标志通过给予你更灵活的格式以便将正则表达式写的更易于理解
    
'''

import sys,re


if __name__ == "__main__":
    for line in sys.stdin:

        # 在 正则表达式前 加上 r 不用担心 转义

        # pat = re.compile("AA")                      # 确定规则
        # m = pat.search(line)                        # 从字符串开头搜索匹配的字符串，返回match对象
        # m = pat.match(line)                         # 从字符串开头搜索匹配的字符串

        # m = re.search("asd",line)                   # 从字符串开头搜索匹配的字符串，返回match对象
        # m = re.match("asd",line)                      # 从字符串开头搜索匹配的字符串

        m = re.sub("a","A",line)                        # 在 line 中搜索 'a' 用 'A' 来替换，返回替换后的字符串
        print(m)
