# **Urllib库详解**
  
## 1.什么是Urllib？  

Python的内置的HTTP请求库：  

urllib.request&ensp;&ensp;&ensp;&ensp; 请求模块  
urllib.error&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;异常处理模块  
urllib.parse&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;      url解析模块  
urllib.robotparser&ensp;&ensp;  robots.txt解析模块    

url 参数的使用  
    
    #  GET类型的请求
    import urllib.request
    
    response = urllib.request.urlopen('http://www.baidu.com')
    print(response.read().decode('utf-8'))#read()获取的字节流信息

urlopen一般常用的有三个参数，它的参数如下：  
urllib.requeset.urlopen(url,data,timeout)

    # post请求
    import urllib.parse
    import urllib.request
    
    data = bytes(urllib.parse.urlencode({'word':'hello'}),encoding='utf8')
    response = urllib.request.urlopen('http://httpbin.org/post',data=data)
    print(response.read())

# 超时时间
    import urllib.request
    
    response=urllib.request.urlopen('http://httpbin.org/get',timeout=1)
    print(response.read())

#
    import socket
    import urllib.request
    import urllib.error
    
    try:
    response =urllib.request.urlopen('http://httpbin.org/get',timeout=0.1)
    except urllib.error.URLError as e:
    if isinstance(e.reason,socket.timeout):
    print('TimeOut')
    
#
    import urllib.request
    
    response = urllib.request.urlopen('https://www.python.org')
    print(type(response))

#
    import urllib.request
    
    request =urllib.request.Request('https://python.org')
    response=urllib.request.urlopen(request)
    print(response.read().decode('utf-8'))
    
#
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
#    
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
#    
    import urllib.request
    
    proxy_handler = urllib.request.ProxyHandler({
    'http':'http://127.0.0.1:9743',
    'https':'https://127.0.0.1:9743'
    })#代理网址
    opener = urllib.request.build_opener(proxy_handler)
    reponse = opener.open('http://httpbin.org/get')
    print(reponse.read())
#    
    import http.cookiejar, urllib.request
    
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    reponse = opener.open('http://www.baidu.com')
    for item in cookie:
    print(item.name+"="+item.value)
#    
    import http.cookiejar, urllib.request
    
    filename = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    cookie.save(ignore_discard=True,ignore_expires=True)
#    
    import http.cookiejar, urllib.request
    
    cookie = http.cookiejar.MozillaCookieJar()
    cookie.load('cookie.txt',ignore_discard=True,ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    print(response.read().decode('utf-8'))
#    
    from urllib import request,error
    
    try:
    response = request.urlopen("http://pythonsite.com/1111.html")
    except error.URLError as e:
    print(e.reason)
#    
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
    import socket
    from urllib import error,request
    
    try:
    response = request.urlopen("http://www.pythonsite.com/",timeout=0.001)
    except error.URLError as e:
    print(type(e.reason))
    if isinstance(e.reason,socket.timeout):
    print("time,out")
#    
    from urllib.parse import urlparse
    
    result = urlparse("http://www.baidu.com/index.html;user?id=5#comment")
    print(result)
#    
    from urllib.parse import urlunparse
    
    data = ['http','www.baidu.com','index.html','user','a=123','commit']
    print(urlunparse(data))
#    
    from urllib.parse import urlencode
    
    params={
    "name":"YY",
    "age":23,
    }
    
    base_url = "http://www.baidu.com?"
    
    url = base_url+urlencode(params)
    print(url)