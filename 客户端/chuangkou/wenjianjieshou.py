from threading import Thread
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import time
class Wenjianjieshou:
    def __init__(self, filename,filesize,conn,othername):
        self.filename=filename
        self.sockfd=conn
        self.size=filesize
        self.othername=othername



    #接收函数
    def jieshou(self):
        self.sockfd.send(b'Y')
        print('接收端发送个 发送者的Y', self.size)
        fill_line = self.canvas.create_rectangle(2, 2, 0, 27, width=0, fill='#64a131')
        with open(self.filelujin+'/'+self.filename,'wb') as of:
            t=0

            while True:
                data = self.sockfd.recv(5120)
                t += len(data)
                of.write(data)
                value = t / self.size * 100
                self.canvas.coords(fill_line, (0, 0, 2 * value, 30))
                self.win.update()
                s = '\n已接收了:' + str('%.2f' % (t / self.size * 100)) + '%'
                self.text1.insert('end', s)
                self.text1.see('end')
                self.win.update()
                print(data,t,self.size)
                if t == self.size:
                    print('进入跳出了了')
                    s='接受完毕了5秒后结束程序'
                    self.showfilelujing.config(state=NORMAL)
                    self.showfilelujing.delete('0.0', 'end')
                    self.showfilelujing.insert('0.0', s)
                    self.showfilelujing.config(state=DISABLED)
                    self.win.update()
                    time.sleep(5)
                    self.sockfd.close()
                    self.win.destroy()
                    break


    #拒绝接受文件
    def jujuejieshoufile(self):
        self.sockfd.send(b'N')
        self.win.destroy()
        self.sockfd.close()


        #选择保存路径
    def savefilelujing(self):
        # self.button.config(state='disable')
        self.filelujin = filedialog.askdirectory()
        print(self.filelujin)
        self.showfilelujing.config(state=NORMAL)
        self.showfilelujing.delete('0.0', 'end')
        self.showfilelujing.insert('0.0', self.filelujin+'/'+self.filename)
        self.showfilelujing.config(state=DISABLED)
        t2= Thread(target=self.jieshou)
        t2.start()



    def main(self):
        self.win=Toplevel()
        self.win.geometry('370x210')
        self.win.title('从 %s 处接受文件'%self.othername)
        self.canvas = Canvas(self.win, width=200, height=26, bg='white')
        self.out_line = self.canvas.create_rectangle(2, 2, 200, 27, width=1, outline='black')
        self.canvas.place(x=10, y=5)
        self.text1 = Text(self.win, relief=FLAT,width=16, height=1)
        self.text1.place(x=230, y=10)
        #一个按钮用来设置保存文件路径选择和一个text控件显示保存文文件路径名字显示
        Label(self.win,text='文件保存路径为').place(x=10,y=35)
        self.showfilelujing = Text(self.win,relief=FLAT,width=50,height=8)
        self.showfilelujing.place(x=10,y=55)
        self.showfilelujing.config(state=DISABLED)
        Button(self.win,text='接收文件-选择保存文件路径',cursor='hand2',command=self.savefilelujing).place(x=30,y=170)
        # self.button = Button(self.win,text='接收文件', command=self.jieshou)
        # self.button.place(x=170,y=85)
        Button(self.win, text='拒绝接收',cursor='hand2', command=self.jujuejieshoufile).place(x=250, y=170)
        # mainloop()

if __name__ == '__main__':
    a = Wenjianjieshou(2,3,6,1)
    a.main()