## Selenium模拟浏览器爬取淘宝美食
**Selenium （浏览器自动化测试框架）**

Selenium是一个用于Web应用程序测试的工具。Selenium测试直接运行在浏览器中，就像真正的用户在操作一样。支持的浏览器包括IE（7, 8, 9, 10, 11），Mozilla Firefox，Safari，Google Chrome，Opera等。这个工具的主要功能包括：测试与浏览器的兼容性——测试你的应用程序看是否能够很好得工作在不同浏览器和操作系统之上。测试系统功能——创建回归测试检验软件功能和用户需求。支持自动录制动作和自动生成 .Net、Java、Perl等不同语言的测试脚本。--百度百科

这次的项目爬今日头条的简单也好理解，所以就没有那么多的解释了，直接分析代码。

这次的项目没有运行成功，原因是淘宝需要登录才能查看信息，现在基本的思路是用淘宝账号真实的登录一下，然后获取到向服务器传递的所有参数信息，包括加密的密码，添加到headers中。（还没有尝试）


代码详解：

```python
# coding=utf-8
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from config import  *
import  pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

browser = webdriver.Chrome() #有操作界面的浏览器


# browser = webdriver.Chrome()  # 有头chrome


# 无操作界面chrome 设置参数
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# browser = webdriver.Chrome(chrome_options=chrome_options)


# 用phantomJS模拟
#browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
#browser_window_size(1400,900)
wait = WebDriverWait(browser,10)

# 搜索商品信息

def search():
    try:
        browser.get('https://www.taobao.com')
        # 获取搜索框。presence_of_all_elements_located--判断搜索框是否加载出来
        input = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#q'))
        )
        # 声明搜索按钮，EC.element_to_be_clickable--判断按钮是否可点击
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button'))
        )
        input[0].send_keys(KEYWORD) # 想搜索框中输入文字
        submit.click()  # 点击按钮
        # total为总页数，presence_of_element_located判断total元素已经加载完成
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_product()
        return total.text 
    except TimeoutException:
        return search()  # 递归，有错误集训搜索

# 模拟翻页
def next_page(page_number):
    try:
        input = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )
        input[0].clear()
        input[0].send_keys(page_number) # 输入页码
        submit.click()
        # 判断高亮是否是当前页数，从而判断是否翻页成功 
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number))
        )
        get_product()
    except TimeoutException:
        next_page(page_number)

# 获取商品信息
def get_product():
    # 等待item元素加载成功
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    # 获取网页源代码
    html = browser.page_source
        
    doc = pq(html)
    # items()返回一个生成器，生成每个item
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        # 根据css选择器获取想要的数据，构造字典
        product={
            'image' : item.find('.pic .img').attr('src'),
            'price' : item.find('.price').text(),
            'deal'  : item.find('.deal-cnt').text()[:-3],
            'title' : item.find('.title').text(),
            'shop'  : item.find('.shop').text(),
            'location' : item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try :
        if db[MONGO_TABLE].insert(result):
            print('存储到MongoDB成功',result)
    except Exception:
        print('存储到MongoDB错误',result)



def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        print(total)
        for i in range(2,total+1):
            next_page(i)
        browser.close()
    except Exception:
        print('出错了')
    finally:
        browser.close()

if __name__ == '__main__':
    main()
```