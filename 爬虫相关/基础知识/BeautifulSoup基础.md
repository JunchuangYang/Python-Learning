## BeautifulSoup基础

BeautifulSoup:灵活又方便的网页解析库，处理高效，支持多种解析器。利用它可以在不用编写正则表达式，即可方便地实现网页信息的提取。

安装： pip3 install beautifulsoup4

### 解析库

![](https://i.imgur.com/uXqpnx6.png)

### 基本使用

    html = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    <p class="story">...</p>
    """   #代码不完整，有的标签标签没有闭合
    
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, 'lxml') #第二个参数，传入解析器lxml
    print(soup.prettify())  # 格式化代码，自动的把代码进行补全，进行容错处理
    print(soup.title.string) # 选择了title标签，并打印其内容

输出结果：

![](https://i.imgur.com/oVrM1r7.png)

### 标签选择器

**选择元素**

    html = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    <p class="story">...</p>
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')
    print(soup.title)
    print(type(soup.title))
    print(soup.head)
    print(soup.p)

输出结果：

![](https://i.imgur.com/Ui6dP0N.png)

**获取名称**

    # <head><title>The Dormouse's story</title></head>

    print(soup.title.name)#输出结果：title

**获取属性**

    # <p class="title" name="dromouse"><b>The Dormouse's story</b></p>

    print(soup.p.attrs['name'])
    print(soup.p['name'])
    #输出结果：
              dromouse
              dromouse

**获取内容**

    # <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
    print（soup.p.string） 
    #输出结果：The Dormouse's story

通过这种soup.标签名 我们就可以获得这个标签的内容

**这里有个问题需要注意，通过这种方式获取标签，如果文档中有多个这样的标签，返回的结果是第一个标签的内容，如上面我们通过soup.p获取p标签，而文档中有多个p标签，但是只返回了第一个p标签内容**

**嵌套选择**

    print(soup.head.title.string)
    #输出结果：The Dormouse's story

**子节点和子孙节点**

contens的使用

```  
html = """
<html>
    <head>
        <title>The Dormouse's story</title>
    </head>
    <body>
        <p class="story">
            Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1">
                <span>Elsie</span>
            </a>
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> 
            and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
            and they lived at the bottom of a well.
        </p>
        <p class="story">...</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.p.contents)


  
```
输出结果：

![](https://i.imgur.com/FulZPgj.png)

从输出结果中可以看到，使用contents后，标签p中的所有元素以列表的形式打印了出来

**chrildren**

```
   print(soup.p.children)
   for i,child in soup.p.children:
		print(i,child)   
```

输出结果：

![](https://i.imgur.com/gJvYuDx.png)

children获取p标签下的所有子节点内容和通过contents获取的结果是一样的，但是不同的地方是soup.p.children是一个迭代对象，而不是列表，只能通过循环的方式获取素有的信息

通过contents以及children都是获取子节点，如果想要获取子孙节点可以通过descendants（包括子节点）同时这种**获取的结果也是一个迭代器**

```
   print(soup.p.descendants)
   for i,descendant in soup.p.descendents：
		print(i,descendent)
```

输出结果：

```
<generator object descendants at 0x10650e678>
0 
            Once upon a time there were three little sisters; and their names were
            
1 <a class="sister" href="http://example.com/elsie" id="link1">
<span>Elsie</span>
</a>
2 

3 <span>Elsie</span>
4 Elsie
5 

6 

7 <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
8 Lacie
9  
            and
            
10 <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
11 Tillie
12 
            and they lived at the bottom of a well.

```

**父节点和祖先节点**

通过 **soup.a.parent** 可以获取p节点的父节点的信息

通过**list(enumerate(soup.a.parents)**)可以获取祖先节点，这个方法返回的结果是一个列表，会分别将a标签的父节点的信息存放到列表中，以及父节点的父节点也放到列表中，并且最后还会讲整个文档放到列表中，**所有列表的最后一个元素以及倒数第二个元素都是存的整个文档的信息**

```
html = """
<html a="老爷节点">
    <body><p>#a的爷爷节点
        <p class="story">
         #a 的父节点
            Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1">
                <span>Elsie</span>
            </a>
        </p>
        <p class="story">...</p>
"""

from bs4 import BeautifulSoup

