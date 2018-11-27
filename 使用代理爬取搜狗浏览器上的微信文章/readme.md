 ## 使用代理爬取搜狗浏览器上的微信文章

### 流程框架

![](https://i.imgur.com/OvgDwbs.png)

### 全局变量

```python

# 不变的URL的信息
base_url = 'https://weixin.sogou.com/weixin?'
# 使用cookie 以及 需要传递的参数字符串
headers = {
    'Cookie': 'SUV=006B71D7DF5BD8345B7660A775D2B520; SMYUV=1539747960285644; IPLOC=CN1304; SUID=F909C6B7541C940A000000005BD26754; ABTEST=6|1540515669|v1; SNUID=9464AADA6C69157B2C2A33A36DF7D0A3; weixinIndexVisited=1; sct=1; JSESSIONID=aaa4ZSXSubIC1ae6-lIzw; ppinf=5|1540517252|1541726852|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNDpKdXN0JTIwYSUyMCUyMFglRUYlQkMlODF8Y3J0OjEwOjE1NDA1MTcyNTJ8cmVmbmljazoyNDpKdXN0JTIwYSUyMCUyMFglRUYlQkMlODF8dXNlcmlkOjQ0Om85dDJsdUlKLXFDbDdKUE5VOGlRREFJeTdoNWNAd2VpeGluLnNvaHUuY29tfA; pprdig=Kh_XW3wdeuljDBo5A3hA1gPS_EqVAdaCKCoxG0tQ5TCk_h6ksm9_QaBeePcg8uYtwRjriU6mvebrkXdfbM1R6LhJNyGQ7Di8lw13uj8JuoOAEbEIAQrqq2umx9CbAKdSWbkK5vbgyY4HYZynd27iVNtWS5wS9qVpAKdsiyJTvlY; sgid=04-35568889-AVvSbYQY4ayenEEia81OSsRQ; ppmdig=15405172530000000eaa3477479224333f117411eb04b128',
    'Host': 'weixin.sogou.com',
    'Referer': 'https://weixin.sogou.com/weixin?query=%E9%A3%8E%E6%99%AF&_sug_type_=&sut=1833&lkt=1%2C1540515730996%2C1540515730996&s_from=input&_sug_=y&type=2&sst0=1540515731099&page=100&ie=utf8&w=01019900&dr=1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
# 搜索关键字
keyword = '风景'
# 使用的代理池的地址，并随机获取代理信息
proxy_pool_url = 'http://127.0.0.1:5555/random'
proxy = None
max_count = 5 # 最大请求次数的判断
```

### 构造url,获取索引页的信息

```python
# 搜索关键字以及页数
def get_index(keyword,page):
    # Query String Parameters
    data = {
        'query' : keyword,
        'type' : 2,
        'page' : page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html
```
### pqyuery解析索引页信息，获取详情页，也就是微信文章的url

```python
def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield  item.attr('href')
```

### 代理IP的实现

```python
def get_html(url,count=1):
    print('Crawling:',url)
    print('Tring Count:',count)
    #使用global声明全局变量，声明后可在函数内改变proxy的值
    global proxy
    # 设置最大尝试次数
    if count >max_count:
        print('Tried Too Many Counts')
        return None
    try:
        # 构造代理地址
        if proxy:
            proxies={
                'http':'http://'+proxy
            }
            # allow_redirects=False，关闭重定向，不让它自动处理跳转，默认为True
            response = requests.get(url,allow_redirects=False,headers = headers,proxies=proxies)
        else :
            # 如果代理为空，使用本机IP
            response = requests.get(url,allow_redirects=False,headers = headers)


        if response.status_code == 200:
            return  response.text
        # 302错误，IP被封
        if response.status_code == 302:
            print('302')
            #当前IP已经被封，需要代理
            proxy = get_proxy()
            if proxy:
                print('Using:',proxy)
                return get_html(url)
            else :
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred!',e.args)
        proxy = get_proxy()
        # 连接失败，次数加一
        count +=1
        return get_html(url,count)
```

### 代理IP地址的获取

```python
def get_proxy():
    try:
        # 由于当前使用的连接池比较简单，返回来的就是随机的一个代理IP的地址（response.text），
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return  None
    except ConnectionError:
        return None
```
### pyquery 解析详情页的url ，获取 文章的标题，内容，时间，昵称，微信号

**注：在解析HTML代码的时候，data时间信息获取不到内容，在开发者工具的response中看，发现包含着时间的标签<em></em>内没有内容。但在elements中看可以看到时间的信息，此问题还没有解决。**

```python
def parse_detail(html):
    try:
        doc = pq(html)

        title = doc('#activity-name').text()
        content = doc('#js_content').text().replace('\n','')
        date = doc('#publish_time').text()#获取不到时间信息
        nickname = doc('#js_name').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()

        return {
            'title':title,
            'content':content,
            'date': date,
            'nickname' : nickname,
            'wechat':wechat
        }
    except :
        return None
```

### 将获取的数据存储到MONGODB中，并去重

mongodb数据库的连接信息

```python
client = pymongo.MongoClient('localhost')
db = client['weixin']
```
存储信息

```python
def save_to_mongo(data):
    # 去重
    # MongoDB中update()使用'$set'指定一个键的值，如果不存在该值就创建（去重）
    #multi：默认是false，只更新找到的第一条记录。如果为true，把按条件查询出来的记录全部更新。
    if db['articles'].update({'title':data['title']},{'$set':data},True):
        print('save to Mongo',data['title'])
    else :
        print('save to Mongo failed',data['title'])
```


----------

### 所遇到的问题

**代码中存在汉字注释**

```python
#_*_ coding:gb2312_*_

#如果是汉字注释，需要在代码开头加上_*_ coding:gb2312_*_
```

**print代码输出时遇到编码错误**

```python
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
#改变标准输出的默认编码
```

上次代理池项目中有一个是改变输出编码为sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8'),这个输出没有错误，在cmd中输出的中文乱码。

python编码的问题真是头疼，目前我只是遇到问题就百度，然后解决。

具体信息参见 https://blog.csdn.net/wpy110521/article/details/80998207

**MongoDB中update()**

update命令

update命令格式：

db.collection.update(criteria,objNew,upsert,multi)

参数说明：

criteria：查询条件

objNew：update对象和一些更新操作符

upsert：如果不存在update的记录，是否插入objNew这个新的文档，true为插入，默认为false，不插入。

multi：默认是false，只更新找到的第一条记录。如果为true，把按条件查询出来的记录全部更新。

具体信息参见 [不爱吃汤圆的汤圆坨坨](https://blog.csdn.net/wenwen360360/article/details/78339221)