# -*- coding:utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class Douban():
	def __init__(self):
		self.url = "http://www.douban.com/"
		# 使用PhantomJS报错
		#  Selenium support for PhantomJS has been deprecated, please use headless versions of Chrome or Firefox instead
		# self.driver = webdriver.PhantomJS()
		# 使用无头版的chrome
		chrome_options = Options()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		self.driver = webdriver.Chrome(chrome_options=chrome_options)
	def log_in(self):
		self.driver.get(self.url)
		time.sleep(3)
		#self.driver.save_screenshot("0.jpg")
		# 输入账号
		self.driver.find_element_by_xpath('//*[@id="form_email"]').send_keys("XXXX@qq.com")
		# 输入密码
		self.driver.find_element_by_xpath('//*[@id="form_password"]').send_keys("password")
		# 点击登录
		self.driver.find_element_by_xpath('//*[@id="lzform"]/fieldset/div[3]/input').click()
		time.sleep(3)
		#self.driver.save_screenshot('douban.jpg')
		# 输出登录后的cookies
		print(self.driver.get_cookies())
	def __del__(self):

		'''调用内建的稀构方法，在程序退出的时候自动调用
            类似的还可以在文件打开的时候调用close，数据库链接的断开'''
		self.driver.quit()

if __name__=='__main__':
	douban = Douban()
	douban.log_in()



