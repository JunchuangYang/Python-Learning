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

browser = webdriver.Chrome()
#browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
#browser_window_size(1400,900)
wait = WebDriverWait(browser,10)

def search():
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#q'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button'))
        )
        input[0].send_keys(KEYWORD)
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_product()
        return total.text
    except TimeoutException:
        return search()

def next_page(page_number):
    try:
        input = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )
        input[0].clear()
        input[0].send_keys(page_number)
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number))
        )
        get_product()
    except TimeoutException:
        next_page(page_number)

def get_product():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
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