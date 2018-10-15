***文章来源 [coder](https://www.cnblogs.com/zhaof/p/6915127.html)***

##Requests基础

Requests是用python语言基于urllib编写的，采用的是Apache2 Licensed开源协议的HTTP库。

Requests比Urllib更加方便，requests是python实现的最简单易用的HTTP库，建议爬虫使用requests库。



    import requests
    
    response = requests.get("http://www.baidu.com")
    print(type(response))
    print(response.status_code)
    print(type(response.text))
    print(response.text)
    print(response.cookies)
    print(response.content)
    print(response.content.decode("utf-8"))
    #上述格式还有一种方法  
    response.encoding="utf-8"

我们可以观察到，最后两个代码输出的结果不同，上面输出的是乱码，很多情况下的网站如果直接response.text会出现乱码的问题,其实是response.content返回的数据格式是二进制的格式，需要用decode()进行解码.

# 
requests的各种请求方式

    import requests
    requests.post("http://httpbin.org/post")
    requests.put("http://httpbin.org/put")
    requests.delete("http://httpbin.org/delete")
    requests.head("http://httpbin.org/get")
    requests.options("http://httpbin.org/get")

Requests模块允许使用params关键字传递参数，以一个字典来传递这些参数

    import requests 
    
    data = {
    "name":"YY",
    "age":22
    }
    response = requests.get("http://httpbin.org/get",params=data)
    print(response.url)
    print(response.text)
结果为：

![](https://i.imgur.com/9WrOZ05.png)

Json解析

    import requests,json
    
    response = requests.get("http://httpbin.org/get")
    print(type(response.text))
    print(response.json())
    print(json.loads(response.text))
    print(type(response.json()))
结果为：
![](https://i.imgur.com/SgyMteG.png)

从结果可以看出requests里面集成的json其实就是执行了json.loads()方法，两者的结果是一样的

    import requests
    
    response = requests.get("http://www.zhihu.com")
    print(response.text)
    #不加headers的信息请求知乎无法访问

添加上头部信息后，知乎就可以正常访问了

    import requests
    
    headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get("https://www.zhihu.com",headers=headers)
    print(response.text)
    
#
基本POST请求

通过在发送post请求时添加一个data参数，这个data参数可以通过字典构造成，这样
对于发送post请求就非常方便

    import requests
    
    data = {
    "name":"YY",
    "age":22
    }
    response = requests.post("http://httpbin.org/post",data=data)
    print(response.text)

响应

我们可以通过response获得很多属性

    import requests
    
    response = requests.get("http://www.baidu.com")
    print(type(response.status_code),response.status_code)
    print(type(response.headers),response.headers)
    print(type(response.cookies),response.cookies)
    print(type(response.url),response.url)
    print(type(response.history),response.history)

结果为：
![](https://i.imgur.com/tGcaqA5.png)


    状态码判断
    Requests还附带了一个内置的状态码查询对象
    主要有如下内容：
    
    100: ('continue',),
    101: ('switching_protocols',),
    102: ('processing',),
    103: ('checkpoint',),
    122: ('uri_too_long', 'request_uri_too_long'),
    200: ('ok', 'okay', 'all_ok', 'all_okay', 'all_good', '\o/', '✓'),
    201: ('created',),
    202: ('accepted',),
    203: ('non_authoritative_info', 'non_authoritative_information'),
    204: ('no_content',),
    205: ('reset_content', 'reset'),
    206: ('partial_content', 'partial'),
    207: ('multi_status', 'multiple_status', 'multi_stati', 'multiple_stati'),
    208: ('already_reported',),
    226: ('im_used',),
    
    Redirection.
    300: ('multiple_choices',),
    301: ('moved_permanently', 'moved', '\o-'),
    302: ('found',),
    303: ('see_other', 'other'),
    304: ('not_modified',),
    305: ('use_proxy',),
    306: ('switch_proxy',),
    307: ('temporary_redirect', 'temporary_moved', 'temporary'),
    308: ('permanent_redirect',
    'resume_incomplete', 'resume',), # These 2 to be removed in 3.0
    
    Client Error.
    400: ('bad_request', 'bad'),
    401: ('unauthorized',),
    402: ('payment_required', 'payment'),
    403: ('forbidden',),
    404: ('not_found', '-o-'),
    405: ('method_not_allowed', 'not_allowed'),
    406: ('not_acceptable',),
    407: ('proxy_authentication_required', 'proxy_auth', 'proxy_authentication'),
    408: ('request_timeout', 'timeout'),
    409: ('conflict',),
    410: ('gone',),
    411: ('length_required',),
    412: ('precondition_failed', 'precondition'),
    413: ('request_entity_too_large',),
    414: ('request_uri_too_large',),
    415: ('unsupported_media_type', 'unsupported_media', 'media_type'),
    416: ('requested_range_not_satisfiable', 'requested_range', 'range_not_satisfiable'),
    417: ('expectation_failed',),
    418: ('im_a_teapot', 'teapot', 'i_am_a_teapot'),
    421: ('misdirected_request',),
    422: ('unprocessable_entity', 'unprocessable'),
    423: ('locked',),
    424: ('failed_dependency', 'dependency'),
    425: ('unordered_collection', 'unordered'),
    426: ('upgrade_required', 'upgrade'),
    428: ('precondition_required', 'precondition'),
    429: ('too_many_requests', 'too_many'),
    431: ('header_fields_too_large', 'fields_too_large'),
    444: ('no_response', 'none'),
    449: ('retry_with', 'retry'),
    450: ('blocked_by_windows_parental_controls', 'parental_controls'),
    451: ('unavailable_for_legal_reasons', 'legal_reasons'),
    499: ('client_closed_request',),
    
    Server Error.
    500: ('internal_server_error', 'server_error', '/o\', '✗'),
    501: ('not_implemented',),
    502: ('bad_gateway',),
    503: ('service_unavailable', 'unavailable'),
    504: ('gateway_timeout',),
    505: ('http_version_not_supported', 'http_version'),
    506: ('variant_also_negotiates',),
    507: ('insufficient_storage',),
    509: ('bandwidth_limit_exceeded', 'bandwidth'),
    510: ('not_extended',),
    511: ('network_authentication_required', 'network_auth', 'network_authentication'),
    
测试

    import requests
    
    response= requests.get("http://www.baidu.com")
    if response.status_code == requests.codes.ok:
    	print("访问成功")
    
#
文件上传

实现方法和其他参数类似，也是构造一个字典然后通过files参数传递

    import requests
    
    files = {"files":open("git.png","rb")}
    response = requsets.post("http://httpbin.org/post",files = files)
    print(response.text)


#
获取cookie
    
    import requests
    
    response = requests.get("http://www.baidu.com")
    print(response.cookies)
    
    for key,value in response.cookies.items():
    	print(key+"="+value)

#
cookie 的一个作用就是可以用于模拟登陆，做会话维持

    import requests
    
    s = requests.Session()
    s.get("http://httpbin.org/cookies/set/number/123456")
    response = s.get("http://httpbin.org/cookies")
    print(response.text)

这是正确的写法，而下面的写法则是错误的

    import requests
    
    requests.get("http://httpbin.org/cookies/set/number/123456")
    response = requests.get("http://httpbin.org/cookies")
    print(response.text)

**因为这种方式是两次requests请求之间是独立的，而第一次则是通过创建一个session对象，两次请求都通过这个对象访问**
 
#
证书验证

现在的很多网站都是https的方式访问，所以这个时候就涉及到证书的问题

    import requests
    
    response = requests.get("https://www.12306.cn")
    print(response.status_code)
    
    #结果为CertificateError      
#
解决方法：urllib3.disable_warnings()

verify=False

    import requests
    
    from requests.packages import urllib3
    
    urllib3.disable_warnings()
    response = requests.get("https://www.12306.cn",verify=False)
    print(response.status_code)

代理设置

    import requests
    
    proxies = {
    	"http":"http://127.0.0.1:9999",
    	"https":"http://127.0.0.1:8888"
    }
    response  = requests.get("https://www.baidu.com",proxies=proxies)
    print(response.text)

认证设置：如果碰到需要认证的网站可以通过requests.auth模块实现

    import requests
    
    from requests.auth import HTTPBasicAuth
    
    response = requests.get("http://120.27.34.24:9001/",auth=HTTPBasicAuth("user","123"))
    #还有一种方式
    #response = requests.get("http://120.27.34.24:9001/"),auth={"user","123"})
    
    print(response.status_code)

异常处理

关于reqeusts的异常在这里可以看到[详细内容](http://www.python-requests.org/en/master/api/#exceptions)

所有的异常都是在requests.excepitons中
    import requests
    
    from requests.exceptions import ReadTimeout,ConnectionError,RequestException
    
    try:
    	response = requests.get("http://httpbin.org/get",timeout=0.1)
    	print(response.status_code)
    except ReadTimeout:
    	print("timeout")
    except ConnectionError:
    	print("connection Errpr")
    except RequestException:
    	print("error")

HTTPError，ConnectionError,Timeout继承RequestionExceptionProxyError

SSLError继承ConnectionError

ReadTimeout继承Timeout异常