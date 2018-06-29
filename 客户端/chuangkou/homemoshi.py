from tkinter import *
# from PIL import Image,ImageTk
from threading import Thread
import tkinter.messagebox as messagebox
import time,sys
from .weather import getAllWeather
# from PIL import ImageTk,Image
from .pribymoshi import Pribymoshi
import tkinter.font as tkfont

class HomeChat:
    def __init__(self,name,conn,addr):
        #初始化用户昵称
        self.username = name
        self.connsockfd = conn
        self.serverddr = addr
        self.city = '天津'
    #时间信息
    def showtime(self):
        s = time.strftime('%Y-%m-%d %H:%M:%S')
        return s+'\n'

    #接口用于控制主循环
    def getretu(self):
        return self.retu

    def recvinfo(self):
        while True:
            # print('多线程启动了')
            da,addr = self.connsockfd.recvfrom(4096)
            data = da.decode()
            print(self.username,'接受到服务端的消息',data)
            # print('房间界面服务器返的数据',data)
            if data[:8] == '*获取房间列表:':
                t = data[8:-1]
                # print('获取房间列表里t的值',t)
                homel = t.split(':')
                #生成字典名字加+密码
                self.homenamepwd={}
                for t1 in homel:
                    x=t1.split('@')
                    # print('x',x)
                    self.homenamepwd[x[0]]=x[1]
                self.listbox_home()
            elif data[:10] == '*获取房间用户信息:':
                userl = data[10:].rstrip(':')
                # print('返回到客户端的房间用户列表',userl)
                #user1的第一个值是密码，

                #房间用户生成里列表
                self.fangjianusername =userl.split(':')
                self.homeuser()
            #如果是机器人消息
            elif data[:7] == '*机器人消息:':
                # 获取时间格式信息
                s = self.showtime()
                self.recvinfofromai.config(state=NORMAL)
                self.recvinfofromai.insert('end', s,'yred')
                self.recvinfofromai.insert('end',data)
                self.recvinfofromai.see('end')
                self.recvinfofromai.config(state=DISABLED)
            elif data[:9] == '*私聊机器人消息:':
                self.siliaomoshi.aiinfos(data[9:])
            elif data[-11:] =='被管理员踢出了该房间\n':
                t = data.split(',')
                if t[1][0] == '你':
                    # print('自己被踢出了',data)
                    self.listuser.delete(0, 'end')
                    self.yonghuxuanzedefangjian.set(' ')
                else:
                    self.againhomeuser()
                s = self.showtime()
                self.infotext.config(state=NORMAL)
                self.infotext.insert('end', s,'yred')
                self.infotext.insert('end',data)
                self.infotext.see('end')
                self.infotext.config(state=DISABLED)

            elif data[:8] == '*获取用户信息:':
                self.Topshowusrinfo(data[8:])
            elif data[:10] == '*私聊获取用户信息:':
                self.siliaomoshi.Topshowuerinfo(data[10:])
            #私聊发送文件模式
            elif data[:8] == '*准备接受文件:':
                self.siliaomoshi.recvfileThread(data[8:])
            elif data[:3] == '<用户':
                    x =data.index(' 退出了')
                    username = data[4:x]
                    # print('退出的用户是',username)
                    #这样可以切除名字在用户列表内将该用户删除
                    self.removeuserlist(data,username)
                    #如果收到了与建立私聊的消息
            elif data[:3] == '*与:':
                t = data[3:].split(':')
                othername = t[0]
                self.new_pribymoshi(othername)

            #如果是私聊消息的话
            elif data[:8] == '*私聊消息来自:':
                #用生成的实例化对象调用接口函数插入到信息框
                self.siliaomoshi.newinfo(data[8:])
            elif data[:7] == '*管理员消息:':
                s = self.showtime()
                self.infotext.config(state=NORMAL)
                self.infotext.insert('end', s,'yred')
                self.infotext.insert('end',data[1:])
                self.infotext.see('end')
                self.infotext.config(state=DISABLED)
                #有可能是建立房间的消息所以，每接受一次管理员消息获取以下所有房间列表
                self.get_homelist()
                #私聊界面显示如果自己没有私聊就会报错所以用ＴＲＹ接收以下
                try:
                    self.siliaomoshi.newinfo(data[1:])
                except :
                    pass
            elif data[:6] ==  '*创建房间:':
                self.serversendcreatehome(data)
            else:
                #聊天消息的话显示在聊天界面
                s = self.showtime()
                da = data.split('&')
                self.infotext.config(state=NORMAL)
                self.infotext.insert('end', s,'yred')
                self.infotext.insert('end',da[0])
                self.infotext.see('end')
                self.infotext.config(state=DISABLED)

    #当双击用户里列表内的用户是显示该用户信息
    def Topshowusrinfo(self,data):
        #这里的消息包含了age,sex,likes,ctiy,phonename,meiting
        t = data.rstrip(':').split(':')
        #创建TOP组件

        top1 = Toplevel(self.root)
        top1.geometry('500x318' )
        s = '年龄:    '+t[0]+'\n'+ '性别:    '+t[1]+'\n'+'爱好:    '+t[2]+'\n'+'城市:    '+t[3]+'\n'\
            +'手机号码:  '+t[4]+'\n'+'注册时间: '+t[5]
        t1=Label(top1,text=s,font='Arial',image=self.im,compound='center',justify='left')
        t1.place(x=0,y=0,width=500)
        Button(top1,text='退出',cursor='hand2',command=top1.destroy).place(x=300,y=225)





    #从列表内删除该用户该
    def removeuserlist(self,data,username):
        self.listuser.delete(0, 'end')
        # print('用户退出了现在的房间列表时',self.fangjianusername)
        for item in self.fangjianusername:
            if item != username:
               self.listuser.insert(0, str(item))
            # 生成时间
        s = self.showtime()
        self.infotext.config(state=NORMAL)
        self.infotext.insert('end', s,'yred')
        self.infotext.insert('end',data)
        self.infotext.see('end')
        self.infotext.config(state=DISABLED)



    #当用户被踢出后再次获取房间用户
    def againhomeuser(self):
        self.yonghuxuanzedefangjian.set('当前所在的房间\n' + self.xuanzedefangjian)
        # print('用户选择了', self.xuanzedefangjian, '房间',self.username)
        s = '*获取房间用户信息:' + self.xuanzedefangjian+":"+self.username
        self.connsockfd.sendto(s.encode(), self.serverddr)

    #如果用户退出了,提示服务器删除数据库信息
    def userquit(self):
        data = '*用户退出了:'+self.username
        self.connsockfd.sendto(data.encode(),self.serverddr)
        self.root.destroy()
        self.retu=0


    def userquit1(self):
        data = '*用户退出了:' + self.username
        self.connsockfd.sendto(data.encode(), self.serverddr)
        self.root.destroy()
        self.retu = 1

    #获取房间列表
    def get_homelist(self):
        s = '*获取房间列表:'
        self.connsockfd.sendto(s.encode(),self.serverddr)



    # 房间列表组件函数
    def listbox_home(self):
        self.lstb.delete(0,'end')
        for item in self.homenamepwd:
            if self.homenamepwd[item] != '*':
                item += ' | 有密码的房间'
            self.lstb.insert(0, str(item))

    #用来验证房间密码的功能
    def yanzheng11(self):
        # print('验证密码了','pwd1', 'self.homenamepwd[self.xuanzedefangjian]', self.homenamepwd[self.xuanzedefangjian])
        pwd1 = self.getpwd.get()
        if self.homenamepwd[self.xuanzedefangjian] == pwd1:
            #关闭验证界面
            self.hpwd.destroy()
            #显示当前所在房间
            self.yonghuxuanzedefangjian.set('当前所在的房间\n' + self.xuanzedefangjian)
            s = '*获取房间用户信息:' + self.xuanzedefangjian + ":" + self.username
            # 发送给服务器
            self.connsockfd.sendto(s.encode(), self.serverddr)
            #删除以前的聊天信息
            self.infotext.config(state=NORMAL)
            self.infotext.delete(0.0, 'end')
            self.infotext.config(state=DISABLED)

        else:
            messagebox.showerror(title='关于密码', message='密码输入错误了')


    #房间密码验证
    def homepwdyanzheng(self):
        # def destory1():
        #     self.hpwd.destroy()
        self.hpwd=Toplevel()
        self.hpwd.geometry('350x300')
        self.hpwd.title('有密码的房间')
        phon = Label(self.hpwd,image=self.yanzheng)
        phon.place(x=0,y=0)
        Label(self.hpwd,text='你想要进入有密码的房间请输入密码',font='Arita',fg='red').place(x=65,y=85)
        self.getpwd=Entry(self.hpwd)
        self.getpwd.place(x=100,y=120)
        Button(self.hpwd,text='确定',cursor='hand2',command=self.yanzheng11).place(x=200,y=240)
        Button(self.hpwd,text='退出',cursor='hand2',command=self.hpwd.destroy).place(x=250,y=240)


    #获取用户选择的房间并且获取房间用户信息并删除以前的聊天信息
    def gethomeuser(self,event):
        self.xuanzedefangjian = self.lstb.get(self.lstb.curselection())
        if self.xuanzedefangjian[-9:] == ' | 有密码的房间':
            self.xuanzedefangjian = self.xuanzedefangjian[:-9]
        password = self.homenamepwd[self.xuanzedefangjian]
        print('选择了有密码的房间,',type(password),type(self.xuanzedefangjian))
        if password != '*':
            self.homepwdyanzheng()
        else:
            self.yonghuxuanzedefangjian.set('当前所在的房间\n'+self.xuanzedefangjian)
            s = '*获取房间用户信息:'+self.xuanzedefangjian+":"+self.username
            # print('用户选择了', self.xuanzedefangjian, '房间')
            # 发送给服务器
            self.connsockfd.sendto(s.encode(),self.serverddr)
            #删除以前房间的聊天信息
            self.infotext.config(state=NORMAL)
            self.infotext.delete(0.0, 'end')
            self.infotext.config(state=DISABLED)

    #房间用户列表双击获取用户信息
    def get_home_userallinfo(self,event):
        username = self.listuser.get(self.listuser.curselection())
        s = '*获取用户信息:'+username
        #发送服务器格式
        self.connsockfd.sendto(s.encode(),self.serverddr)


    #房间用户列表组件函数
    def homeuser(self):
        self.listuser.delete(0, 'end')
        for item in self.fangjianusername:
            self.listuser.insert(0,str(item))
        # listuser.delete(0,END)





    #聊天天信息显示框
    def show_infos(self):
        da = self.username +':'+self.inputinfo.get('0.0','end')
        self.connsockfd.sendto(da.encode(),self.serverddr)
        data = '我说:'+self.inputinfo.get('0.0','end')
        s = self.showtime()
        self.infotext.config(state=NORMAL)
        self.infotext.insert('end', s,'yred')
        self.infotext.insert('end',data)
        self.infotext.see('end')
        self.infotext.config(state=DISABLED)
        self.inputinfo.delete(0.0,'end')



    #输入框设置
    def input_info(self,center3):
        self.inputinfo = Text(center3,width = 54,relief=FLAT,height=4)
        self.inputinfo.pack()

    #发送机器人消息
    def sendtoAIinfo(self):
        #从输入框获取用户输入信息
        da = self.inputinfo.get(0.0,'end')
        data = '*机器人消息:'+da
        self.connsockfd.sendto(data.encode(),self.serverddr)
        #获取时间格式信息
        s = self.showtime()
        self.recvinfofromai.config(state=NORMAL)
        self.recvinfofromai.insert('end',s,'yred')
        self.recvinfofromai.insert('end','我说:'+da)
        self.recvinfofromai.see('end')
        self.recvinfofromai.config(state=DISABLED)
        #清空输入框
        self.inputinfo.delete(0.0, 'end')


    #显示天气函数
    def weathershow(self):
        while True:
            city = self.city
            try:
                cityweather = getAllWeather(self.city)
                if not cityweather:
                    data = '输入城市不正确\n现在的城市是:'+city
                    img = 'image/weather/chushihua.png'
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
                            elif t[2] == '雷阵雨':
                                img = 'image/weather/leizhenyu.png'
                                self.weather.config(fg='yellow')
                            elif t[2] == '阵雨':
                                img = 'image/weather/zhenyu.png'
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
            except Exception as e:
                # print('获取天气失败的内容是',e)
                try:
                    data = '获取天气失败请稍等'
                    self.weathertext.set(data)
                except:
                    pass



    #更新城市默认值
    def cityupdate(self):
        self.city = self.cityinput.get()
        self.cityinput.delete(0, 'end')
    #被动建立聊天模式函数启动
    def beidongs(self,othername):
        self.siliaomoshi = Pribymoshi(self.connsockfd, self.username, othername, self.serverddr)
        self.siliaomoshi.main()

    #被动建立私聊模式线程
    def new_pribymoshi(self,othername):
        beidongsiliao=Thread(target=self.beidongs,args=(othername,))
        beidongsiliao.start()


    #主动建立私聊
    def siliao(self):
        othername = self.listuser.get(self.listuser.curselection()[0])
        msg = '*我要与:' + othername + ':' + self.username + ':建立私聊模式'
        if othername == self.username:
            messagebox.showerror(title='有错误！',message='不能与自己建立私聊!')
        else:
            self.connsockfd.sendto(msg.encode(), self.serverddr)
            self.siliaomoshi = Pribymoshi(self.connsockfd, self.username, othername, self.serverddr)
            self.siliaomoshi.main()

    #建立私聊模式
    def getlistuser(self):
        #启动线程建立新的私聊模式
        siliao=Thread(target=self.siliao)
        siliao.start()

    #对付服务器返回创建房间的返回结果进行处理
    def serversendcreatehome(self,da):
        if  not self.createhomepassword:
            if da == '*创建房间:创建失败':
                data = '创建失败房间已存在!\n请查看现在房间有哪些再创建！'
                # 更新界面的提醒label
                self.createvar.set(data)
            else:
                data = '创建成功\n房间名字:%s\n房间密码是:默认值(*)\n3秒后结束该界面\n也可手动点击退出按钮'\
                       % self.createhomename
                # 更新界面的提醒label
                self.createvar.set(data)
                # 从新获取一次房间列表
                self.get_homelist()
                time.sleep(3)
                self.cteateh.destroy()

        else:
            if da == '*创建房间:创建失败':
                data = '创建失败房间已存在!\n请查看现在房间有哪些再创建！'
                # 更新界面的提醒label
                self.createvar.set(data)
            else:
                data = '创建成功\n房间名字:%s\n房间密码是:%s\n3秒后结束该界面\n也可手动点击退出按钮'\
                       % (self.createhomename, self.createhomepassword)
                # 更新界面的提醒label
                self.createvar.set(data)
                #从新获取一次房间列表
                self.get_homelist()
                time.sleep(3)
                self.cteateh.destroy()

    #发送创建房间数据数据
    def homecreate(self):
        self.createhomename = self.homename.get()
        self.createhomepassword = self.homepassword.get()

        if not self.createhomename:
            da = '房间名字没有输入啊!'
            self.createvar.set(da)
        elif not self.createhomepassword:
            da = '*创建房间:'+self.username+':'+self.createhomename
            self.connsockfd.sendto(da.encode(),self.serverddr)
        else:
            da = '*创建房间:' + self.username + ':' + self.createhomename+":"+self.createhomepassword
            # print('创建房间发送内容', da)
            self.connsockfd.sendto(da.encode(), self.serverddr)



    #创建房间相关
    def createhome(self):
        self.cteateh = Toplevel()
        self.cteateh.geometry('400x300')
        Label(self.cteateh,image=self.creHomeimg).place(x=0,y=0)
        Label(self.cteateh, text=' 房间名',bg='#FFFFFF').place(x=100, y=100)
        Label(self.cteateh, text='房间密码',bg='#FFFFFF').place(x=100, y=130)
        self.homename = Entry(self.cteateh)
        self.homename.place(x=170, y=100)
        self.homepassword = Entry(self.cteateh)
        self.homepassword.place(x=170, y=130)
        self.createvar = StringVar()
        Label(self.cteateh, textvariable=self.createvar, font='Arica', fg='red',bg='#FFFFFF').place(x=120, y=155)
        Button(self.cteateh, text='确定',cursor='hand2', command=self.homecreate).place(x=100, y=260)
        Button(self.cteateh, text='取消',cursor='hand2', command=self.cteateh.destroy).place(x=200, y=260)

    #主模块开启循环
    def root_main(self):
        self.root = Tk()
        self.im = PhotoImage(file='image/userinfo.png')
        self.fangjian = PhotoImage(file='image/fangjian.png')
        chushihua=PhotoImage(file='image/weather/chushihua.png')
        self.yanzheng = PhotoImage(file='image/fagnjianyanzheng.png')
        self.creHomeimg=PhotoImage(file='image/createhome.png')
        self.root.title('欢迎用户:<'+self.username+'>你好')

        # 菜单相关
        menubar = Menu(self.root)
        menubar.add_command(label='重新选择聊天方式',command=self.userquit1)
        menubar.add_command(label='创建房间',command=self.createhome)
        # 菜单实例应用到大窗口中
        self.root['menu'] = menubar

        #房间显示窗口
        left1 = LabelFrame(self.root,text='房间列表',width = 100,height=500)
        left1.grid(row=0,column=0,rowspan = 5,padx=5)
        self.yonghuxuanzedefangjian = StringVar()
        tkFont1 = tkfont.Font(family='Arial', size=12, weight=tkfont.BOLD)
        t1 =Label(left1,textvariable=self.yonghuxuanzedefangjian,font=tkFont1,image=self.fangjian, \
                     fg='Green',compound='center',width=140,height=100)
        t1.pack(side='top')

        # 滑块组件
        listhuakuai = Scrollbar(left1)
        listhuakuai.pack(side=RIGHT, fill=Y)
        xhuakuai = Scrollbar(left1,orient=HORIZONTAL)
        xhuakuai.pack(side=BOTTOM, fill=X)
        # 房间列表组件
        self.lstb = Listbox(left1, width=18, height=21, yscrollcommand=listhuakuai.set,xscrollcommand=xhuakuai.set)
        self.lstb.pack(side=LEFT,fill=BOTH)
        listhuakuai.config(command=self.lstb.yview)
        xhuakuai.config(command=self.lstb.xview)
        # 绑定获取房间信息列表进入该房间在
        self.lstb.bind('<Double-Button-1>', self.gethomeuser)

        #聊天窗口
        center1 = LabelFrame(self.root,text='聊天信息',width=400,height =100)
        center1.grid(row = 0,column=1,rowspan=3)

        #信息显示信息
        infoscr = Scrollbar(center1)
        self.infotext = Text(center1,width=52,height=25,relief=FLAT,yscrollcommand = infoscr.set)
        infoscr.grid(row=0,column=1,sticky='ns')
        self.infotext.grid(row=0,column=0)
        infoscr.config(command=self.infotext.yview)
        self.infotext.tag_config('yred', foreground='red')
        self.infotext.config(state=DISABLED)

        #机器人窗口
        center2 = LabelFrame(self.root,text='机器人消息',width=400,height=80)
        center2.grid(row=3,column=1)
        aisc = Scrollbar(center2)
        self.recvinfofromai = Text(center2,width=52,height=5,relief=FLAT,yscrollcommand=aisc.set)
        aisc.grid(row=0, column=1, sticky='ns')
        self.recvinfofromai.grid(row=0, column=0)
        aisc.config(command=self.recvinfofromai.yview)
        self.recvinfofromai.tag_config('yred',foreground='red')
        self.recvinfofromai.config(state=DISABLED)

        #输入框
        center3 = LabelFrame(self.root,text='聊天信息输入框',width=400,height=60)
        center3.grid(row=4,column=1)

        #输入框设置
        self.input_info(center3)
        right1 = LabelFrame(self.root,text='天气显示框',width=100,height=350)
        right1.grid(row=0,column=2,columnspan=3,pady=5,padx=5)
        self.weathertext=StringVar()
        tkFont=tkfont.Font(family='Arial',size=14,weight=tkfont.BOLD)
        self.weather = Label(right1,fg='yellow',font=tkFont,textvariable=self.weathertext,compound='center')
        self.weather.pack()
        self.weathertext.set('获取天气中请稍等')
        self.weather.config(image=chushihua)


        #城市输入框
        w1 = LabelFrame(self.root, text='请输入天气', width=219, height=60)
        w1.grid(row=1,column=2,padx=5)
        self.cityinput = Entry(w1)
        b4 = Button(w1, text='天气发送', cursor='hand2', command=self.cityupdate)
        b4.place(x=148, y=0)
        self.cityinput.place(x=5, y=5)

        #房间用户信息框
        right4 = LabelFrame(self.root,text='房间内用户信息',width=200,height=100)
        right4.grid(row=3,column=2,columnspan=3,pady=5)
        huauser = Scrollbar(right4)
        # 列表组件
        self.listuser = Listbox(right4, width=26, height=3, yscrollcommand=huauser.set)
        self.listuser.grid(row=0, column=0)
        huauser.grid(row=0, column=1, sticky='ns')
        huauser.config(command=self.listuser.yview)
        self.listuser.bind('<Double-Button-1>',self.get_home_userallinfo)
        #
        #发送确定退出模块
        #发送按钮

        right5 = Frame(self.root,width=200,height=40)
        right5.grid(row=4,column=2,columnspan=2,pady=5)

        t1 = Button(right5,text='发送',command = self.show_infos)
        t1.grid(row=0,column=1,padx = 10)
        t2 = Button(right5, text='机器人消息',cursor='hand2', command=self.sendtoAIinfo)
        t2.grid(row=0, column=2,padx = 10)
        t3 = Button(right5, text='私聊', cursor='hand2',command=self.getlistuser)
        # t4 = Button(right5,text='重新选择聊天方式',command=self.userquit1)
        # t4.grid(row=1,column=2,pady=5)
        t3.grid(row=0, column=3,padx = 10)
        s = '*获取房间列表:'
        self.connsockfd.sendto(s.encode(), self.serverddr)
        t1 = Thread(target=self.recvinfo)
        t1.start()
        t2 = Thread(target=self.weathershow)
        t2.start()

        self.root.protocol('WM_DELETE_WINDOW',self.userquit)
        self.root.mainloop()




if __name__ == '__main__':
    home = HomeChat()
    home.root_main()
