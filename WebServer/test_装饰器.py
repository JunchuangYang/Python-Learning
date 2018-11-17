#-*- coding:utf-8 -*-
__author__ = 'lenovo'

# 多个装饰器装饰一个函数
def set_call_1(func):
    def call_func():
        return "<h1>"+func()+"<h2>"
    return call_func

def set_call_2(func):
    def call_func():
        return "<td>"+func()+"</td>"
    return call_func

@set_call_1
@set_call_2
def get_str():
    return "haha"

print(get_str())


# 类装饰器
class Test(object):
    def __init__(self,func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("这里是装饰器添加的功能....")
        return self.func()


@Test # 相当于 get_str2 = Test(get_str2)
def get_str2():
    return "haha"

print(get_str2())


#通用装饰器
def set_func(func):
    def call_func(num,*args,**kwargs):
        print("权限验证1")
        print("权限验证2")

        #return func(args,kwargs) #不行，相当于传递了两个参数：一个元祖，一个字典
        return func(num,*args,**kwargs) #拆包
    return call_func

@set_func
def test1(num,*args,**kwargs):
    print("----test1----%d"%num)
    print("----test1----%d",args)
    print("----test1----%d",kwargs)
    return "ok"

print(test1(100))












