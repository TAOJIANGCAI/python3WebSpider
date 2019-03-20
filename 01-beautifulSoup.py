from bs4 import BeautifulSoup

# html = '''
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
# </p>
# <p class="story">...</p>
# '''
# soup = BeautifulSoup(html, 'lxml')

# 1,标签选择器,如有多个标签，这种方式只返回第一个
# print(soup.title, type(soup.title))
# print(soup.p)
# print(soup.a)

# 2,获取标签名称
# print(soup.title.name, type(soup.title.name))
# print(soup.p.name)

# 3,获取属性
# print(soup.p.attrs['class'])
# print(soup.p['class'])
# print(soup.a.attrs['href'])

# 4，获取内容
# print(soup.title.string)
# print(soup.a.string)

# 5,嵌套选择
# print(soup.head.title.string)

# 6,子节点和子孙节点
# print(soup.contents)
# print(soup.p.children)
# for i, child in enumerate(soup.p.children):
#     print(i, child)

# 7,父节点和祖先节点
# print(soup.a.parents)
# html = """
# <html>
#     <head>
#         <title>The Dormouse's story</title>
#     </head>
#     <body>
#         <p class="story">
#             Once upon a time there were three little sisters; and their names were
#             <a href="http://example.com/elsie" class="sister" id="link1">
#                 <span>Elsie</span>
#             </a>
#             <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
#             and
#             <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
#             and they lived at the bottom of a well.
#         </p>
#         <p class="story">...</p>
# """

# 8,兄弟节点
# print(soup.a.next_sibling)
# soup.a.next_siblings 获取后面的兄弟节点
# soup.a.previous_siblings 获取前面的兄弟节点
# soup.a.next_sibling 获取下一个兄弟标签
# souo.a.previous_sinbling 获取上一个兄弟标签

html = '''
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
            <li class="element">Jay</li>
        </ul>
        <ul class="list list-small" id="list-2">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
        </ul>
    </div>
</div>
'''
# 标准选择器
# find_all(name,attrs,recursive,text,**kwargs)
# find(name,attrs,recursive,text,**kwargs)
# find返回的匹配结果的第一个元素
soup = BeautifulSoup(html, 'lxml')
# 1，name的使用
# print(soup.find_all('ul'), type(soup.find_all('ul')[0]))

# 2，attrs
# print(soup.find_all(attrs={'id': 'list-1'}))
# print(soup.find_all(attrs={'class': 'element'}))

# 3,text
# print(soup.find_all(text='Foo'))

# CSS 选择器

# print(soup.select('.panel .panel-heading'))
# print(soup.select('ul li'))
# print(soup.select('#list-2 .element'))

# 1,获取内容  get_text()
# for li in soup.select('li'):
#     print(li.get_text())

# 2，获取属性 [属性名]或者attrs[属性名]
for ul in soup.select('ul'):
    print(ul['id'], ul.attrs['class'])
