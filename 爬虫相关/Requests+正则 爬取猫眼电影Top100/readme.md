Requests+正则 爬取猫眼电影
## 1

流程框架：

抓取单页内容：利用requests请求目标站点，得到单个网页HTML代码，返回结果

正则表达式分析： 根据HTML代码分析得到电影的名称、主演、上映时间、评分、图片链接等信息

开启循环及多线程：对多页内容遍历，开启多线程提高抓取速度

保存至文件：通过文件的形式将结果保存，每一部电影一个结果一行Json字符串


## 2

程序中出现中文，运行的时候出现如下错误：

SyntaxError: Non-UTF-8 code starting with 'xc1' in file C:...xxx.py on line 8, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details

导致出错的根源就是编码问题。

解决方案是：在程序最上面加上：#coding=gbk

这样程序就可以正常运行了。


## 3

写代码期间还遇到了pycharm的一些问题，换了一个Python源之后pycharm突然不能用了，由于以前的那个Python源的包比较少，所以换了一个，之后就一直出现 **AttributeError: 'PyDevTerminalInteractiveShell' object has no attribute 'has_readline'** 这个问题。最后百度了一下ipython版本的问题，

解决方法如下：

这是因为安装的ipython版本不兼容导致，可以使用下面命令解决：

```
 pip uninstall ipython
 pip install ipython==4.2.0

```

## 4


关于文件中open()的mode参数：

'r'：读

'w'：写

'a'：追加

'r+' == r+w（可读可写，文件若不存在就报错(IOError)）

'w+' == w+r（可读可写，文件若不存在就创建）

'a+' ==a+r（可追加可写，文件若不存在就创建）

对应的，如果是二进制文件，就都加一个b就好啦：

'rb'　　'wb'　　'ab'　　'rb+'　　'wb+'　　'ab+'