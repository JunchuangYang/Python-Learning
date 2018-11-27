大佬的项目的地址[Proxy Pool](https://github.com/Python3WebSpider/ProxyPool)

# ProxyPool

## 安装

### 安装Python

至少Python3.5以上

### 安装Redis

安装好之后将Redis服务开启

### 配置代理池

```
cd proxypool
```

进入proxypool目录，修改settings.py文件

PASSWORD为Redis密码，如果为空，则设置为None

#### 安装依赖

```
pip3 install -r requirements.txt
```

#### 打开代理池和API

```
python3 run.py
```

## 获取代理


利用requests获取方法如下

```python
import requests

PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
```

----------

我在学习过程中遇到的一些问题。


为什么要用代理池？

许多网站有专门的反爬虫的措施，可能遇到封IP的问题。

互联网上公开了大量免费代理，利用好资源。

通过定时的检测维护同样可以得到多个可用代理。

代理池的要求：

多站抓取，异步检测。

定时筛选，持续更新。

提供接口，易于提取。

代理池架构：

![](https://i.imgur.com/XiL3mWb.jpg)


**改变标准输出的默认编码（这个比较重要一点，可以有效解决编码异常）**

```python
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

**Random.choice()**

choice() 方法返回一个列表，元组或字符串的随机项。

```python
from  random import choice

print "choice([1, 2, 3, 5, 9]) : ", random.choice([1, 2, 3, 5, 9])
print "choice('A String') : ", random.choice('A String')

output:

choice([1, 2, 3, 5, 9]) :  2
choice('A String') :  n 
```

**aiohttp的使用**

async，await 可以参考[一起来学python](http://www.cnblogs.com/c-x-a/p/9248906.html)


**元类的使用**

参见[两句话掌握python最难知识点——元类](https://segmentfault.com/a/1190000011447445)


## 项目中所用到的Redis的操作：

### set集合

有序集合：在集合的基础上，为每元素排序，元素的排序需要根据另外一个值来进行比较，所以，对于有序集合，每一个元素有两个值，即：值和分数，分数专门用来做排序。

**1.zrange，zrevrange**

```python

zrange( name, start, end, desc=False, withscores=False, score_cast_func=float)

zrevrange(name, start, end, withscores=False, score_cast_func=float) 同zrange，集合顺序是从大到小的

按照索引范围获取name对应的有序集合的元素

aa=r.zrange("zset_name",0,1,desc=False,withscores=True,score_cast_func=int)
print(aa)
参数：
    name    redis的name
    start   有序集合索引起始位置
    end     有序集合索引结束位置
    desc    排序规则，默认按照分数从小到大排序
    withscores  是否获取元素的分数，默认只获取元素的值
    score_cast_func 对分数进行数据转换的函数
```
**2.zscore**

```python
zscore(name, value)

#获取name对应有序集合中 value 对应的分数
print(r.zscore("zset_name","a1"))
```

**3.zadd**

```python
zadd(name, *args, **kwargs)

# 在name对应的有序集合中添加元素
r.zadd("zset_name", "a1", 6, "a2", 2,"a3",5)
#或
r.zadd('zset_name1', b1=10, b2=5)
```

**4.zrangebyscore**

```python
Redis Zrangebyscore 返回有序集合中指定分数区间的成员列表。有序集成员按分数值递增(从小到大)次序排列。

具有相同分数值的成员按字典序来排列(该属性是有序集提供的，不需要额外的计算)。

默认情况下，区间的取值使用闭区间 (小于等于或大于等于)，你也可以通过给参数前增加 ( 符号来使用可选的开区间 (小于或大于)。

举个例子：

ZRANGEBYSCORE zset (1 5
返回所有符合条件 1 < score <= 5 的成员，

而

ZRANGEBYSCORE zset (5 (10
则返回所有符合条件 5 < score < 10 的成员。
```

**5.zincrby**

```python
zincrby(name, value, amount)

#自增有序集合内value对应的分数
r.zincrby("zset_name","a1",amount=2)

#自增zset_name对应的有序集合里a1对应的分数
```

**6.zrem**

```python
#删除name对应的有序集合中值是values的成员

r.zrem("zset_name","a1","a2")
```

**7.zcard**

```python
zcard(name)

#获取有序集合内元素的数量
```

这只是极少的一部分Redis数据库中的操作，具体详见[J_hong](https://www.cnblogs.com/melonjiang/p/5342505.html)