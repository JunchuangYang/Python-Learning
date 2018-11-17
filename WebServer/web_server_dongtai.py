#-*- coding:utf-8 -*-
# __author__ = 'lenovo'


import multiprocessing
import re
import socket
import time

class WSGIServer(object):

    def __init__(self):
        """用来完成整体的控制"""
        # 1.创建套接字
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 2. 绑定
        self.tcp_server_socket.bind(("", 7890))
        # 3. 变为监听套接字
        self.tcp_server_socket.listen(128)

    def service_client(self,new_socket):
        # 1.接受浏览器发送过来的请求
        # get /HTTP/1.1
        # ....
        request = new_socket.recv(1024).decode("utf-8")
        request_lines = request.splitlines()
        print("")
        print(">"*20)
        print(request_lines)
        # GEt/index.html Http/1.1
        # get post put del
        file_name = ""
        ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
        if ret:
            file_name = ret.group(1)

            if file_name == "/":
                file_name = "/index.html"
        # 2.返回http个格式的数据，给浏览器
        # 2.1如果请求的资源不是以.py结尾的，那么就认为是静态资源（html/css/js/png/jpg）
        if not file_name.endswith(".py"):
            try:
                f = open("./html" + file_name,"rb")
            except:
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += '\r\n'
                response += '------file not found------'
                new_socket.send(response.encode("utf-8"))
            else:
                html_content = f.read()
                f.close()
                # 2.1 准备发送给浏览器的数据 --- header
                response = 'HTTP/1.1 200 OK\r\n'
                response += '\r\n'
                # 2.2准备发送个浏览器的数据 ---body
                # 将response header发送给浏览器
                new_socket.send(response.encode("utf-8"))
                # 将response body发送给浏览器
                new_socket.send(html_content)
        else :
            header = "HTTP/1.1 200 OK\r\n"
            header += "\r\n"
            body ="hahah %s"%time.ctime()
            response = header + body
            new_socket.send(response.encode("utf-8"))
        # 关闭套接字
        new_socket.close()

    def run_forever(self):
        while True:
            # 4. 等待新客户端的链接
            new_socket, client_addr = self.tcp_server_socket.accept()
            # 5. 为这个客户端服务
            p = multiprocessing.Process(target=self.service_client, args=(new_socket,))
            p.start()
            new_socket.close()
        # 关闭监听套接字
        self.tcp_server_socket.close()

def main():
    """控制整体，创建一个web服务器对象，然后调用这个对象的run_forever方法运行"""
    wsgi_server = WSGIServer()
    wsgi_server.run_forever()

if __name__ == '__main__':
    main()
