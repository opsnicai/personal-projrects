import re

s =  '<a title="[小甲鱼]零基础入门学习Python" href="//www.bilibili.com/video/BV1xs411Q799?from=search&amp;seid=16284475408134808463" target="_blank" class="title">[小甲鱼]零基础入门学习<em class="keyword">Python</em></a>'
findTitle_Link = re.compile(r'<a title="(\S*?)" href="//(\S*?)\?from=.*?class="title">')

print(re.findall(findTitle_Link,s))