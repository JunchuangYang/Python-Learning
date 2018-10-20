文章来源 [coder](https://www.cnblogs.com/zhaof/p/6953241.html)

## selenium基础

[selenium中文文档](https://selenium-python-zh.readthedocs.io/en/latest/index.html)

**selenium** 是一套完整的web应用程序测试系统，包含了测试的录制（selenium IDE）,编写及运行（Selenium Remote Control）和测试的并行处理（Selenium Grid）。Selenium的核心Selenium Core基于JsUnit，完全由JavaScript编写，因此可以用于任何支持JavaScript的浏览器上。

selenium可以模拟真实浏览器，自动化测试工具，支持多种浏览器，爬虫中主要用来解决JavaScript渲染问题。

**基本使用**

```
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
    input = browser.find_element_by_id('kw')  #获取百度页面中id为kw的输入框
    input.send_keys('Python')                 #向输入框中写入关键字
    input.send_keys(Keys.ENTER)                 
    wait = WebDriverWait(browser, 10)         #浏览器等待10秒
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))   

    #直到id为content_left加载成功等待结束，或时间到了直接抛出TimeOut的错误

    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.page_source)
finally:
    browser.close()

output：

整个程序的输出结果是，浏览器自动执行输入Python关键字并搜索，然后输出当前网址的url，
cookie和网页源代码
```

**声明浏览器对象**

调用各种浏览器的方法

```
from selenium import webdriver

browser = webdriver.Chrome()
browser = webdriver.Firefox()
browser = webdriver.Edge()
browser = webdriver.PhantomJS()
browser = webdriver.Safari()
```


**访问页面**

```

from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
print(browser.page_source)
browser.close()

```

**查找元素**

单个元素

这里我们通过三种不同的方式去获取响应的元素，第一种是通过id的方式，第二个中是CSS选择器，第三种是xpath选择器，结果都是相同的。

```
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input_first  = browser.find_element_by_id('q')
input_second = browser.find_element_by_css_selector('#q')
imput_third = browser.find_element_by_xpath('//*[@id="q"]')
print(input_first, input_second, input_third)
browser.close()
```

常用的查找元素的方法：

```
find_element_by_name
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector

```

还有一种方法：这里需要记住By模块所以需要导入
from selenium.webdriver.common.by import By

```
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input_first = browser.find_element(By.ID, 'q')
print(input_first)
browser.close()

```

**查找多个元素**

其实多个元素和单个元素的区别，举个例子：find_elements,单个元素是find_element,其他使用上没什么区别，通过其中的一个例子演示：

```
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
lis = browser.find_elements_by_css_selector('.service-bd li')
print(lis)
browser.close()

#输出结果是一个列表

```

当然上面的方式也是可以通过导入from selenium.webdriver.common.by import By 这种方式实现

lis = browser.find_elements(By.CSS_SELECTOR,'.service-bd li')

同样的在单个元素中查找的方法在多个元素查找中同样存在：

```
find_elements_by_name
find_elements_by_id
find_elements_by_xpath
find_elements_by_link_text
find_elements_by_partial_link_text
find_elements_by_tag_name
find_elements_by_class_name
find_elements_by_css_selector
```

**元素交互操作**

对获取的元素调用交互方法

```
from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input = browser.find_element_by_id('q')
input.send_keys('iPhone')
time.sleep(1)
input.clear()
input.send_keys('iPad')
button = browser.find_element_by_class_name('btn-search')
button.click()

#
运行的结果可以看出程序会自动打开Chrome浏览器并打开淘宝输入iPhone,然后删除，重新输入iPad，并点击搜索
```
更多操作:[selenium](http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webelement)

**交互动作**

将动作附加到动作链接中串行执行

```
from selenium import webdriver
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to.frame('iframeResult')
source = browser.find_element_by_css_selector('#draggable')
target = browser.find_element_by_css_selector('#droppable')
actions = ActionChains(browser)
actions.drag_and_drop(source, target)
actions.perform()


```
更多操作参考：[selenium-python](http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains)

**执行JavaScript**

这是一个非常有用的方法，这里就可以直接调用js方法来实现一些操作，

下面的例子是通过登录知乎然后通过js翻到页面底部，并弹框提示

```
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')

```
**获取元素信息**

获取属性

```
from selenium import webdriver
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
logo = browser.find_element_by_id('zh-top-link-logo')
print(logo)
print(logo.get_attribute('class'))

```

**获取文本值**

```
from selenium import webdriver

browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
input = browser.find_element_by_class_name('zu-top-add-question')
print(input.text)

output:提问


```

**获取ID、位置、标签名、大小**

```
from selenium import webdriver

browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
input = browser.find_element_by_class_name('zu-top-add-question')
print(input.id)
print(input.location)
print(input.tag_name)
print(input.size)

```

**Frame**

在很多网页中都是有Frame标签，所以我们爬取数据的时候就涉及到切入到frame中以及切出来的问题，通过下面的例子演示

这里常用的是switch_to.from()和switch_to.parent_frame()

```
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to.frame('iframeResult')
source = browser.find_element_by_css_selector('#draggable')
print(source)
try:
    logo = browser.find_element_by_class_name('logo')
except NoSuchElementException:
    print('NO LOGO')
browser.switch_to.parent_frame()
logo = browser.find_element_by_class_name('logo')
print(logo)
print(logo.text)
```

**等待**

隐式等待

当使用了隐式等待执行测试的时候，如果 WebDriver没有在 DOM中找到元素，将继续等待，超出设定时间后则抛出找不到元素的异常, 换句话说，当查找元素或元素并没有立即出现的时候，隐式等待将等待一段时间再查找 DOM，默认的时间是0

```
from selenium import webdriver

browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.get('https://www.zhihu.com/explore')
input = browser.find_element_by_class_name('zu-top-add-question')
print(input)
```

**显示等待**

指定一个等待条件，并且指定一个最长等待时间，会在这个时间内进行判断是否满足等待条件，如果成立就会立即返回，如果不成立，就会一直等待，直到等待你指定的最长等待时间，如果还是不满足，就会抛出异常，如果满足了就会正常返回

```
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.get('https://www.taobao.com/')
wait = WebDriverWait(browser, 10)
input = wait.until(EC.presence_of_element_located((By.ID, 'q')))
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btnsearch')))
print(input, button)
```

上述的例子中的条件：

EC.presence_of_element_located（）是确认元素是否已经出现了

EC.element_to_be_clickable（）是确认元素是否是可点击的

```
title_is 标题是某内容
title_contains 标题包含某内容
presence_of_element_located 元素加载出，传入定位元组，如(By.ID, 'p')
visibility_of_element_located 元素可见，传入定位元组
visibility_of 可见，传入元素对象
presence_of_all_elements_located 所有元素加载出
text_to_be_present_in_element 某个元素文本包含某文字
text_to_be_present_in_element_value 某个元素值包含某文字
frame_to_be_available_and_switch_to_it frame加载并切换
invisibility_of_element_located 元素不可见
element_to_be_clickable 元素可点击
staleness_of 判断一个元素是否仍在DOM，可判断页面是否已经刷新
element_to_be_selected 元素可选择，传元素对象
element_located_to_be_selected 元素可选择，传入定位元组
element_selection_state_to_be 传入元素对象以及状态，相等返回True，否则返回False
element_located_selection_state_to_be 传入定位元组以及状态，相等返回True，否则返回False
alert_is_present 是否出现Alert

```
[详细内容](http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions)

**前进后退**

```
import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.baidu.com/')
browser.get('https://www.taobao.com/')
browser.get('https://www.python.org/')
browser.back()
time.sleep(1)
browser.forward()
browser.close()
```

**Cookies**

```
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
print(browser.get_cookies())
browser.add_cookie({'name': 'name', 'domain': 'www.zhihu.com', 'value': 'germey'})
print(browser.get_cookies())
browser.delete_all_cookies()
print(browser.get_cookies())

```

**选项卡管理**

通过执行js命令实现新开选项卡window.open()

不同的选项卡是存在列表里browser.window_handles

通过browser.window_handles[0]就可以操作第一个选项卡

```
import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.execute_script('window.open()')
print(browser.window_handles)
browser.switch_to_window(browser.window_handles[1])
browser.get('https://www.taobao.com')
time.sleep(1)
browser.switch_to_window(browser.window_handles[0])
browser.get('https://python.org')

```

**异常处理**

```
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
except TimeoutException:
    print('Time Out')
try:
    browser.find_element_by_id('hello')
except NoSuchElementException:
    print('No Element')
finally:
    browser.close()
```