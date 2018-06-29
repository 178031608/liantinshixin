from tkinter import *
from threading import Thread
from .weather import getAllWeather
import time
import sys,os
import tkinter.font as tkfont

class Nimingliaotian:
    def __init__(self,name,sockfd,addr):
        self.username = name
        self.sockfd = sockfd
        self.serveraddr = addr
        self.city = '天津'
        self.a = 'HELLO'

    # 实现样式设置，全部为黄色的底红色的字体加粗字体有返回值
    def showtime(self):
        s = time.strftime('%Y-%m-%d %H:%M:%T')
        return s + '\n'

    #接口用来控制主模块选择
    def getretu(self):
        return self.retu

    #用来接收服务端发回的消息
    def recvnewinfo(self):
        while True:
            dat,addr = self.sockfd.recvfrom(4096)
            data = dat.decode()
            if data[:7] == '*机器人消息:':
                s = self.showtime()
                self.aiinfo.config(state=NORMAL)
                self.aiinfo.insert('end',s,'yred')
                self.aiinfo.insert('end', data[1:])
                self.aiinfo.see('end')
                self.aiinfo.config(state=DISABLED)
            elif data[:7] == '*管理员消息:':
                    s=self.showtime()
                    self.showinfo.config(state=NORMAL)
                    self.showinfo.insert('end', s ,'yred')
                    self.showinfo.insert('end',data[1:])
                    self.showinfo.see('end')
                    self.showinfo.config(state=DISABLED)
            else:
                s = self.showtime()
                t = data.split(":")
                zaixian = '在线人数是:\n'
                print(t)
                renshu = t[1].split('&')
                self.var1.set(zaixian+renshu[1])
                print(self.var1)
                if renshu[0] != ' \n':
                    da = '******:'+renshu[0]
                    self.showinfo.config(state=NORMAL)
                    self.showinfo.insert('end',s,'yred')
                    self.showinfo.insert('end',da)
                    self.showinfo.see('end')
                    self.showinfo.config(state=DISABLED)



    #发送用户输入信息
    def sendtoliaotian(self):
        neirong = self.inpu.get('0.0','end')
        s = self.showtime()
        self.showinfo.config(state=NORMAL)
        self.showinfo.insert('end',s,'yred')
        self.showinfo.insert('end','我说:'+neirong)
        self.showinfo.see('end')
        self.showinfo.config(state=DISABLED)
        data =  self.username +':'+neirong
        self.sockfd.sendto(data.encode(),self.serveraddr)
        self.inpu.delete('0.0','end')

    def sendtoai(self):
        da = self.inpu.get(0.0, 'end')
        data = '*机器人消息:' + da
        self.sockfd.sendto(data.encode(), self.serveraddr)
        # 获取时间格式信息
        s = self.showtime()
        self.aiinfo.config(state=NORMAL)
        self.aiinfo.insert('end',s,'yred')
        self.aiinfo.insert('end', '我说:'+da)
        self.aiinfo.see('end')
        self.aiinfo.config(state=DISABLED)
        # 清空输入框
        self.inpu.delete(0.0, 'end')

    def weatherxianshi(self):
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
                            print('天气里的data准备切割', t)
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
                except :
                    pass

    def weatherupdate(self):
        self.city = self.weatherEntry.get()
        self.weatherEntry.delete(0,'end')

    def userquit(self):
        data = '*用户退出了:'+self.username
        self.sockfd.sendto(data.encode(),self.serveraddr)
        self.root.destroy()
        self.retu = 1

    def userquit1(self):
        data = '*用户退出了:' + self.username
        self.sockfd.sendto(data.encode(), self.serveraddr)
        self.root.destroy()
        self.retu=0

    def main(self):
        self.root = Tk()
        self.root.title('欢迎来到匿名聊天模式！')
        self.root.geometry('700x510')
        chushihua = PhotoImage(file='image/weather/chushihua.png')
        #菜单相关
        menubar = Menu(self.root)
        menubar.add_command(label='重新选择聊天方式',command=self.userquit)
        # 菜单实例应用到大窗口中
        self.root['menu'] = menubar


        #聊天消息相关框架和组件
        xianshi = LabelFrame(self.root,text='聊天信息')
        xianshi.place(x=5,y=5)
        huakuai=Scrollbar(xianshi)
        self.showinfo = Text(xianshi,width=60,height=20,relief=FLAT,yscrollcommand=huakuai.set)
        huakuai.pack(side=RIGHT,fill=Y)
        self.showinfo.pack(side=LEFT,fill=BOTH)
        huakuai.config(command=self.showinfo.yview)
        self.showinfo.tag_config('yred', foreground='red')
        self.showinfo.config(state=DISABLED)

        #机器人相关组件和滑块以及TEXT
        jiqi = LabelFrame(self.root,text='机器人消息')
        jiqi.place(x=5,y=290)
        huakuai1 = Scrollbar(jiqi)
        self.aiinfo = Text(jiqi,width=60,height=9,relief=FLAT,yscrollcommand=huakuai1.set)
        huakuai1.pack(side=RIGHT,fill=Y)
        self.aiinfo.pack(side=LEFT,fill=BOTH)
        huakuai1.config(command=self.aiinfo.yview)
        self.aiinfo.tag_config('yred', foreground='red')
        self.aiinfo.config(state=DISABLED)

        #输入框相关
        inpu = LabelFrame(self.root,text='输入框')
        inpu.place(x=5,y=430)
        huakuai2 = Scrollbar(inpu)
        self.inpu = Text(inpu,width=60,height=2 ,relief=FLAT,yscrollcommand=huakuai2.set)
        huakuai2.pack(side=RIGHT,fill=Y)
        self.inpu.pack(side=LEFT,fill=BOTH)
        huakuai2.config(command=self.inpu.yview)
        #天气显示框
        weate= LabelFrame(self.root,text='天气信息')
        weate.place(x=455,y=5)
        self.weathertext = StringVar()
        tkFont = tkfont.Font(family='Arial', size=14, weight=tkfont.BOLD)
        self.weather = Label(weate, fg='yellow', font=tkFont, textvariable=self.weathertext, compound='center')
        self.weather.pack()
        self.weathertext.set('获取天气中请稍等')
        self.weather.config(image=chushihua)

        #天气输入模板
        w1 = LabelFrame(self.root, text='请输入天气', width=219, height=60)
        w1.place(x=460, y=290)
        self.weatherEntry = Entry(w1)
        b4 = Button(w1, text='天气发送', cursor='hand2', command=self.weatherupdate)
        b4.place(x=148, y=0)
        self.weatherEntry.place(x=5, y=0)

        #一个带图片的Labe显示在线人数
        self.var1 = StringVar()
        # print('图框里的',self.var1)
        im = PhotoImage(file='image/niming.png')
        self.renshu= Label(self.root,textvariable=self.var1,font='Arial',image=im,compound='center')
        self.renshu.place(x=460,y=355)

        Button(self.root,text='发送',cursor='hand2',command=self.sendtoliaotian).place(x=490,y=465)
        Button(self.root, text='发送给机器人',cursor='hand2', command=self.sendtoai).place(x=580,y=465)

        #发送个服务器进入匿名聊天模式将用户加入到匿名聊天模式
        s = '*匿名聊天模式:'+self.username
        self.sockfd.sendto(s.encode(),self.serveraddr)

        #线程用来不断就收服务器反馈数据
        t1 = Thread(target=self.recvnewinfo)
        t1.start()
        t2 = Thread(target=self.weatherxianshi)
        t2.start()
        data5 = self.username + ':' + ' \n'
        self.sockfd.sendto(data5.encode(), self.serveraddr)
        self.root.protocol('WM_DELETE_WINDOW', self.userquit1)
        self.root.mainloop()

if __name__ == '__main__':
    s = Nimingliaotian()
    s.main()
