## 初识Scrapy

文字解释来自 https://www.cnblogs.com/zhaof/p/7173094.html

Scrapy使用了Twisted作为框架，Twisted有些特殊的地方是它是事件驱动的，并且比较适合异步的代码。对于会阻塞线程的操作包含访问文件、数据库或者Web、产生新的进程并需要处理新进程的输出(如运行shell命令)、执行系统层次操作的代码(如等待系统队列),Twisted提供了允许执行上面的操作但不会阻塞代码执行的方法。

scrapy的项目结构：

![](https://i.imgur.com/W02IdxG.png)

items.py 负责数据模型的建立，类似于实体类。
middlewares.py 自己定义的中间件。
pipelines.py 负责对spider返回数据的处理。
settings.py 负责对整个爬虫的配置。
spiders目录 负责存放继承自scrapy的爬虫类。
scrapy.cfg scrapy基础配置

那么如何创建上述的目录，通过下面命令：

scrapy startprogect quote

可是在windows下哪有那么简单，我是使用conda install scray 安装的，但是依然出了问题。

**问题一**

```
1.
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\scrapy\cmdline.py", line 149, in execute
    cmd.crawler_process = CrawlerProcess(settings)
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\scrapy\crawler.py", line 252, in __init__
    log_scrapy_info(self.settings)
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\scrapy\utils\log.py", line 149, in log_scrapy_info
    for name, version in scrapy_components_versions()
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\scrapy\utils\versions.py", line 35, in scrapy_components_versions
    ("pyOpenSSL", _get_openssl_version()),
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\scrapy\utils\versions.py", line 43, in _get_openssl_version
    import OpenSSL
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\OpenSSL\__init__.py", line 8, in <module>
    from OpenSSL import crypto, SSL
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\OpenSSL\crypto.py", line 16, in <module>
    from OpenSSL._util import (
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\OpenSSL\_util.py", line 6, in <module>
    from cryptography.hazmat.bindings.openssl.binding import Binding
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\cryptography\hazmat\bindings\openssl\binding.py", line 13, in <module>
    from cryptography.hazmat.bindings._openssl import ffi, lib
ImportError: DLL load failed: 操作系统无法运行 %1。

解决办法：pip3.6 uninstall pyopenssl
pip3.6 uninstall cryptography

pip3.6 install pyopenssl
pip3.6 install cryptography
```

继续使用scrapy startproject quote,又出现如下错误 :

**问题二**

```

Traceback (most recent call last):
  File "C:\Users\lenovo\Anaconda3\Scripts\scrapy-script.py", line 10, in <module>
    sys.exit(execute())
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\scrapy\cmdline.py", line 149, in execute
    cmd.crawler_process = CrawlerProcess(settings)
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\scrapy\crawler.py", line 252, in __init__
    log_scrapy_info(self.settings)
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\scrapy\utils\log.py", line 149, in log_scrapy_info
    for name, version in scrapy_components_versions()
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\scrapy\utils\versions.py", line 35, in scrapy_components_versions
    ("pyOpenSSL", _get_openssl_version()),
  File "C:\Users\lenovo\Anaconda3\lib\site-packages\scrapy\utils\versions.py", line 43, in _get_openssl_version
    import OpenSSL
ModuleNotFoundError: No module named 'OpenSSL'

C:\Users\lenovo>pip3.6 install OpenSSL
Collecting OpenSSL
  Could not find a version that satisfies the requirement OpenSSL (from versions: )
No matching distribution found for OpenSSL


解决办法：pip3.6 install pyopenssl
```

至此，scrapy startproject quote 命令成功执行

这次通过爬取  [Quotes to Scrape](http://quotes.toscrape.com/)这个网站，来使自己对于scrapy有个简单的了解。

这个网站是一个名言警句的网站，比较简单，好像是官方做出来让学习scrapy爬虫用的。

**items.py**代码分析

items.py里存放的是我们要爬取数据的字段信息:

text:文本信息

author：作者信息

tags： 标签信息

```python
import scrapy


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

```

**spiders/quotes.py**代码

spiders目录下的quotes.py为主要的爬虫代码，包括了对页面的请求以及页面的处理。

1. 我们爬取的页面时http://quotes.toscrape.com/，所以parse的response，返回的是这个页面的信息，但是我们这个时候需要的是获取下一页的地址继续访问，这里就用到了yield Request()这种用法，可以把获取到文章的url地址继续传递进来，使函数自己回调自己形成递归，再次进行请求。
2. scrapy提供了response.css这种的css选择器，我们可以根据自己的需求获取我们想要的字段信息
3. scrapy 使用

```python
# -*- coding: utf-8 -*-
import scrapy
from quote.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    #爬虫名称
    name="quotes" 
    #允许爬虫的域名
    allowed_domains = ["quotes.toscrape.com"]
    #开始的网址
    start_urls = ['http://quotes.toscrape.com/']

    # 请求start_urls成功之后得到的response,只需要解析就行了
    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item

        # 获取下一页的url
        next = response.css('.pager .next a::attr(href)').extract_first()
        # 获取绝对的url
        url = response.urljoin(next)
        yield scrapy.Request(url=url,callback=self.parse)

```

**pipelines.py**代码

pipeline主要是对spiders中爬虫的返回的数据的处理，这里我们可以让写入到数据库，也可以让写入到文件等等。

下面代码中主要包括的写入到json文件以及写入到数据库。

```python

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from scrapy.exceptions import DropItem

# item 的处理
# 文本信息超过50字段截断并加上 ‘...’
class TextPipeline(object):
    def  __init__(self):
        self.limit=50
    def process_item(self, item, spider):
        if item['text']:
            if len(item['text'])>self.limit:
                item['text'] = item['text'][0:self.limit].rstrip()+'...'
                return  item['text']
        else :
            return DropItem('Missing Text')


# 保存到MongoDB数据库
class MongoPipeLine(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db =mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        # 从配置文件setting中获取数据库连接信息
        return  cls(
            mongo_uri = crawler.setting.get('MONGO_URI'),
            mongo_db = crawler.setting.get('MONGO_DB')
        )

    # 爬虫启动时进行的相关操作
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    # item插入到MongoDB
    def process_item(self,item,spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()

```

上面在MongoPipeLine中用到了@classmethod：关于@classmethod的讲解https://blog.csdn.net/yzxnuaa/article/details/79862386

当自己添加了pipeline时，不要忘记 ： **Don't forget to add your pipeline to the ITEM_PIPELINES setting**

这里我们可以定义各种我们需要的pipeline，当然这里我们不同的pipeline是有一定的顺序的，需要的设置是在**settings.py**配置文件中，如下，后面的数字表示的是优先级，数字越小优先级越高。

**settings.py**代码

```python

BOT_NAME = 'quote'

SPIDER_MODULES = ['quote.spiders']
NEWSPIDER_MODULE = 'quote.spiders'

MONGO_URI = 'localhost'
MONGO_DB = 'quotes'
ROBOTSTXT_OBEY = True

# 需要将自己修改或添加的pipeline加入到ITEM_PIPELINES

ITEM_PIPELINES = {
   'quote.pipelines.TextPipeline': 300,
   'quote.pipelines.MongoPipeline': 400,

}
```

除了可以将爬取到的数据保存在数据库中，还可以将数据保存成自己指定的格式

保存爬取的内容json文件：
scrapy crawl quotes -o qutes.json

存取成单独的一行一行的数据
scrapy crawl quotes -o qutes.jl

远程ftp的保存格式
scrapy crawl quotes -o ftp://user:pass@ftp.example.com/path/quotes.csv
