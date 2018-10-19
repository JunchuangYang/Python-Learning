# coding=gbk
import  requests
from multiprocessing import Pool
from requests.exceptions import RequestException
import re,json,time

def get_one_page(url):
    #爬取猫眼现在需要添加headers信息，否则可能爬取不到
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      +'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?'
                         +'class="star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?'
                         +'fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html) #返回的是一个list，每一个list是一个元祖
    for item in items:
        yield {
            'index' : item[0],
            'image' : item[1],
            'title' : item[2],
            'actor' : item[3].strip()[3:],#strip()去除换行符，[3:]使用切片来去除主演
            'time' : item[4].strip()[5:],
            'score' : item[5]+item[6]
        }#生成器

def write_to_file(item):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(item , ensure_ascii=False) + '\n') #json.dumps()将dict的数据类型转换为字符串
        #json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False：
        f.close()

#图片下载
def pic_download(url,title):
    r = requests.get(url)
    with open("pics/" + title +".jpg","wb") as f:
        f.write(r.content)

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for  item in parse_one_page(html):
        write_to_file(item)
        pic_download(item['image'],item['title'])

if __name__ == '__main__':
    for i in range(10):
        main(i*10)
#   添加多线程后会出现爬取不完整和顺序错乱问题，目前还没有解决
#    pool = Pool()
#    pool.map(main,[ i*10 for i in range(10)])