soup = BeautifulSoup(hrml,'lxml')
print(list(enumerate(soup.a.parents))

#输出结果

[(0, <p class="story">
         #a 的父节点
            Once upon a time there were three little sisters; and their names were
            <a class="sister" href="http://example.com/elsie" id="link1">
<span>Elsie</span>
</a>
</p>), (1, <body><p>#a的爷爷节点
        </p><p class="story">
         #a 的父节点
            Once upon a time there were three little sisters; and their names were
            <a class="sister" href="http://example.com/elsie" id="link1">
<span>Elsie</span>
</a>
</p>
<p class="story">...</p>
</body>), (2, <html a="老爷节点">
<body><p>#a的爷爷节点
        </p><p class="story">
         #a 的父节点
            Once upon a time there were three little sisters; and their names were
            <a class="sister" href="http://example.com/elsie" id="link1">
<span>Elsie</span>
</a>
</p>
<p class="story">...</p>
</body></html>), (3, <html a="老爷节点">
<body><p>#a的爷爷节点
        </p><p class="story">
         #a 的父节点
            Once upon a time there were three little sisters; and their names were
            <a class="sister" href="http://example.com/elsie" id="link1">
<span>Elsie</span>
</a>
</p>
<p class="story">...</p>
</body></html>)]

```

**兄弟节点**

    soup.a.next_siblings 获取后面的兄弟节点  
    soup.a.previous_siblings 获取前面的兄弟节点  
    soup.a.next_sibling 获取下一个兄弟标签  
    souo.a.previous_sinbling 获取上一个兄弟标签  

**标准选择器**

find_all( name , attrs , recursive , text , **kwargs )

可根据标签名、属性、内容查找文档

**name的用法**

```
 html='''
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
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.find_all('ul'))
print(type(soup.find_all('ul')[0]))
```
输出结果：

![](https://i.imgur.com/kJv9OHq.png)

输出的结果是列表的形式

我们可以根据find_all('ul')获取ul标签下所有的li信息

```
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
for ul in soup.find_all('ul'):
    print(ul.find_all('li'))

```

**attrs用法**

```
html='''
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1" name="elements">
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
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')

print(soup.find_all(attrs={'id': 'list-1'}))
print(soup.find_all(attrs={'name': 'elements'}))

print(soup.find_all(id='list-1')) #与第一个输出结果一样
print(soup.find_all(class_='element'))

```

attrs可以传入字典的方式来查找标签，但是这里有个特殊的就是class,因为class在python中是特殊的字段，所以如果想要查找class相关的可以更改attrs={'**class_**':'element'}

**text**

print(soup.find_all(text='Foo')) #结果返回的是text='Foo'的文本

**find( name , attrs , recursive , text , **kwargs )**

**find返回单个元素，find_all返回所有元素**

    print(soup.find('ul')) #返回找到的一个ul标签
    print(type(soup.find('ul'))) #<class 'bs4.element.Tag'>
    print(soup.find('page')) #没有page标签，返回None

find_parents() find_parent()

find_parents()返回所有祖先节点，find_parent()返回直接父节点。

find_next_siblings() find_next_sibling()

find_next_siblings()返回后面所有兄弟节点，find_next_sibling()返回后面第一个兄弟节点。

find_previous_siblings() find_previous_sibling()

find_previous_siblings()返回前面所有兄弟节点，find_previous_sibling()返回前面第一个兄弟节点。

find_all_next() find_next()

find_all_next()返回节点后所有符合条件的节点, find_next()返回第一个符合条件的节点

find_all_previous() 和 find_previous()

find_all_previous()返回节点前所有符合条件的节点, find_previous()返回第一个符合条件的节点

**CSS选择器**

通过select()直接传入CSS选择器即可完成选择

标签1，标签2 找到所有的标签1和标签2

标签1 标签2 找到标签1内部的所有的标签2

[attr] 可以通过这种方法找到具有某个属性的所有标签

[atrr=value] 例子[target=_blank]表示查找所有target=_blank的标签


```
  html='''
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
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.select('.panel .panel-heading')) # . 表示class
print(soup.select('ul li'))  # 空格表示下一个属性
print(soup.select('#list-2 .element')) # #表示id
print(type(soup.select('ul')[0]))

```

输出结果：

![](https://i.imgur.com/yfFYzA0.png)

```
for ul in soup.select('ul'):
    print(ul.select('li'))

output:[<li class="element">Foo</li>, <li class="element">Bar</li>, <li class="element">Jay</li>]
[<li class="element">Foo</li>, <li class="element">Bar</li>]
```
**获取属性**

```
for ul in soup.select('ul'):
    print(ul['id'])
    print(ul.attrs['id'])

output:
    list-1
	list-1
	list-2
	list-2
```
**获取内容**

```
for li in soup.select('li'):
    print(li.get_text())
output :
	Foo
	Bar
	Jay
	Foo
	Bar
```

**总结**

推荐使用lxml解析库，必要时使用html.parser  

标签选择筛选功能弱但是速度快

建议使用find()、find_all() 查询匹配单个结果或者多个结果

如果对CSS选择器熟悉建议使用select()

记住常用的获取属性和文本值的方法