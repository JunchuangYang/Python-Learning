#_*_ coding:gb2312_*_
#encoding=utf-8
# #如果是汉字注释，需要在代码开头加上_*_ coding:gb2312_*_
import requests
from urllib.parse import  urlencode
from requests.exceptions import  ConnectionError
from pyquery import PyQuery as pq
import io
import sys
import re
import pymongo

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
client = pymongo.MongoClient('localhost')
db = client['weixin']



base_url = 'https://weixin.sogou.com/weixin?'
headers = {
    'Cookie': 'SUV=006B71D7DF5BD8345B7660A775D2B520; SMYUV=1539747960285644; IPLOC=CN1304; SUID=F909C6B7541C940A000000005BD26754; ABTEST=6|1540515669|v1; SNUID=9464AADA6C69157B2C2A33A36DF7D0A3; weixinIndexVisited=1; sct=1; JSESSIONID=aaa4ZSXSubIC1ae6-lIzw; ppinf=5|1540517252|1541726852|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNDpKdXN0JTIwYSUyMCUyMFglRUYlQkMlODF8Y3J0OjEwOjE1NDA1MTcyNTJ8cmVmbmljazoyNDpKdXN0JTIwYSUyMCUyMFglRUYlQkMlODF8dXNlcmlkOjQ0Om85dDJsdUlKLXFDbDdKUE5VOGlRREFJeTdoNWNAd2VpeGluLnNvaHUuY29tfA; pprdig=Kh_XW3wdeuljDBo5A3hA1gPS_EqVAdaCKCoxG0tQ5TCk_h6ksm9_QaBeePcg8uYtwRjriU6mvebrkXdfbM1R6LhJNyGQ7Di8lw13uj8JuoOAEbEIAQrqq2umx9CbAKdSWbkK5vbgyY4HYZynd27iVNtWS5wS9qVpAKdsiyJTvlY; sgid=04-35568889-AVvSbYQY4ayenEEia81OSsRQ; ppmdig=15405172530000000eaa3477479224333f117411eb04b128',
    'Host': 'weixin.sogou.com',
    'Referer': 'https://weixin.sogou.com/weixin?query=%E9%A3%8E%E6%99%AF&_sug_type_=&sut=1833&lkt=1%2C1540515730996%2C1540515730996&s_from=input&_sug_=y&type=2&sst0=1540515731099&page=100&ie=utf8&w=01019900&dr=1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
keyword = '风景'
proxy_pool_url = 'http://127.0.0.1:5555/random'
proxy = None
max_count = 5 # 最大请求次数的判断


def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return  None
    except ConnectionError:
        return None

def get_html(url,count=1):
    print('Crawling:',url)
    print('Tring Count:',count)
    global proxy
    if count >max_count:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:
            proxies={
                'http':'http://'+proxy
            }
            # 不让它自动处理跳转
            response = requests.get(url,allow_redirects=False,headers = headers,proxies=proxies)
        else :
            response = requests.get(url,allow_redirects=False,headers = headers)


        if response.status_code == 200:
            return  response.text
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
        count +=1
        return get_html(url,count)

def get_indx(keyword,page):
    data = {
        'query' : keyword,
        'type' : 2,
        'page' : page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield  item.attr('href')

def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return  response.text
        return None
    except ConnectionError:
        return None

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

def save_to_mongo(data):
    # 去重
    if db['articles'].update({'title':data['title']},{'$set':data},True):
        print('save to Mongo',data['title'])
    else :
        print('save to Mongo failed',data['title'])


def main():
    for i in range(1,101):
        html =get_indx(keyword,i)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    print(article_data)
                    #if data: save_to_mondo(data)


if __name__ == '__main__':
    main()
