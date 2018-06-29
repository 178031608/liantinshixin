from tkinter import *
import os,sys
import tkinter.messagebox as message

class Dengluzhuce:
    def __init__(self,sockfd,addr):
        self.root = Tk()
        self.login_info = ''
        self.zhongwen = ''
        self.conn=sockfd
        self.addr = addr
        #Unicode所有的中文
        for x in range(0x4e00, 0x9f9d):
            self.zhongwen += chr(x)
        self.zhanghaomima= ''
        self.retu=1

    #接口返回给调用者和是注册信息还是登录信息
    def userxuanzeliaotianmoshi(self):
        return self.xuanzeliaotianmoshi+':'+self.username

    #获得选择的模式的值
    def printList2(self):
        self.xuanzeliaotianmoshi = '匿名聊天'
        self.liaotianmoshixuanze.destroy()

    #获得选择的模式的值
    def printList1(self):
        self.xuanzeliaotianmoshi = '房间聊天'
        self.liaotianmoshixuanze.destroy()


    def userquit(self):
        self.xuanzeliaotianmoshi = ''
        self.liaotianmoshixuanze.destroy()

    #接口用户登录直接点关闭
    def rootquit(self):
        return self.retu

    #如果没登录直接点击了关闭
    def userquit1(self):
        self.retu=0
        self.root.destroy()

    def xuanzefangshi(self):
        self.liaotianmoshixuanze = Tk()
        self.xuanze = PhotoImage(file='image/homeselect.png')
        self.liaotianmoshixuanze.geometry('704x799')
        #背景图片设置
        Label(self.liaotianmoshixuanze,
              image=self.xuanze,
              ).place(x=0,y=0)
        img1 = PhotoImage(file='image/nimingmoshi.png')
        img2 = PhotoImage(file='image/fangjianmoshi.png')
        # 匿名模式按钮
        Button(self.liaotianmoshixuanze,
               width=325,
               height=75,
               image=img1,
               bd=0,
               relief=FLAT,
               cursor='hand2',
               command=self.printList2).place(x=190, y=283)
        # 房间模式按钮
        Button(self.liaotianmoshixuanze,
               width=325,
               height=75,
               image=img2,
               bd=0,
               relief=FLAT,
               cursor='hand2',
               command=self.printList1).place(x=190, y=388)
        self.liaotianmoshixuanze.mainloop()

    def get_user_info(self):
        # 获取用户账号密码
        self.zhanghaomima= '*登录信息:'+self.zhanghao.get()+':'+ self.password.get()
        data= self.zhanghaomima.encode()
        print(data)
        (self.conn).sendto(data,self.addr)
        data1, addr = self.conn.recvfrom(4096)
        print(data1.decode())
        #如果是正确信心
        if data1.decode()[0] == 'Y':
            self.username = data1.decode()[2:]
            self.root.destroy()

        else:
            #如果是错误信息
            to = Toplevel(width = 400,height=400)
            to.geometry('220x200' )
            Label(to,text = '错误提示\n'+data1.decode()).pack()
            b1 = Button(to,text='重新输入',cursor='hand2',command = to.destroy)
            b1.pack(side='bottom')

    #手机用户找回密码功能所输入的数据并发送
    def getbacktijiao(self):
        shenfenzhenghao = self.getbackidshenfenzheng.get()
        phone = self.getbackphone.get()
        s = '*找回密码:'+shenfenzhenghao+':'+phone
        self.conn.sendto(s.encode(),self.addr)
        data,addr = self.conn.recvfrom(4096)
        #返回的数据弹出顶级菜单显示
        info = data.decode()
        print(info[:5])
        t1 = Toplevel(self.getps)
        t1.geometry('220x200' )
        Label(t1,text=info).pack()
        if info[:5] == '用户账号:':
            b1 = Button(t1,text='确定',cursor='hand2',command=self.getps.destroy)
            b1.pack(side='bottom')
        else:
            b1 = Button(t1, text='再试一次',cursor='hand2', command=t1.destroy)
            b1.pack(side='bottom')


    #找回密码功能
    def getbackuserpassword(self):
        self.getps = Toplevel(self.root)
        self.getps.geometry('500x510')
        bm = PhotoImage(file='image/zhaohuimima.png')
        l1 =Label(self.getps,image=bm)

        l1.place(x=0,y=0)
        # Label(self.getps, text='身份证号').place(x=5, y=50)
        # Label(self.getps, text='手机号').place(x=5, y=110)
        self.getbackidshenfenzheng = Entry(self.getps,
                                           font=('Adobe 黑体 Std', '28'),
                                           width=16,
                                           bd=0, bg='#CCCCCC',
                                           fg='red',  relief=FLAT, insertbackground='yellow',
                                           highlightthickness=3, highlightcolor='#17536B',
                                           highlightbackground='#3B87A9', justify=CENTER,
                                           )
        self.getbackphone = Entry(self.getps,
                                  font=('Adobe 黑体 Std', '28'),
                                  width=16,
                                  bd=0, bg='#CCCCCC',
                                  fg='red', relief=FLAT, insertbackground='yellow',
                                  highlightthickness=3, highlightcolor='#17536B',
                                  highlightbackground='#3B87A9', justify=CENTER,
                                  )
        self.getbackidshenfenzheng.place(x = 151,y=203)
        self.getbackphone.place(x = 151,y=325)
        img2 = PhotoImage(file='image/zhaohuimimaqueding.png')
        Button(self.getps,
               width=80,
               height=70,
               image=img2,
               bd=0,
               relief=FLAT,
                cursor='hand2',command = self.getbacktijiao).place(x =210,y = 415)
        self.getps.mainloop()
    def enter_Tk(self):
        s = '欢迎来到聊天室请登录'
        self.root.geometry('1184x537')
        self.root.title(s)
        self.root.iconbitmap('image/tb.ico')

        bm = PhotoImage(file="image/denglu.png")
        t2 = Label(self.root, image=bm)
        t2.place(x=0,y=0)
        # t1 = Label(self.root, text='账号')
        # t1.place(x=60,y=235)
        # Label(self.root, text='密码').place(x=60,y=265)
        self.zhanghao = Entry(self.root,
                              bd=0,
                              font=('Helvetica', '20'),
                              # bg='',
                              fg='red',justify=CENTER,
                              width=17,
                              relief=FLAT,
                              insertbackground='green',
                              highlightthickness=4,
                              highlightcolor='pink',

                              )

        self.password = Entry(self.root,
                              bd=0,
                              font=('Helvetica', '20'),
                              # bg='',
                              fg='red',
                              width=17,justify=CENTER,
                              relief=FLAT,
                              insertbackground='green',
                              highlightthickness=4,
                              highlightcolor='pink',
                              show = '*')
        self.zhanghao.place(x=780, y=188)
        self.password.place(x=780, y=248)
        zhmima = PhotoImage(file='image/zhohuimima.png')
        zhuce = PhotoImage(file='image/zhuce.png')
        dengluanniu = PhotoImage(file='image/dengluanniu.png')
        Button(self.root,
               width=250,
               height=45,
               image=dengluanniu,
               bd=0,
               relief=FLAT,
               cursor='hand2',
               command=self.get_user_info
               ).place(x=770,y=340)
        #找回密码按钮
        Button(self.root,
               width=85,
               height=30,
               image=zhmima,
               bd=0,
               relief=FLAT,
               cursor='hand2',
               command=self.getbackuserpassword).place(x=780,y=290)
        #注册按钮
        Button(self.root,
               width=72,
               height=25,
               image=zhuce,
               bd=0,
               relief=FLAT,
               cursor='hand2',
               command=self.new_user).place(x=955,y=295)

        self.root.protocol('WM_DELETE_WINDOW', self.userquit1)
        self.root.mainloop()

    def new_user(self):
        # 获取所有的详细信息
        def gets_info():
            #不正确信息列表存放
            not_data = []
            #判断身份证号是否正确
            pidcard = identitycard.get().strip()
            a = ['1','2','3','4','5','6','7','8','9','0','x']
            i = 0
            for x in pidcard:
                if x in a:
                    i +=1
            if i != 18:
                print(i)
                not_data.append('身份证号不正确,长度是18位')
            #判断手机号是否正确
            pnumber = phonnumber.get().strip()
            if len(pnumber) != 11:
                not_data.append('手机号长度是11位，输入不正确')
            #判断性别是否输入正确
            se_x = sex.get().strip()
            if se_x =='男' or se_x == '女' or se_x == 'M' or se_x == 'F':
                pass
            else:
                not_data.append('性别输入不正确,男，女，M或者F')
            #判断密码是否正确
            symbols = r'''`!@#$%^&*()_+-=/*{}[]\|'";:/?,.<>'''
            for sym in symbols:
                if sym in newuserpasswd.get() or newuserpasswd.get().isdigit() or newuserpasswd.get().isalpha() or \
                        len(newuserpasswd.get()) < 8:
                    not_data.append('密码输入不合法，请输入数字加字母，不要有特殊字符,长度大于8')
                    break
            #判断名字输入
            newname= name.get().strip()
            for x in newname:
                if x == '@':
                    break
                elif x not in self.zhongwen:
                    not_data.append('名字输入不正确')
                    break

            if len(petname.get()) == 0:
                not_data.append('昵称没输入')
            if  len(age.get()) == 0:
                not_data.append('年龄没输入')
            if len(like.get()) == 0:
                not_data.append('爱好没有输入')
            if len(city.get()) == 0:
                not_data.append('城市没有输入')
            #如果有错误的输入
            if len(not_data) != 0:
                info=''
                for not_info in not_data:
                    info+=not_info+'\n'
                message.showerror(title='注册信息输入错误',message=info)
            else:   
                #生成正确信息
                self.zhanghaomima = '*注册信息:'+newuserpasswd.get()+':'+petname.get()+':'+ \
                                  name.get()+':'+identitycard.get().strip()+':'+age.get()+ \
                                  ':'+sex.get()+':'+like.get()+':'+city.get()+':' \
                                  +phonnumber.get().strip()
                self.conn.sendto((self.zhanghaomima).encode(), self.addr)
                print(self.zhanghaomima)
                data,addr = self.conn.recvfrom(4096)
                #用弹窗显示服务器返回值
                if data.decode()[0] != 'Y':
                    message.showerror(title='注册用户出错了',message=data)
                else:
                    message.showerror(title='注册用户成功了', message=data[2:])

                # ********************************************


        #控制输入存数字，给数字不显示
        def test(content):
            return content.isdigit()
        v2 = StringVar()
        self.root.iconify()
        self.login = Toplevel(self.root,bd=0,relief=FLAT)
        testCMD = self.root.register(test)
        self.login.geometry('1184x537')

        bm1 = PhotoImage(file="image/zhucescreen.png")
        Label(self.login,image=bm1).place(x=0,y=0)

        # 用户注册信息
        # Label(self.login, text='密码').place(x=10,y=290)
        # Label(self.login, text='昵称').place(x=200,y=290)
        # Label(self.login, text='姓名').place(x=10,y=320)
        # Label(self.login, text='身份证号').place(x=190,y=320)
        # Label(self.login, text='年龄').place(x=10,y=350)
        # Label(self.login, text='性别').place(x=200,y=350)
        # Label(self.login, text='爱好').place(x=10,y=380)
        # Label(self.login, text='城市').place(x=200,y=380)
        # Label(self.login, text='手机号').place(x=5,y=410)
        #s各种输入框
        newuserpasswd = Entry(self.login,
                              bd=0, font=('Helvetica', '21'), bg='#3B87A9',
                              fg='red', width=12, relief=FLAT, insertbackground='yellow',
                              highlightthickness=3, highlightcolor='#17536B',
                              highlightbackground='#3B87A9',justify=CENTER,
                              )
        petname = Entry(self.login,
                        bd=0, font=('Helvetica', '21'), bg='#3B87A9',
                        fg='red', width=12, relief=FLAT, insertbackground='yellow',
                        highlightthickness=3, highlightcolor='#17536B',
                        highlightbackground='#3B87A9',justify=CENTER,
                        )
        name = Entry(self.login,
                     bd=0, font=('Helvetica', '21'), bg='#3B87A9',
                     fg='red', width=12, relief=FLAT, insertbackground='yellow',
                     highlightthickness=3, highlightcolor='#17536B',
                     highlightbackground='#3B87A9',justify=CENTER,
                     )
        identitycard = Entry(self.login,
                             bd=0, font=('Helvetica', '21'), bg='#3B87A9',
                             fg='red', width=15, relief=FLAT, insertbackground='yellow',
                             highlightthickness=3, highlightcolor='#17536B',
                             highlightbackground='#3B87A9',justify=CENTER,
                             )
        age = Entry(self.login,
                    bd=0, font=('Helvetica', '21'), bg='#3B87A9',
                    fg='red', width=12, relief=FLAT, insertbackground='yellow',
                    highlightthickness=3, highlightcolor='#17536B',
                    highlightbackground='#3B87A9',justify=CENTER,
                    )
        sex = Entry(self.login,
                    bd=0, font=('Helvetica', '21'), bg='#3B87A9',
                    fg='red', width=12, relief=FLAT, insertbackground='yellow',
                    highlightthickness=3, highlightcolor='#17536B',
                    highlightbackground='#3B87A9',justify=CENTER,
                    )
        like = Entry(self.login,
                     bd=0, font=('Helvetica', '21'), bg='#3B87A9',
                     fg='red', width=12, relief=FLAT, insertbackground='yellow',
                     highlightthickness=3, highlightcolor='#17536B',
                     highlightbackground='#3B87A9',justify=CENTER,
                     )
        city = Entry(self.login,
                     bd=0,font=('Helvetica', '21'),bg='#3B87A9',
                     fg='red',width=12,relief=FLAT,insertbackground='yellow',
                     highlightthickness=3,highlightcolor='#17536B',
                     highlightbackground='#3B87A9',justify=CENTER,
                     )
        phonnumber = Entry(self.login,textvariable=v2,validate='key',
                           bd=0, font=('Helvetica', '21'), bg='#3B87A9',
                           fg='red', width=12, relief=FLAT, insertbackground='yellow',
                           highlightthickness=3, highlightcolor='#17536B',
                           highlightbackground='#3B87A9', justify=CENTER,
                            validatecommand=(testCMD, '%P'))
        petname.place(x=330,y=168)
        newuserpasswd.place(x=742,y=165)
        name.place(x=330,y=234)
        city.place(x=742, y=230)
        age.place(x=330,y=301)
        sex.place(x=742,y=296)
        phonnumber.place(x=330, y=368)
        like.place(x=742,y=368)
        identitycard.place(x=330,y=430)


        # 下边的按钮
        zhucequding= PhotoImage(file='image/zhucequding.png')
        zhucequxiao = PhotoImage(file='image/zhucequxiao.png')
        Button(self.login,
               width=165, height=40,
               image=zhucequding, bd=0,
               relief=FLAT,
               cursor='hand2',command=gets_info).place(x=595,y=428)
        #取消按钮
        t = Button(self.login,
                   width=165, height=40,
                   image=zhucequxiao, bd=0,
                   relief=FLAT,
                   cursor='hand2',command = self.quitzhuce).place(x=790,y=428)

        self.login.mainloop()

    #注册按钮所用的退出
    def quitzhuce(self):
        self.login.destroy()
        self.root.deiconify()


if __name__ =='__main__':
    s = Dengluzhuce(1,2)
    s.new_user()
