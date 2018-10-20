# 总结

## 遇到的问题

**1.response.text  和 response.content**

在某些情况下来说，response.text 与 response.content 都是来获取response中的数据信息，效果看起来差不多。那么response.text 和 response.content 到底有哪些差别 ？ 什么情况下该用 response.text 什么情况下该用 response.content ？

返回的数据类型 

response.text 返回的是一个 unicode 型的文本数据

response.content 返回的是 bytes 型的**二进制**数据 


也就是说如果想取**文本数据**可以通过response.text 

如果想取**图片，文件，**则可以通过 response.content

数据编码 

response.content 返回的是**二进制响应内容 **

response.text 则是默认”iso-8859-1”编码，服务器不指定的话是根据**网页的响应**来猜测编码。 

来源：CSDN  [何惜戈](https://blog.csdn.net/qq_37049781/article/details/79958436)


**2.Python print 输出文本显示 gbk 编码错误**

UnicodeEncodeError: ‘ gbk ’ codec can ’ t encode character ‘\xa0 ’ in position，在网上一查，发现是 Windows 的控制台的问题。控制台的编码是 GBK，Python 是 UTF-8，造成了冲突。

```
第一种方法：直接替换出错的内容
url = 'https://zhuanlan.zhihu.com/p/39747259' 
print(requests.get(url).text.replace('\xa0', ' '))

第二种方法：再解码

先用 GBK 编码，加个 ignore 丢弃错误的字符，然后再解码。

import requests
url = 'https://zhuanlan.zhihu.com/p/39747259'
print(requests.get(url).text.encode('gbk', 'ignore').decode('gbk')

第三种方法：修改控制台编码

新建一个 cmd.reg, 输入代码：
Windows Registry Editor Version 5.00
[HKEY_CURRENT_USER\Console\%SystemRoot%_system32_cmd.exe]
"CodePage"=dword:0000fde9
"FontFamily"=dword:00000036
"FontWeight"=dword:00000190
"FaceName"="Consolas"
"ScreenBufferSize"=dword:232900d2
"WindowSize"=dword:002b00d2

保存后运行。如果 Ctrl+B 无效，用 python.exe 打开.py 程序后再试一次。

```

[来源](https://www.v2ex.com/t/470896)

**3.pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [WinError 10061] 由于目标计算机积极拒绝，无法连接。**

原因：在PyCharm中调用MongoDB数据库时，由于没有启动本地的MongoDB服务引起。

解决方法：打开命令行窗口 ，用cd命令打开mongod.exe所在的目录，并输入**mongod.exe --nojournal --dbpath .**（注意–dbpath后面有个点） 

如果出现‘ [initandlisten] waiting for connections on port 27017’提示说明服务器已经启动成功 

-Ctrl + C 关闭服务器

[来源](https://blog.csdn.net/qq_38410428/article/details/81478361)

**4.python中json文件处理涉及的四个函数json.dumps()和json.loads()、json.dump()和json.load()的区分**

一、概念理解

1、json.dumps()和json.loads()是json格式处理函数（可以这么理解，json是字符串）

　　(1)json.dumps()函数是将一个Python数据类型列表进行json格式的编码（可以这么理解，json.dumps()函数是将字典转化为字符串）

　　(2)json.loads()函数是将json格式数据转换为字典（可以这么理解，json.loads()函数是将字符串转化为字典）

2、json.dump()和json.load()主要用来读写json文件函数

二、测试

**json.dumps()函数的使用，将字典转化为字符串**

```
import json
dict1 = {"age": "12"}
json_info = json.dumps(dict1)
print("dict1的类型："+str(type(dict1)))
print("通过json.dumps()函数处理：")
print("json_info的类型："+str(type(json_info)))

```
output:

![](https://i.imgur.com/85M4znD.png)


**json.loads函数的使用，将字符串转化为字典**


```
import json


json_info = '{"age": "12"}'
dict1 = json.loads(json_info)
print("json_info的类型："+str(type(json_info)))
print("通过json.dumps()函数处理：")
print("dict1的类型："+str(type(dict1)))

```

![](https://i.imgur.com/yNVu57v.png)


**json.dump()函数的使用，将json信息写进文件**

```
import json


json_info = "{'age': '12'}"
file = open('1.json','w',encoding='utf-8')
json.dump(json_info,file)



1.json文件:

"{'age': '12'}"
```

**json.load()函数的使用，将读取json信息**

```
import json


file = open('1.json','r',encoding='utf-8')
info = json.load(file)
print(info)



output:

{'age':'12'}

```

[来源](https://www.cnblogs.com/xiaomingzaixian/p/7286793.html)

## 总结

路还很长，基础还要慢慢的学，不会的东西依然很多。

