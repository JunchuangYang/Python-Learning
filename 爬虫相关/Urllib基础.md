***文章来源 [coder](https://www.cnblogs.com/zhaof/p/6910871.html)***

# **Urllib库详解**
  
## 1.什么是Urllib？  

Python的内置的HTTP请求库：  

urllib.request&ensp;&ensp;&ensp;&ensp; 请求模块  
urllib.error&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;异常处理模块  
urllib.parse&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;      url解析模块  
urllib.robotparser&ensp;&ensp;  robots.txt解析模块    

url 参数的使用  
urlopen一般常用的有三个参数，它的参数如下：  
urllib.requeset.urlopen(url,data,timeout)
    
GET类型的请求  

**response.read()的数据类型为bytes类型，需要用decode()来进行解码**。

    import urllib.request
    
    response = urllib.request.urlopen('http://www.baidu.com')
    print(response.read().decode('utf-8'))


post请求  

data参数需要**byte**类型，所以使用bytes()函数进行编码，而bytes()函数的第一个参数需要str类型，所以使用**urllib.parse.urllencode()**将字典转换为字符串。




    import urllib.parse
    import urllib.request
    
    data = bytes(urllib.parse.urlencode({'word':'hello'}),encoding='utf8')
    response = urllib.request.urlopen('http://httpbin.org/post',data=data)
    #urlopen方法的data要求传入的参数形式是二进制
    print(response.read())

设置请求超时时间（timeout），如果在这个时间内没有响应，程序将会抛出异常。
  
    import urllib.request
    
    response=urllib.request.urlopen('http://httpbin.org/get',timeout=1)
    print(response.read())

用try...except...来对异常进行抓取

    import socket
    import urllib.request
    import urllib.error
    
    try:
    response =urllib.request.urlopen('http://httpbin.org/get',timeout=0.1)
    except urllib.error.URLError as e:
    if isinstance(e.reason,socket.timeout):
    print('TimeOut')
    
响应（响应类型，状态码，响应头）

    import urllib.request
    
    response = urllib.request.urlopen('https://www.python.org')
    print(type(response))

我们可以通过response.status、response.getheaders().response.getheader("server")，获取状态码以及头部信息
response.read()获得的是响应体的内容


**request**

设置Headers

有很多网站为了防止程序爬虫爬网站造成网站瘫痪，会需要携带一些headers头部信息才能访问，最长见的有user-agent参数

简单实例

    import urllib.request
    
    request =urllib.request.Request('https://python.org')
    response=urllib.request.urlopen(request)
    print(response.read().decode('utf-8'))
    
给请求添加头部信息，模拟浏览器进行访问。

    from urllib import request,parse
    
    url='http://httpbin.org/post'
    headers={
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Host':'httpbin.org'
    }
    dict={
    'name':'YY'
    }
    
    data=bytes(parse.urlencode(dict),encoding='utf-8')#formdata,bytes类型的数据
    req = request.Request(url=url,data=data,headers=headers,method='POST')
    response=request.urlopen(req)
    print(reponse.read().decode('utf-8'))

添加请求头的第二种方式。

    from urllib import request,parse
    
    url='http://httpbin.org/post'
    dict={
    'name':'YY'
    }
    data= bytes(parse.urlencode(dict),encoding='utf-8')
    req = request.Request(url=url,data=data,method='POST')
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    response = request.urlopen(req)
    print(response.read().decode('utf-8'))

设置代理    

通过**rulllib.request.ProxyHandler()**可以设置代理,网站它会检测某一段时间某个IP 的访问次数，如果访问次数过多，它会禁止你的访问,所以这个时候需要通过设置代理来爬取数据

    import urllib.request
    
    proxy_handler = urllib.request.ProxyHandler({
    'http':'http://127.0.0.1:9743',
    'https':'https://127.0.0.1:9743'
    })#代理网址
    opener = urllib.request.build_opener(proxy_handler)
    reponse = opener.open('http://httpbin.org/get')
    print(reponse.read())
#   
cookie中保存中我们常见的登录信息，有时候爬取网站需要携带cookie信息访问,这里用到了http.cookijar，用于获取cookie以及存储cookie

 
    import http.cookiejar, urllib.request
    
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    reponse = opener.open('http://www.baidu.com')
    for item in cookie:
        print(item.name+"="+item.value)
#   

同时cookie可以写入到文件中保存，有两种方式**http.cookiejar.MozillaCookieJar()**和**http.cookiejar.LWPCookieJar()**，当然你自己用哪种方式都可以 
    import http.cookiejar, urllib.request
    
    filename = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    cookie.save(ignore_discard=True,ignore_expires=True)
#    

同样的如果想要通过获取文件中的cookie获取的话可以通过load方式，当然用哪种方式写入的，就用哪种方式读取。


    import http.cookiejar, urllib.request
    
    cookie = http.cookiejar.MozillaCookieJar()
    cookie.load('cookie.txt',ignore_discard=True,ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    print(response.read().decode('utf-8'))
#    

异常处理

    from urllib import request,error
    
    try:
    response = request.urlopen("http://pythonsite.com/1111.html")
    except error.URLError as e:
    print(e.reason)
#    
这里我们需要知道的是在urllb异常这里有两个个异常错误：  

URLError,HTTPError，HTTPError是URLError的子类

**URLError里只有一个属性：reason**,即抓异常的时候只能打印错误信息，类似上面的例子

**HTTPError里有三个属性：code,reason,headers**，即抓异常的时候可以获得code,reson，headers三个信息，



    from urllib import request,error
    
    try:
    	response = request.urlopen("http://pythonsite.com/1111.html")
    except error.HTTPError as e:
    	print (e.reason)
    	print (e.code)
   		print (e.headers)
    except error.URLError as e:
    	print(e.reason)
    
    else:
    	print("request successfully!")
    
#    
同时，e.reason其实也可以在做深入的判断

    import socket
    from urllib import error,request
    
    try:
    	response = request.urlopen("http://www.pythonsite.com/",timeout=0.001)
    except error.URLError as e:
    	print(type(e.reason))
    if isinstance(e.reason,socket.timeout):
    	print("time,out")
#
URL解析

拆分url


    from urllib.parse import urlparse
    
    result = urlparse("http://www.baidu.com/index.html;user?id=5#comment")
    print(result)
结果为：
![](https://i.imgur.com/uQOG5wF.png)

拼接URL
    
    from urllib.parse import urlunparse
    
    data = ['http','www.baidu.com','index.html','user','a=123','commit']
    print(urlunparse(data))


#    
urlencode()这个方法可以将字典转换为url参数

    from urllib.parse import urlencode
    
    params={
    "name":"YY",
    "age":23,
    }
    
    base_url = "http://www.baidu.com?"
    
    url = base_url+urlencode(params)
    print(url)
结果为：

![](https://i.imgur.com/iJe8DLj.png)