#导入相关模块
from multiprocessing import Process
from threading import Thread
from chuangkou.enter_enroll import Dengluzhuce
from chuangkou.homemoshi import HomeChat
import socket
from chuangkou.nimingliaotian import Nimingliaotian
from tkinter import *
import sys
import tkinter.font as tkfont
# from PIL import Image,ImageTk


HOST = '172.211.80.145'
# try:
#     with open('host.txt') as f:
#         HOST = f.readline()
# except Exception as e:
#     print('获取HOST错误内容是，',e)

PORT = 8888
addr = (HOST,PORT)
conn = ''

#主模块
def main():
    global  adrr,conn
    retu = 0
    #创建套接字
    sockfd = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #登录相关窗口启动
    screen = Dengluzhuce(sockfd,addr)
    screen.enter_Tk()
    #如果没登录直接退出了
    retu =screen.rootquit()
    print(retu)
    while retu:
        sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        screen.xuanzefangshi()
        x = screen.userxuanzeliaotianmoshi()
        x=x.split(':')
        if x[0] == '房间聊天':
            home = HomeChat(x[1], sockfd, addr)
            print('生成房间模式对象')
            home.root_main()
            retu = home.getretu()
            print('retu的值', retu)
        elif x[0] == '匿名聊天':
            niming = Nimingliaotian(x[1], sockfd, addr)
            niming.main()
            retu = niming.getretu()
        else:
            retu = 0
            sys.exit()




if __name__ == '__main__':
    main()