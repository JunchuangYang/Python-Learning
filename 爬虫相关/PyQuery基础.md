文章来源 [coder](https://www.cnblogs.com/zhaof/p/6935473.html)

## PyQuery基础
PyQuery库也是一个非常强大又灵活的网页解析库，如果你有前端开发经验的，都应该接触过jQuery,那么PyQuery就是你非常绝佳的选择，PyQuery 是 Python 仿照 jQuery 的严格实现。语法与 jQuery 几乎完全相同，所以不用再去费心去记一些奇怪的方法了。

[PyQuery官网地址](http://pyquery.readthedocs.io/en/latest/)

[jQuery参考文档](http://jquery.cuishifeng.cn/)

**初始化**

**字符串初始化**

```
html = '''
<div>
    <ul>
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
from pyquery import PyQuery as pq #给PyQuery起一个别名pq
doc = pq(html)
print(doc('li'))


output：


<li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>

```

**URL初始化**

```
from pyquery import PyQuery as pq

doc = pq(url="http://www.baidu.com")
print(doc('head'))


output:


<head><meta http-equiv="content-type" content="text/html;charset=utf-8"/><meta http-equiv="X-UA-Compatible" content="IE=Edge"/><meta content="always" name="referrer"/><link rel="stylesheet" type="text/css" href="http://s1.bdstatic.com/r/www/cache/bdorz/baidu.min.css"/><title>ç¾åº¦ä¸ä¸ï¼ä½ å°±ç¥é</title></head> 
```


**文件初始化**

```
from pyquery import PyQuery as pq

doc = pq(filename='demo.html')
print(doc('li'))


output:


<li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
```

**这里我们可以知道上述代码中的doc其实就是一个pyquery对象，我们可以通过doc可以进行元素的选择，其实这里就是一个css选择器，所以CSS选择器的规则都可以用，直接doc(标签名)就可以获取所有的该标签的内容，如果想要获取class 则doc('.class_name'),如果是id则doc('#id_name')....**

**基本CSS选择器**

```
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
from pyquery import PyQuery as pq
doc = pq(html)
print(doc('#container .list li'))

output:


<li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     
```

这里我们需要注意的一个地方是doc('#container .list li')，这里的三者之间的并不是必须要挨着，只要是层级关系就可以,下面是常用的CSS选择器方法：



**查找元素**

**子元素**

```
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
from pyquery import PyQuery as pq
doc = pq(html)
items = doc('.list')
print(type(items))
print(items)
lis = items.find('li')
print(type(lis))
print(lis)


output:


<class 'pyquery.pyquery.PyQuery'>
<ul class="list">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 
<class 'pyquery.pyquery.PyQuery'>
<li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
```

子元素

```
lis = items.children()
print(type(lis))
print(lis)

output:

<class 'pyquery.pyquery.PyQuery'>
<li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>

```
     
同时在children里也可以用CSS选择器

```
lis = items.children('.active')
print(lis)


output:

<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
```

**父元素**

.parent()方法

```

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
from pyquery import PyQuery as pq
doc = pq(html)
items = doc('.list')
container = items.parent()
print(type(container))
print(container)

output:

<class 'pyquery.pyquery.PyQuery'>
<div id="container">
    <ul class="list">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
```

.parents()方法

```
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
items = doc('.list')
parents = items.parents()
print(type(parents))
print(parents)


output:

从结果我们可以看出返回了两部分内容，一个是的父节点的信息，一个是父节点的父节点的信息即祖先节点的信息

<class 'pyquery.pyquery.PyQuery'>
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div><div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
```

同样我们通过.parents查找的时候也可以添加css选择器来进行内容的筛选

parent = items.parents('.wrap')

**兄弟元素**

```
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.list .item-0.active')
print(li.siblings())


output:

<li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0">first item</li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
```
代码中doc('.list .item-0.active') 中的.tem-0和.active是紧挨着的，所以表示是并的关系，这样满足条件的就剩下一个了：thired item的那个标签了
这样在通过.siblings就可以获取所有的兄弟标签，当然这里是不包括自己的
同样的在.siblings()里也是可以通过CSS选择器进行筛选

print(li.siblings('.active'))

**遍历**

单个元素

```
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')
print(li)

output:

<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
```

通过items()可以得到一个生成器，并且我们通过for循环得到的每个元素依然是一个pyquery对象

```
from pyquery import PyQuery as pq
doc = pq(html)
lis = doc('li').items()  #生成器
print(type(lis))
for li in lis:
    print(li)

output:

<class 'generator'>
<li class="item-0">first item</li>
             
<li class="item-1"><a href="link2.html">second item</a></li>
             
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
             
<li class="item-0"><a href="link5.html">fifth item</a></li>


```


**获取信息**

获取属性

pyquery对象.attr(属性名)

pyquery对象.attr.属性名

```
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
a = doc('.item-0.active a')
print(a)
print(a.attr('href'))
print(a.attr.href)



output:


<a href="link3.html"><span class="bold">third item</span></a>
link3.html
link3.html

```

获取文本

```
from pyquery import PyQuery as pq
doc = pq(html)
a = doc('.item-0.active a')
print(a)
print(a.text())

output:

<a href="link3.html"><span class="bold">third item</span></a>
third item
```

获取HTML

```
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')
print(li)
print(li.html()) #字标签的html


output:

<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             
<a href="link3.html"><span class="bold">third item</span></a>
```

**DOM操作**


**addClass、removeClass**

熟悉前端操作的话，通过这两个操作可以添加和删除属性

```

html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')
print(li)
li.removeClass('active')
print(li)
li.addClass('active')
print(li)



output:

<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             
<li class="item-0"><a href="link3.html"><span class="bold">third item</span></a></li>
             
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
```

**attr、css**

同样的我们可以通过attr给标签添加和修改属性，

如果之前没有该属性则是添加，如果有则是修改

我们也可以通过css添加一些css属性，这个时候，标签的属性里会多一个style属性

```
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')
print(li)
li.attr('name', 'link')
print(li)
li.css('font-size', '14px')
print(li)



output:

<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             
<li class="item-0 active" name="link"><a href="link3.html"><span class="bold">third item</span></a></li>
             
<li class="item-0 active" name="link" style="font-size: 14px"><a href="link3.html"><span class="bold">third item</span></a></li>


```

**remove**

```

html = '''
<div class="wrap">
    Hello, World
    <p>This is a paragraph.</p>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
wrap = doc('.wrap')
print(wrap.text())
wrap.find('p').remove()
print(wrap.text())

output：

Hello, World This is a paragraph.
Hello, World
```

[其他DOM方法](http://pyquery.readthedocs.io/en/latest/api.html)

**伪类选择器**

```
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('li:first-child')  #第一个子节点
print(li)
li = doc('li:last-child')  #最后一个子节点
print(li)
li = doc('li:nth-child(2)') #第二个子节点
print(li)
li = doc('li:gt(2)')  #比2大的子节点
print(li)
li = doc('li:nth-child(2n)')  #偶数个子节点
print(li)
li = doc('li:contains(second)')  #内容中包含second的子节点
print(li)



output:


<li class="item-0">first item</li>
             
<li class="item-0"><a href="link5.html">fifth item</a></li>
         
<li class="item-1"><a href="link2.html">second item</a></li>
             
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         
<li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             
<li class="item-1"><a href="link2.html">second item</a></li>
```

更多CSS选择器可以查看 [CSS选择器](http://www.w3school.com.cn/css/index.asp)

官方文档 [pyquery文档](http://pyquery.readthedocs.io/)