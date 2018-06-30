from tkinter import *
from 数据库.UserinfoMysql import Userinfo
from 数据库.Homemysql import Homeinfo
from AI import ServerAI
import time
import tkinter.messagebox as messagebox


class ServerTkinter:
    def __init__(self,sockfd):
        self.serverai= ServerAI()
        self.serversockfd = sockfd
        self.homemysqlamd = Homeinfo()
        self.userdata=[]


    #显示客户端的各种信息
    def showinfott(self,data):
        s=self.showtime()
        self.showinfo.config(state=NORMAL)
        self.showinfo.insert('end',s,'yred')
        self.showinfo.insert('end',data)
        self.showinfo.see('end')
        self.showinfo.config(state=DISABLED)


    #实现样式设置，全部为黄色的底红色的字体加粗字体有返回值
    def showtime(self):
        s = time.strftime('%Y-%m-%d %H:%M:%S')
        self.showinfo.tag_config('yred',foreground='red')
        self.jqrinfo.tag_config('yred',foreground='red')
        return s+'\n'

    #机器人聊天交互
    def robotsendinfo(self):
        #输入框内容
        data =self.inputinfo.get(0.0,'end')
        self.inputinfo.delete(0.0,'end')
        s = self.showtime()

        self.jqrinfo.config(state=NORMAL)
        self.jqrinfo.insert('end',s,'yred')
        i_speak = '我说:'+data
        self.jqrinfo.insert('end',i_speak)
        #机器人返回值
        info =self.serverai.robot_ai(data)
        s = self.showtime()
        self.jqrinfo.insert('end',s,'yred')
        # print(info)
        fromai = '机器人说:'+info+'\n'
        self.jqrinfo.insert('end',fromai)
        self.jqrinfo.see('end')
        self.jqrinfo.config(state=DISABLED)
        pass

    #发送管理员消息
    def chatsendinfo(self):
        #获取所有在线用户并发送管理员消息
        # 输入框内容
        data = self.inputinfo.get(0.0, 'end')
        self.inputinfo.delete(0.0, 'end')
        s = self.showtime()
        i_speak = '我说:' + data
        #显示在自己的消息界面
        self.showinfo.config(state=NORMAL)
        self.showinfo.insert('end',s,'yred')
        self.showinfo.insert('end',i_speak)
        self.showinfo.see('end')
        self.showinfo.config(state=DISABLED)
        #获取去所有咋在线用户
        alluseraddr=self.homemysqlamd.getalluseradd()
        #alluseraddr形式应该是（（IP&端口,),（IP&端口,),（IP&端口,),)
        for addr in alluseraddr:
            t=addr[0].split('&')
            info='*管理员消息:'+data
            self.serversockfd.sendto(info.encode(),(t[0],int(t[1])))

    #管理员发送创建成房间成功的消息,没发送一次获取所有房间
    def sendcreatehomeinfo(self,homename,createuser='管理员'):
        #有人创建房间就更新信息
        self.getallhome()
        addr = self.homemysqlamd.getalluseradd()
        s = '*管理员消息: '+createuser+' 刚刚创建了新的房间\n房间名字是:'+homename+'\n'
        for addr in addr:
            t = addr[0].split('&')
            self.serversockfd.sendto(s.encode(), (t[0], int(t[1])))
            print('创建房间发送的消息', s)


    #显示在线用户
    def userlist(self,data):
        self.userdata=data
        try:
            self.userlisall.delete(0,'end')
            for i in data:
                self.userlisall.insert(0,str(i))
        except :
            pass

    #显示所有房间的功能
    def getallhome(self):
        #管理员获取的房间信息比较全面
        homeinfo = self.homemysqlamd.getallhome()
        self.homelisall.delete(0, 'end')
        self.allhomeinfo=[]
        for x in homeinfo:
            s = '房间ID:%s\n\n房间名:%s\n\n房间创建者:%s\n\n房间密码:%s\n\n' % (str(x[0]), str(x[1]), str(x[2]), str(x[3]))
            self.allhomeinfo.append(s)
            self.homelisall.insert(0,str(x[1]))

    #双击房间名获取房间建详细信息
    def homexiangxiinfo(self,event):

        homename=self.homelisall.get(self.homelisall.curselection())
        for x in self.allhomeinfo:
            print('到这里了',x)
            name = x.split('\n\n')[1]
            if name == '房间名:'+homename:
                top1 = Toplevel()
                top1.geometry('500x318')
                t1 = Label(top1, text=x, font='Arial', image=self.im, compound='center', justify='left')
                t1.place(x=0, y=0, width=500)
                Button(top1,text='退出',cursor='hand2',command=top1.destroy).place(x=300,y=225)
                break


    #删除房间
    def removehome(self):
        try:
            homename=self.homelisall.get(self.homelisall.curselection())
        except:
            messagebox.showerror(title='关于删除房间',message='出错了，你还没有选择房间啊')
            return
        print('选择的房间是',homename)
        if homename:
            data = self.homemysqlamd.removehome(homename)
            time = self.showtime()
            messagebox.showinfo(title='关于删除房间',message=homename+'\n房间于'+time+'\n'+data)
        #删除房间后也更新信息
        self.getallhome()
        pass

    #双击踢出用户功能
    def outhomeuser(self,event):
        try:
            tichuyonghu = self.userlisall.get(self.userlisall.curselection())
            self.tirengongneng(tichuyonghu)
        except:
            pass

    #一键踢出所有用户调用的函数
    def allusertichu(self):
        for xuanzedeyonghu in self.userdata:
            self.tirengongneng(xuanzedeyonghu)

    #踢人的功能
    def tirengongneng(self,xuanzedeyonghu):
        try:
            #获取房间所有用户并发送消息并把他数据中删除
            data=self.homemysqlamd.severtirenyong(xuanzedeyonghu)
            # (('你好', '127.0.0.1&55292'),)
            # print('踢出用户数据库的返回值', data)
            for z in data:
                t = z[1].split('&')
                if z[0]==xuanzedeyonghu:
                    xiaoxi = '因不文明用语,你被管理员踢出了该房间\n'
                    self.serversockfd.sendto(xiaoxi.encode(),(t[0],int(t[1])))
                else:
                    xiaoxi = xuanzedeyonghu+',因不文明用语,被管理员踢出了该房间\n'
                    self.serversockfd.sendto(xiaoxi.encode(), (t[0], int(t[1])))
            self.homemysqlamd.userquit(xuanzedeyonghu)
        except Exception as e:
            print('踢出错误了',e)

    #用于创建房间的功能
    def mysqlhomecreate(self):
        homename=self.homename.get()
        homepassword=self.homepassword.get()
        if not homename:
            data='房间名字没有输入啊'
        elif not homepassword:
            da=self.homemysqlamd.createhome(homename,'管理员')
            if da =='创建失败':
                data='创建失败房间已存在!\n请查看现在房间有哪些再创建！'
            else:
                data='创建成功\n房间名字:%s\n房间密码是:默认值(*)'%homename
                self.sendcreatehomeinfo(homename)
        else:
            da =self.homemysqlamd.createhome(homename,'管理员',homepassword)
            if da =='创建失败':
                data = '创建失败房间已存在!\n请查看现在房间有哪些再创建！'
            else:
                data = '创建成功\n房间名字:%s\n房间密码是:%s' %(homename,homepassword)
                self.sendcreatehomeinfo(homename)
        #更新界面的提醒label
        self.createvar.set(data)


    #服务器创建房间的界面
    def createhome(self):
        cteateh=Toplevel()
        cteateh.geometry('804x629')
        homezhuce = PhotoImage(file='image/homezhuce.png')
        t2 = Label(cteateh, image=homezhuce)
        t2.place(x=0, y=0)
        # Label(cteateh,text=' 房间名').place(x=5,y=5)
        # Label(cteateh,text='房间密码').place(x=5,y=30)
        self.homename=Entry(cteateh,
                            bd=0,
                            font=('Adobe 黑体 Std', '32'),
                            bg='#5EC6CF',
                            fg='red',
                            width=13, justify=CENTER,
                            relief=FLAT,
                            insertbackground='green',
                            # highlightthickness=4,
                            highlightcolor='pink',
                            )
        self.homename.place(x=330,y=195)
        self.homepassword=Entry(cteateh,
                                bd=0,
                                font=('Adobe 黑体 Std', '32'),
                                bg='#5EC6CF',
                                fg='red',
                                width=13, justify=CENTER,
                                relief=FLAT,
                                insertbackground='green',
                                # highlightthickness=4,
                                highlightcolor='pink',
                                )
        self.homepassword.place(x=330,y=295)
        self.createvar=StringVar()
        Label(cteateh,textvariable=self.createvar, relief=FLAT,
              bd=0,bg='#01859E',font=('Arica','14',),fg='yellow').place(x=40,y=40)
        img1 = PhotoImage(file='image/homezhucequeding.png')
        img2 = PhotoImage(file='image/homezhucequxiao.png')
        Button(cteateh,
               width=120,
               height=60,
               image=img1,
               bd=0,
               relief=FLAT,
               cursor='hand2',
               command=self.mysqlhomecreate).place(x=116,y=518)
        Button(cteateh,
               width=120,
               height=60,
               image=img2,
               bd=0,
               relief=FLAT,
               cursor='hand2',
               command=cteateh.destroy).place(x=312, y=518)
        cteateh.mainloop()

    #主窗口
    def main(self):
        root  = Tk()
        root.title('服务器管理员')
        self.im = PhotoImage(file='image/userinfo.png')
        root.geometry('700x510' )
        # jiemian = PhotoImage(file='image/jiemian.png')

        # Label(root, image=jiemian).place(x=180, y=62)
        # 菜单功能一键提出所有用户用于调试
        menubar=Menu(root,bg='yellow',bd=0,)
        menubar.add_command(label='一键踢出所有用户用于调试',


                            command=self.allusertichu)
        #创建一个字级菜单
        fangjian = Menu(menubar,tearoff=False)
        fangjian.add_command(label='创建房间', command=self.createhome)
        fangjian.add_separator()
        fangjian.add_command(label='删除房间', command=self.removehome)
        menubar.add_cascade(label='房间相关功能',menu=fangjian)
        #加入到主窗口
        root['menu'] = menubar

        #左侧在线用户窗口pass
        left1 = Frame(root,width = 150,height=500)
        left1.place(x=5,y=5)
        Label(left1, text='在线信息表', fg='green').pack()
        userscro = Scrollbar(left1,background='#FFE6FF',relief=FLAT,width=5)
        userscro.pack(side = RIGHT,fill=Y)
        self.userlisall = Listbox(left1,background='#FFE1FF',relief=FLAT,bd=0,
                                  highlightthickness=0,
                                  width = 18,height=25,yscrollcommand = userscro.set)
        self.userlisall.pack(side=LEFT,fill=BOTH)
        userscro.config(command=self.userlisall.yview)
        #双击踢出用户
        self.userlisall.bind('<Double-Button-1>',self.outhomeuser)

        #右侧房间信息表
        right2 = Frame(root, width=150, height=500)
        right2.place(x=470, y=5)
        Label(right2, text='房间信息表', fg='green').pack()
        userscro = Scrollbar(right2 ,background='#FFE4FF',relief=FLAT,width=5)
        userscro.pack(side=RIGHT, fill=Y)
        user = Scrollbar(right2,orient=HORIZONTAL,background='#FFE1FF',relief=FLAT,width=5)
        user.pack(side=BOTTOM, fill=X)
        self.homelisall = Listbox(right2 ,background='#FFE1FF',highlightthickness=0,
                                  relief=FLAT, width=29, bd=0,height=20,
                                  yscrollcommand=userscro.set,xscrollcommand=user.set)
        self.homelisall.pack(side=LEFT, fill=BOTH)
        userscro.config(command=self.homelisall.yview)
        user.config(command=self.homelisall.xview)
        #双击显示所有用户房间详细信息
        self.homelisall.bind('<Double-Button-1>',self.homexiangxiinfo)

        #中间信息窗口
        center1 = Frame(root,width=300,height=100)
        center1.place(x=160,y=5)
        Label(center1, text='各种信息框', fg='green').pack()
        huakuai = Scrollbar(center1,background='#FFE2FF',relief=FLAT,width=5)
        huakuai.pack(side=RIGHT,fill=Y)
        self.showinfo= Text(center1,width=40,bg='#FFE12F',bd=0,
                            height = 21,relief=FLAT,yscrollcommand=huakuai.set)
        self.showinfo.pack(side=LEFT,fill=BOTH)

        huakuai.config(command=self.showinfo.yview)
        self.showinfo.config(state=DISABLED)

        #中间下输入窗口
        center2 = Frame(root,width=300,height=50,relief=FLAT)
        center2.place(x=160,y=421)
        Label(center2,text='输入框',fg='green').pack()
        #初始化输入框
        self.inputinfo = Text(center2,width=42,heigh=4,relief=FLAT)
        self.inputinfo.pack()


        #机器人消息
        right1 = Frame(root,width=150,height=200)
        right1.place(x=160,y=320)
        Label(right1, text='机器人信息框', fg='green').pack()
        jqrhk = Scrollbar(right1,background='#FFE1FF',relief=FLAT,width=5)
        jqrhk.pack(side=RIGHT,fill=Y)
        self.jqrinfo=Text(right1,width=40,height=5,bg='#FFE1F1',relief=FLAT,yscrollcommand=jqrhk.set)
        self.jqrinfo.pack(side=LEFT,fill=BOTH)
        jqrhk.config(command=self.jqrinfo.yview)
        self.jqrinfo.config(state=DISABLED)
        #初始化获取所有房间
        self.getallhome()

        # jiqiren = PhotoImage(file='image/jiqiren.png')

       #输入框
        Button(root,text='发送机器人',
               # background='red',
               # width=125,height=45,
               cursor='hand2',
               # default=NORMAL,
               # font='12',
               # image=jiqiren,
               # bd=0,
               # relief=SUNKEN,
               command=self.robotsendinfo).place(x=508,y=445)

        #消息发送按钮
        Button(root, text='发送',cursor='hand2', command=self.chatsendinfo).place(x=470, y=470)
        # img2 = PhotoImage(file='image/userinfo.png')
        # l12 = Label(root,image=img2)
        # l12.place(x=490,y=490)
        # img1 = PhotoImage(file='image/ceshi.png')
        # l11 = Label(root,image=img1,text='ssssss',compound=BOTTOM)
        # l11.place(x=500,y=500)

        root.mainloop()


# if __name__ == '__main__':
#     t = ServerTkinter()
#     t.main()

