# -*- coding:utf-8 -*-
"""
使用SocketServer编写FTP服务功能
"""
import SocketServer
from SocketServer import ThreadingMixIn
from SocketServer import TCPServer
import os
import time

class MYTCPHandler(SocketServer.BaseRequestHandler):

    def confirm(self, username, password):
        if username == 'root' and password == 'password':
            return True
        else:
            return False

    def handle(self):
        while True:
            print "Connected by %s" % self.client_address[0]
            self.username = self.request.recv(1024)
            self.password = self.request.recv(1024)

            self.username = self.username.strip()
            self.password = self.password.strip()
            print "recv: %s %s" % (self.username, self.password)

            '''登录验证'''
            if not (self.username and self.password):
                break
            if not self.confirm(self.username, self.password):
                self.request.send("Auth Failed")
                break

            '''认证成功，开启功能'''
            self.request.send("Welcome, %s !" % self.username)
            while True:
                self.cmd = self.request.recv(1024).strip()
                if not self.cmd or self.cmd == 'quit':
                    break
                # 帮助信息
                elif self.cmd == 'help':  
                    helpinfo = ''' 
                    Help Info
                    [+]downloadfile [filename] [path]
                    [+]uploadfile [filename] [path]
                    [+]ls
                    [+]quit
                    ''' 
                    self.request.sendall(helpinfo)
                # 执行dir命令
                elif self.cmd.starstwith('ls'):
                    cmd_res = os.popen('ls').read()
                    self.request.sendall(cmd_res + '\0\n')

                # 下载文件
                elif self.cmd.startswith('downloadfile'):
                    downloadinfo = self.cmd.split(' ')
                    filepath = downloadinfo[1]
                    f = open(filepath, 'rb')
                    if not f:
                        break
                    data = f.read()
                    data = data + 'file_end'
                    self.request.sendall(data)
                    f.close()

                # 上传文件
                elif self.cmd.startswith('uploadfile'):
                    uploadinfo = self.cmd.split(' ')
                    filepath = uploadinfo[2]
                    data = ''
                    f = open(filepath, 'w')
                    while True:
                        a = self.request.recv(1024)
                        data = data + a
                        if a.endswith('file_end'):
                            f.write(a.replace('file_end', ''))
                            break
                        f.write(data)
                    f.close()
                    print "RECV file: %s" % filepath
                else:
                    pass

# 定义支持多线程的服务类，注意是多继承 
class ThreadingSocketServer(ThreadingMixIn, TCPServer):
    pass

if __name__ == '__main__':
    serveraddr = ('127.0.0.1', 8888)
    ftpserver = TCPServer(serveraddr, MYTCPHandler)
    ftpserver.serve_forever()