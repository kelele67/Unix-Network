# -*- coding:utf-8 -*-
"""
FTP服务器的客户端
"""
import socket
import getpass
import sys, time

print "Welcome to FTP client!"
serveraddr = ('127.0.0.1', 8888)
clientfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientfd.connect(serveraddr)

username = raw_input('User :')
clientfd.sendall(username.strip() + '\n')
password = getpass.getpass('Pass :')
clientfd.sendall(password.strip() + '\n')
infos = clientfd.recv(1024).strip()
print infos

if infos == "Auth Failed!":
    clientfd.close()
    print "Exit!"
    sys.exit()

while True:
    cmd = raw_input('ftp>')
    if not cmd:
        continue
    elif cmd.startswith('ls'):
        clientfd.send(cmd)
        # 设置socket为非阻塞
        clientfd.setblocking(0)
        while True:
            try:
                # 防止出错，做一个假的阻塞
                time.sleep(0.3)
                a = clientfd.recv(1024)
                print a
                if not len(a):
                    break
            except:
                break
        # 将socket还原成阻塞，否则下面的recv和send会报错
        clientfd.setblocking(1)

    elif cmd.startswith('help'):
        clientfd.send(cmd)
        print clientfd.recv(1024).strip()

    elif cmd.startswith('downloadfile'):
        filepath = cmd.split(' ')[2]
        clientfd.sendall(cmd)
        f = open(filepath, 'a')
        data = ''
        while True:
            a = clientfd.recv(1024).strip()
            data = data + a
            if a.endswith('file_end'):
                f.write(a.replace('file_end', ''))
                break
            f.write(data)
        f.close()

        print "Downloadfile Success! %s" % filepath

    elif cmd.startswith('uploadfile'):
        filepath = cmd.split(' ')[1]
        clientfd.sendall(cmd)
        f.open(filepath, 'rb')
        data = f.read()
        data = data + 'file_end'
        clientfd.sendall(data)
        f.close()
        print "Uploadfile Success! %s" % filepath

    elif cmd.startswith('quit'):
        print "bye~"
        break

    else:
        print "Unkonwn Service!"
        continue

clientfd.close()