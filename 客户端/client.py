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


HOST = '192.168.1.132'
try:
    with open('host.txt') as f:
        HOST = f.readline()
except Exception as e:
    print('获取HOST错误内容是，',e)

PORT = 18888
root = Tk()
# root.geometry('300x200')
phont = PhotoImage(file='image/2.gif')

tkFont = tkfont.Font(family='Arial', size=14, weight=tkfont.BOLD)
def host():
    global  HOST
    HOST=e1.get()
    root.destroy()
ca = Canvas(root,

       # height=200,
       # width=300,
            )
ca.place(x=0,y=0)
ca.create_image((0,0),image=phont,anchor=NW)

ca.create_arc((10,10,90,100),fill='red',style=PIESLICE)
e1 = Entry(root,
           # bg='blue',
           font=tkFont,
           bd=0,
           fg='green',
           highlightcolor='yellow',
           insertbackground='pink',
           justify=CENTER,
           relief=FLAT,
           selectbackground='orange',
           )
e1.place(x=50,y=60)
Button(root,text='确定',activebackground='#64a131',cursor='hand2'
,compound='center',command=host).place(x=50,y=100)
root.mainloop()

with open('host.txt','w') as f:
    f.write(HOST)

print(HOST)
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