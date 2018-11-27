# -*- coding=utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
class Douyu(object):
	"""docstring for douyu"""
	def __init__(self):
		chrome_options=Options()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		self.driver = webdriver.Chrome(chrome_options=chrome_options)
		self.driver.get("https://www.douyu.com/directory/all")

	def get_content(self):
		time.sleep(3) #每次发送完请求等待三秒，等待页面加载完成
		li_list =self.driver.find_elements_by_xpath('//*[@id="live-list-contentbox"]/li')

		content = []

		for li in li_list:
			item={}
			item['img']=li.find_element_by_xpath('./a//img').get_attribute('src')
			item['title'] = li.find_element_by_xpath('./a').get_attribute('title')
			item['category'] = li.find_element_by_xpath("./a/div[@class='mes']/div/span").text
			item['name'] = li.find_element_by_xpath("./a/div['mes']/p/span[1]").text
			item['watch_num'] = li.find_element_by_xpath("./a/div['mes']/p/span[2]").text
			#print(item)
			content.append(item)
		return content
	#保存内容
	def save_content(self,contents):
		with open("F:\\douyu.txt",'a',encoding='utf-8') as f:
			for content in contents:
				json.dump(content,f,ensure_ascii=False,indent=2)
				f.write('\n')
	def run(self):
		#1.发送首页的请求
        #2.获取第一页的信息
		contents = self.get_content();
		self.save_content(contents)
		#3.循环  点击下一页按钮，知道下一页对应的class名字不再是"shark-pager-next"
		#判断有没有下一页
		while self.driver.find_element_by_class_name('shark-pager-next'):
			#点击下一页的按钮
			self.driver.find_element_by_class_name('shark-pager-next').click()
			# 4.继续获取下一页的内容
			contents = self.get_content()
			self.save_content(contents)

if __name__ =='__main__':
	douyu=Douyu()
	douyu.run()
