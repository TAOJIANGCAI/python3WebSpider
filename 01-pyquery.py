from pyquery import PyQuery as pq

html = '''
<div id="container">
    <ul class="list">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
# 初始化：1，传入字符串，传入url，传入文件
# 01,传入字符串
# doc = pq(html)
# print(doc)

# 02，传入url
# doc = pq(url="https://www.baidu.com", encoding="utf-8")
# print(doc)

# 03,传入文件
# doc = pq(filename='index.html')
# print(doc)

# 2，基本的css选择器
# doc = pq(html)
# print(doc('#container .list li'))

# 查找元素 children find
# items = doc('.list')
# print(items)
# print(items.find('.item-0'))
# print(items.children('.active'))

# print(items.parents())

# li = doc('.list .item-0.active')
# # print(li.siblings())
# 遍历
# lis = doc('li').items()
# print(type(lis))
#
# for li in lis:
#     print(type(li))
#     print(li)


# 获取属性 attr.href 或者attr('href')
# a = doc('.item-0.active a')
# print(a.attr('href'))
# print(a.attr.href)

# 获取文本 text()
# a = doc('.item-0.active a')
# print(a.text())


# 获取html  html()
# a = doc('.item-0.active')
# print(a.html(a))

# DOM操作 addclass removeClass,attr,css
# li = doc('.item-0')
# print(li)
# li.add_class('abc')
# print(li)
#
# li2 = doc('.item-1.active')
# print(li2)
# li2.remove_class('active')
# print(li2)

# li = doc('.item-0.active')
# print(li)
# li.attr('name', 'link')
# li.css('font-size', '14px')
# li.attr('name', 'link2')
# print(li)

# remove操作  有时候我们获取文本信息的时候可能并列的会有一些其他标签干扰，这个时候通过remove就可以将无用的或者干扰的标签直接删除，从而方便操作
html2 = '''
<div class="wrap">
    Hello, World
    <p>This is a paragraph.</p>
 </div>
'''
doc2 = pq(html2)
wrap = doc2('.wrap')
print(wrap.text())
wrap.find('p').remove()
print(wrap.text())
