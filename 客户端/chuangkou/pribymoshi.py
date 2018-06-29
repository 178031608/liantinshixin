from tkinter import *
from threading import Thread
import time
from .weather import getAllWeather
import socket
from tkinter import filedialog
from .wenjianjieshou import Wenjianjieshou
from .wenjianfasong import Wenjian
from multiprocessing import Process
import os
import tkinter.font as tkfont
import random


class Pribymoshi:
    def __init__(self,sockfd,username,othername,serveraddr):
        self.sockfd = sockfd
        self.othername = othername
        self.myname = username
        self.serveraddr = serveraddr
        self.city='天津'

    #获取时间函数
    def showtime(self):
        s = time.strftime('%Y-%m-%d %H:%M:%S')
        return s+'\n'

    #发送消息按钮功能
    def sendtouserinfo(self):
        data = self.inputinfo.get(0.0,'end')
        s = self.showtime()
        self.showinfo.config(state=NORMAL)
        self.showinfo.insert('end',s,'yred')
        self.showinfo.insert('end','我说:'+data)
        self.showinfo.see('end')
        self.showinfo.config(state=DISABLED)
        self.inputinfo.delete(0.0,'end')
        #然后在发送该消息
        msg = '*发送给:'+self.othername+':'+self.myname+':'+data.rstrip('\n')
        self.sockfd.sendto(msg.encode(),self.serveraddr)

    #新消息来了
    def newinfo(self,data):
        s = self.showtime()
        self.showinfo.config(state=NORMAL)
        self.showinfo.insert('end',s,'yred')
        self.showinfo.insert('end',data)
        self.showinfo.see('end')
        self.showinfo.config(state=DISABLED)

    #发送机器人消息按钮
    def sendtoaiinfo(self):
        # 从输入框获取用户输入信息
        da = self.inputinfo.get(0.0, 'end')
        data = '*私聊机器人消息:' + da
        self.sockfd.sendto(data.encode(), self.serveraddr)
        # 获取时间格式信息
        s = self.showtime()
        self.aiinfo.config(state=NORMAL)
        self.aiinfo.insert('end', s,'yred')
        self.aiinfo.insert('end','我说:'+da)
        self.aiinfo.see('end')
        self.aiinfo.config(state=DISABLED)
        # 清空输入框
        self.inputinfo.delete(0.0, 'end')

    #机器人的返回消息
    def aiinfos(self,data):
        s = self.showtime()
        self.aiinfo.config(state=NORMAL)
        self.aiinfo.insert('end',s,'yred')
        self.aiinfo.insert('end','机器人说:'+data)
        self.aiinfo.see('end')
        self.aiinfo.config(state=DISABLED)

    #发送用户天气输入
    def weathersendto(self):
        while True:
            city = self.city
            try:
                cityweather = getAllWeather(self.city)
                if not cityweather:
                    data = '输入城市不正确\n现在的城市是:'+city
                    img = 'image/weathersiliao/chushihua.png'
                    self.weather.config(fg='#FFFF00')
                    openimage = PhotoImage(file=img)
                    self.weathertext.set(data)
                    self.weather.config(image=openimage)
                    continue
                else:
                    # print('s',cityweather)
                    for x in cityweather:
                        for z in x:
                            if self.city != city:
                                continue
                            time.sleep(5)
                            t = z.split(',')
                            # print('天气里的data准备切割', t)
                            data = self.city + ':' + t[0] + '\n天气:' + t[2] + '\n温度:' + t[3] + '\n风向:' + \
                                   t[4] + '\n风力:' + t[5]
                            if t[2] == '晴':
                                img = 'image/weather/qingtian.png'
                                self.weather.config(fg='yellow')
                            elif t[2] == '多云':
                                img = 'image/weather/duoyun.png'
                                self.weather.config(fg='#00FA9A')
                            elif t[2] == '暴雨' or t[2] == '大雨':
                                img = 'image/weather/baoyu.png'
                                self.weather.config(fg='yellow')
                            elif t[2] == '晴转多云':
                                img = 'image/weather/qingzhuanduoyun.png'
                                self.weather.config(fg='yellow')
                            elif t[2] == '中雨':
                                img = 'image/weather/zhongyu.png'
                                self.weather.config(fg='yellow')
                            elif t[2] == '小雨转多云':
                                img = 'image/weather/xiaoyuzhuanduoyun.png'
                                self.weather.config(fg='yellow')
                            elif t[2] == '阵雨':
                                img = 'image/weather/zhenyu.png'
                                self.weather.config(fg='yellow')
                            elif t[2] == '雷阵雨':
                                img = 'image/weather/leizhenyu.png'
                                self.weather.config(fg='yellow')
                            elif t[2] == '阴':
                                img = 'image/weather/yintian.png'
                                self.weather.config(fg='yellow')
                            elif t[2] == '小雨':
                                img = 'image/weather/xiaoyu.png'
                                self.weather.config(fg='#00FFFF')
                            else:
                                img = 'image/weather/chushihua.png'
                                self.weather.config(fg='yellow')
                            openimage = PhotoImage(file=img)
                            self.weathertext.set(data)
                            self.weather.config(image=openimage)

            except Exception :
                try:
                    data = '获取天气失败请稍等'
                    self.weathertext.set(data)
                except:
                    pass

    #更换城市
    def cityupdate(self):
        self.city = self.weatherEntry.get()
        self.weatherEntry.delete(0, 'end')

    #私聊用户信息接收
        # 当双击用户里列表内的用户是显示该用户信息
    def Topshowuerinfo(self, data):
        # 这里的消息包含了age,sex,likes,ctiy,phonename,meiting
        t = data.rstrip(':').split(':')
        # 创建TOP组件
        top1 = Toplevel()
        top1.geometry('500x318')
        s = '年龄:    ' + t[0] + '\n' + '性别:    ' + t[1] + '\n' + '爱好:    ' + t[2] + '\n' + '城市:    ' + t[3] + '\n' \
            + '手机号码:  ' + t[4] + '\n' + '注册时间: ' + t[5]
        t1 = Label(top1, text=s, font='Arial', image=self.im, compound='center', justify='left')
        t1.place(x=0, y=0, width=500)
        Button(top1, text='退出',cursor='hand2', command=top1.destroy).place(x=300, y=225)

    #获取用户信息发送
    def get__userallinfo(self,event):
        username = self.uesrinfo.get(self.uesrinfo.curselection())
        s = '*私聊获取用户信息:' + username
        # 发送服务器格式
        self.sockfd.sendto(s.encode(), self.serveraddr)

    #接受文件线程
    def recvfileThread(self,data):
        recvfile=Thread(target=self.recvfile,args=(data,))
        recvfile.start()

    #接受文件功能
    def recvfile(self,data):
        #data内容是字符串形式的对方IP&端口
        #套接字创建
        self.recvconn=socket.socket()

        #套接字链接
        self.recvconn.connect((data.split('&')[0],int(data.split('&')[1])))
        #初期准备完毕
        # print('已链接上服务器tcp协议')
        #接受文件名字
        name=self.recvconn.recv(4096).decode()
        filename=name.split('&')[0]
        filesize=int(name.split('&')[1])
        # print('调试用给接受者发送文件总长度',filesize)
        s = self.showtime()
        da= '已链接进入tcp文件发送服务器,文件名字是:'+filename
        self.showinfo.config(state=NORMAL)
        self.showinfo.insert('end', s,'yred')
        self.showinfo.insert('end',da)
        self.showinfo.see('end')
        self.showinfo.config(state=DISABLED)
        #链接后创建图形接受文件图形界面初始化传入filename和套接字
        filerecv=Wenjianjieshou(filename,filesize,self.recvconn,self.othername)
        filerecv.main()
        print('客户端打开文件准备接受就绪')

    #发送文件功能
    def sendtofile(self,addr1):
        self.tcpsockfd = socket.socket()
        self.tcpsockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpsockfd.bind((self.serveraddr[0], addr1))
        self.tcpsockfd.listen(5)
        otherconn, addr = self.tcpsockfd.accept()
        # 用户链接进来了
        print('tcp发送文件套接字用户链接进来了', addr)
        s = self.showtime()
        da1 = '客户端:' +str(addr)+'：已链接进入tcp文件发送服务器,请选择发送文件'
        self.showinfo.config(state=NORMAL)
        self.showinfo.insert('end', s,'yred')
        self.showinfo.insert('end',da1)
        self.showinfo.see('end')
        self.showinfo.config(state=DISABLED)
        #l链接后创建图形发送文件图形界面
        a = Wenjian(otherconn,self.othername)
        a.main()



    #发送文件的线程
    def sendtofileThread(self):
        fileaddr = random.randint(50000, 60000)
        #发送文件给+端口+目标用户+加自己的名字
        s='*发送文件给:'+str(fileaddr)+':'+self.othername
        self.sockfd.sendto(s.encode(),self.serveraddr)
        #创建进程
        sendfile=Thread(target=self.sendtofile,args=(fileaddr,))
        # print('创建进程')
        sendfile.start()

    # 当点击退出按钮给正在私聊的人发送消息该用户退出了
    def destroy(self):
        s = '*发送给:'+self.othername+':'+'服务器消息'+':'+ '用户 ' + self.myname + ' 关闭了私聊'
        self.sockfd.sendto(s.encode(),self.serveraddr)
        self.root.destroy()

    #主界面搭建
    def main(self):
        self.root = Toplevel()
        self.root.geometry('530x520')
        self.root.title('与 '+self.othername+' 的私聊！')
        self.im = PhotoImage(file='image/userinfo.png')
        self.chushi = PhotoImage(file='image/weather/chushihua.png')

        #菜单相关函数
        menubar = Menu(self.root)
        menubar.add_command(label='发送文件', command=self.sendtofileThread)
        # 菜单实例应用到大窗口中
        self.root['menu'] = menubar

        #title待定模式暂定为谁和谁的私聊模式
        showinfos = LabelFrame(self.root,text='聊天信息')
        showinfos.place(x=5,y=5)
        huakuai1 = Scrollbar(showinfos)
        self.showinfo = Text(showinfos,width=37,relief=FLAT,height=18,yscrollcommand = huakuai1.set)
        huakuai1.config(command=self.showinfo.yview)
        huakuai1.pack(side=RIGHT,fill=Y)
        self.showinfo.pack(side=LEFT,fill =BOTH)
        self.showinfo.tag_config('yred',foreground='red')
        self.showinfo.config(state=DISABLED)

        #机器人消息
        aiinfos = LabelFrame(self.root,text='机器人信息')
        aiinfos.place(x=5,y=265)
        hukuai2 = Scrollbar(aiinfos)
        self.aiinfo = Text(aiinfos,width=37,height=10,relief=FLAT,yscrollcommand=hukuai2.set)
        hukuai2.config(command =self.aiinfo.yview)
        hukuai2.pack(side=RIGHT,fill=Y)
        self.aiinfo.pack(side=LEFT,fill=BOTH)
        self.aiinfo.tag_config('yred',foreground='red')
        self.aiinfo.config(state=DISABLED)

        #输入框
        inputinfos = LabelFrame(self.root,text='输入信息')
        inputinfos.place(x=5,y=420)
        self.inputinfo = Text(inputinfos,relief=FLAT,width=40,height=4)
        self.inputinfo.pack()

        #天气显示框
        weatherinfos = LabelFrame(self.root, text='天气信息')
        weatherinfos.place(x=300, y=5)
        self.weathertext = StringVar()
        tkFont = tkfont.Font(family='Arial', size=14, weight=tkfont.BOLD)
        self.weather = Label(weatherinfos, fg='yellow', font=tkFont, textvariable=self.weathertext, compound='center')
        self.weather.pack()
        self.weathertext.set('获取天气中请稍等')
        self.weather.config(image=self.chushi)

        #天气输入框
        w1=LabelFrame(self.root,text='请输入天气',width=220,height=60)
        w1.place(x=300,y=295)
        self.weatherEntry = Entry(w1)
        b4 = Button(w1,text='天气发送',cursor='hand2',command=self.cityupdate)
        b4.place(x=148,y=0)
        self.weatherEntry.place(x=5,y=0)

        #用户显示狂
        userinfos = LabelFrame(self.root, text='用户信息')
        userinfos.place(x=300, y=360)
        huakuai4= Scrollbar(userinfos)
        self.uesrinfo = Listbox(userinfos, width=28, height=2,yscrollcommand=huakuai4.set)
        huakuai4.pack(side=RIGHT,fill=Y)
        self.uesrinfo.pack(side=LEFT,fill=BOTH)
        self.uesrinfo.insert(0,self.myname)
        self.uesrinfo.insert(0,self.othername)
        self.uesrinfo.bind('<Double-Button-1>', self.get__userallinfo)

        #按钮界面
        anniuinfos = Frame(self.root)
        anniuinfos.place(x=300, y=450)
        b1 = Button(anniuinfos,text='发送',command = self.sendtouserinfo)
        b1.grid(row=0,column=0,padx =10)
        b2 = Button(anniuinfos,text='机器人消息',cursor='hand2',command = self.sendtoaiinfo)
        b2.grid(row=0,column=1,padx =10)
        b3 = Button(anniuinfos,text='退出',cursor='hand2',command = self.destroy)
        b3.grid(row=0,column=2,padx =10)
        t1 = Thread(target=self.weathersendto)
        t1.start()






if __name__ == '__main__':
    s = Pribymoshi(2,1,'2',2)
    s.main()