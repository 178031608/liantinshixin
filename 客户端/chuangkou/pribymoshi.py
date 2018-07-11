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
        self.img10 = PhotoImage(file='image/info.png')
        self.infotuichu = PhotoImage(file='image/infotuichu.png')

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
        # # 创建TOP组件
        # top1 = Toplevel()
        # top1.geometry('500x318')
        # s = '年龄:    ' + t[0] + '\n' + '性别:    ' + t[1] + '\n' + '爱好:    ' + t[2] + '\n' + '城市:    ' + t[3] + '\n' \
        #     + '手机号码:  ' + t[4] + '\n' + '注册时间: ' + t[5]
        # t1 = Label(top1, text=s, font='Arial', image=self.im, compound='center', justify='left')
        # t1.place(x=0, y=0, width=500)
        # Button(top1, text='退出',cursor='hand2', command=top1.destroy).place(x=300, y=225)

        top1 = Toplevel()
        top1.geometry('1004x692')
        top1.iconbitmap('image/tubiao.ico')
        Label(top1, image=self.img10).place(x=0, y=0)
        agestr = StringVar()
        Label(top1, textvariable=agestr, font=('Asria', '18'), bd=0, bg='#F9F5F5', ).place(x=540, y=145)
        sexstr = StringVar()
        Label(top1, textvariable=sexstr, bd=0, font=('Asria', '18'), bg='#F9F5F5', ).place(x=540, y=210)
        likestr = StringVar()
        Label(top1, textvariable=likestr, font=('Asria', '18'), bd=0, bg='#F9F5F5', ).place(x=540, y=280)
        citystr = StringVar()
        Label(top1, textvariable=citystr, font=('Asria', '18'), bd=0, bg='#F9F5F5', ).place(x=540, y=345)
        phonestr = StringVar()
        Label(top1, textvariable=phonestr, font=('Asria', '10'), bd=0, bg='#F9F5F5', ).place(x=610, y=420)
        timestr = StringVar()
        Label(top1, textvariable=timestr, font=('Asria', '10'), bd=0, bg='#F9F5F5', ).place(x=610, y=480)
        agestr.set(t[0])
        sexstr.set(t[1])
        likestr.set(t[2])
        citystr.set(t[3])
        phonestr.set(t[4])
        timestr.set(t[5][:11])

        s = '年龄:    ' + t[0] + '\n' + '性别:    ' + t[1] + '\n' + '爱好:    ' + t[2] + '\n' + '城市:    ' + t[3] + '\n' \
            + '手机号码:  ' + t[4] + '\n' + '注册时间: ' + t[5]
        # t1=Label(top1,text=s,font='Arial',image=self.im,compound='center',justify='left')
        # t1.place(x=0,y=0,width=500)
        Button(top1, image=self.infotuichu,
               width=170,
               height=60,
               bd=0,
               relief=FLAT,
               cursor='hand2', command=top1.destroy).place(x=502, y=535)

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
        self.root = Toplevel(bg='#ccc'
                             )
        self.root.geometry('770x738')
        self.root.title('与 '+self.othername+' 的私聊！')
        self.im = PhotoImage(file='image/userinfo.png')
        self.chushi = PhotoImage(file='image/weather/chushihua.png')
        self.root.iconbitmap('image/tubiao.ico')

        l1 = Label(self.root,width=150,height=3,bg='#313131')
        l1.place(x=0,y=0)
        l2 = Label(self.root,font=('Adobe 黑体 Std', '18'),
                   text='聊天信息',bg='#ccc')
        l2.place(x=10,y=60)

        b1 =Button(self.root,
               text='发送文件',
               font=('Adobe 黑体 Std', '14'),
                fg='white',
               bg='#313131',
               bd=0,
               relief=FLAT,
               cursor='hand2',
               command=self.sendtofileThread)
        b1.place(x=20, y=10)
        #菜单相关函数
        # menubar = Menu(self.root)
        # menubar.add_command(label='发送文件', command=self.sendtofileThread)
        # # 菜单实例应用到大窗口中
        # self.root['menu'] = menubar

        #title待定模式暂定为谁和谁的私聊模式
        showinfos = Frame(self.root,bg='#ccc')
        showinfos.place(x=0,y=90)
        huakuai1 = Scrollbar(showinfos,relief=FLAT,width=5)
        self.showinfo = Text(showinfos,width=54,relief=FLAT,height=23,yscrollcommand = huakuai1.set)
        huakuai1.config(command=self.showinfo.yview)
        huakuai1.pack(side=RIGHT,fill=Y)
        self.showinfo.pack(side=LEFT,fill =BOTH)
        self.showinfo.tag_config('yred',foreground='red')
        self.showinfo.config(state=DISABLED)

        #机器人消息
        l3 = Label(self.root, font=('Adobe 黑体 Std', '20'), text='机器人信息',
                    bg='#ccc')
        l3.place(x=10, y=400)
        aiinfos = Frame(self.root,bg='#ccc')
        aiinfos.place(x=0,y=430)
        hukuai2 = Scrollbar(aiinfos,relief=FLAT,width=5)
        self.aiinfo = Text(aiinfos,width=54,height=11,relief=FLAT,yscrollcommand=hukuai2.set)
        hukuai2.config(command =self.aiinfo.yview)
        hukuai2.pack(side=RIGHT,fill=Y)
        self.aiinfo.pack(side=LEFT,fill=BOTH)
        self.aiinfo.tag_config('yred',foreground='red')
        self.aiinfo.config(state=DISABLED)

        #输入框

        l3 = Label(self.root, font=('Adobe 黑体 Std', '20'), text='输入信息',
                   bg='#ccc')
        l3.place(x=10, y=580)
        inputinfos = Frame(self.root,bg='#ccc')
        inputinfos.place(x=0,y=615)
        self.inputinfo = Text(inputinfos,relief=FLAT,width=54,height=8)
        self.inputinfo.pack()

        #天气显示框
        l4 = Label(self.root, font=('Adobe 黑体 Std', '20'), text='天气信息',
                   bg='#ccc')
        l4.place(x=440, y=60)
        weatherinfos = Frame(self.root,bg='#ccc')
        weatherinfos.place(x=440, y=90)
        self.weathertext = StringVar()
        tkFont = tkfont.Font(family='Arial', size=14, weight=tkfont.BOLD)
        self.weather = Label(weatherinfos, fg='yellow', font=tkFont,bd=0,relief=FLAT,
                             textvariable=self.weathertext, compound='center')
        self.weather.pack()
        self.weathertext.set('获取天气中请稍等')
        self.weather.config(image=self.chushi)

        #天气输入框
        l4 = Label(self.root, font=('Adobe 黑体 Std', '20'), text='请输入天气',
                   bg='#ccc')
        l4.place(x=440, y=440)
        w1=Frame(self.root,width=270,height=60,bg='#ccc')
        w1.place(x=440,y=480)

        self.weatherEntry = Entry(w1)
        img = PhotoImage(file='image/siliaoweater.png')
        b4 = Button(w1,text='天气发送',
                    font=('Adobe 黑体 Std', '14'),
                    fg='black',
                    bg='#ccc',
                    cursor='hand2',command=self.cityupdate)
        b4.place(x=168,y=0)
        # b4.config(image=img)
        self.weatherEntry.place(x=5,y=5)

        #用户显示狂
        l4 = Label(self.root, font=('Adobe 黑体 Std', '20'), text='用户信息',
                   bg='#ccc')
        l4.place(x=440, y=530)
        userinfos = Frame(self.root,bg='#ccc' )
        userinfos.place(x=450, y=580)

        huakuai4= Scrollbar(userinfos,relief=FLAT,width=5)
        self.uesrinfo = Listbox(userinfos, width=26,
                                font=('Adobe 黑体 Std', '16'),
                                bd=0,
                                relief=FLAT,
                                bg='#f2f2f2',
                                height=2,yscrollcommand=huakuai4.set)
        huakuai4.pack(side=RIGHT,fill=Y)
        self.uesrinfo.pack(side=LEFT,fill=BOTH)
        self.uesrinfo.insert(0,self.myname)
        self.uesrinfo.insert(0,self.othername)
        self.uesrinfo.bind('<Double-Button-1>', self.get__userallinfo)

        #按钮界面
        anniuinfos = Frame(self.root,bg='#ccc')
        anniuinfos.place(x=430, y=670)
        b1 = Button(anniuinfos,text='发送',
                    font=('Adobe 黑体 Std', '14'),
                    fg='black',
                    bg='#ccc',
                    command = self.sendtouserinfo)
        b1.grid(row=0,column=0,padx =10)
        b2 = Button(anniuinfos,text='机器人消息',
                    font=('Adobe 黑体 Std', '14'),
                    fg='black',
                    bg='#ccc',
                    cursor='hand2',command = self.sendtoaiinfo)
        b2.grid(row=0,column=1,padx =10)
        b3 = Button(anniuinfos,text='退出',
                    font=('Adobe 黑体 Std', '14'),
                    fg='black',
                    bg='#ccc',
                    cursor='hand2',command = self.destroy)
        b3.grid(row=0,column=2,padx =10)
        t1 = Thread(target=self.weathersendto)
        t1.start()






if __name__ == '__main__':
    s = Pribymoshi(2,1,'2',2)
    s.main()
