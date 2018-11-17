#-*- coding:utf-8 -*-
__author__ = 'lenovo'

def index():
    with open('./templates/index.html',encoding='utf-8') as f:
        return f.read()

def center():
    with open('./templates/center.html',encoding='utf-8') as f:
        return  f.read()

# environ 字典属性; start_response:函数的引用
def application(environ,start_response):
    start_response('200 OK',[('content-Type','text/html;charset=utf-8')])

    file_name = environ['PATH_INFO']
    if file_name == '/index.py':
        return index()
    elif file_name == '/center.py':
        return center()
    else:
        return 'Hello Word! 我爱你中国...'
