# 分析Ajax请求并抓取今日头条街拍美图

参考 [sixkery](https://blog.csdn.net/sixkery/article/details/81836017)

## 1.分析索引页

我们打开今日头条官网，在输出框中输入“街拍”

![](https://i.imgur.com/yva4uGs.png)

点击确定，跳转到详情页，使用F12，然后再刷新页面，会在开发者工具中看到如下页面

![](https://i.imgur.com/7AsVbyN.png)

不断用鼠标往下话，页面地址没有变化，会看见左边的请求参数中不跳出新的请求参数，随着不断往下滑，其中offset的值会变化offset=0,20,40.......，这一看就是Ajax加载的页面，同时，右下方的请求参数我们也需要记住，我们爬取得时候要当成参数传进去。

![](https://i.imgur.com/7PayoYa.png)

在同一个界面，点解preview可以看到在data列表中有一个**article_url**,将url打开以下，会发现是每个文章的详细内容界面，同时，可以判断，这个url就是我们要的文章详情页的url

打开上述的article_url

![](https://i.imgur.com/yKyO4At.png)

通过查看response的内容可以分析到有一个gallery的列表，发现他的count=3，而我们此时的页面的图片也是有3个，同时，他后面跟了一些url地址，会不会是我们要的图片地址呢？我们将图片地址复制到浏览器中进行查看，你会发现不是我们想要的结果。等等，有没有觉得这个URL感觉不对，他里面多了一些转义字符'\\',我们把它去掉以后再输一次，你会发现我们想要的东西终于出来了。


## 2.代码

通过上面的分析，我们只要一步一步进行解析就能获得我们的结果了。

**引入库**

```
#coding=gbk

import json,re
import os
import pymongo
import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from config import *  
from hashlib import md5
from multiprocessing import Pool

# config是一个MongoDB的配置文件

```

**获取索引数据**

也就是我们在今日头条中输入‘街拍’的过程

```
def get_page_index(offset,keyword):

    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        'from': 'search_tab'
    }
 
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None


####################################
offset是页面加载需要的参数

keyword是搜索关键字，如 ‘街拍’

data就是获取网页需要的 Query String Parameters

添加headers信息，否则可能获取不到结果，今日头条有反爬机制

```

**解析索引页**

```
def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


####################################
获取所有详情页的URL

页面时json格式的，用json.loads()将字符串转换成为Python对象

data.keys() 获取所有的键值


```

**请求详情页**

```
def get_page_detail(url):
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
            #return response.text.encode('gbk', 'ignore')
        return None
    except RequestException:
        print('请求详情页出错')
        return None

####################################

获取详情页的内容，也就是我们分析出来的URL内容
```

**解析详情页**

```
def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    images_pattern = re.compile('.*?gallery: JSON.parse\("(.*?)"\)', re.S)
    result = re.search(images_pattern,html)
    if result:
        data = json.loads(result.group(1).replace('\\',''))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]  #提取图片url
            for image in images: download_image(image)  #下载图片
            return {
                'title': title,
                'url' : url,
                'images': images
            }

####################################
soup.select('title')[0].get_text() 获取详情页的标题

使用正则表达式匹配图片的url地址

json.loads(result.group(1).replace('\\','')) 将匹配到的URL中的转义字符除去，并将字符串转换成Python对象
```

**MongoDB**

config.py配置文件中的内容

```
#coding=utf-8
#链接地址
MONGO_URL = 'localhost'

#数据库名称
MONGO_DB = 'jiepai'

#表名称
MONGO_TABLE = 'jiepai'

KEYWORDS = '街拍'

GROUP_START=1
GROUP_END=20

```

MongoDB的设置

```
client = pymongo.MongoClient(MONGO_URL,connect=False) #声明mongo对象

db = client[MONGO_DB] #数据库名称

#保存到mongo数据库中

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功')
        return True
    return  False

```

**下载/保存 图片**

```
def download_image(url):
    print('正在下载',url)
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片出错',url)
        return None

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()

####################################

这里用了 hashlib 库的 md5 这个方法，目的是为了防止图片的重复，这个方法会根据图片的内容生成唯一的字符串，用来去重。

```

**开启多线程抓取**

```
def main(offset):
    html = get_page_index(offset,KEYWORDS)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html,url)
            if result:
                save_to_mongo(result)



if __name__ == '__main__':
    groups = [x*20 for x in range(GROUP_START,GROUP_END+1)]
    pool = Pool()
    pool.map(main,groups) #这里声明一个线程池，调用 map 方法开启线程就可以了。
    pool.close()
```