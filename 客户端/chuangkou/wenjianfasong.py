from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog
import os
import time
from threading import Thread
from queue import Queue
msg=Queue()
msg1=Queue()
class Wenjian:
    def __init__(self,conn,othername):
        self.conn=conn
        self.othername=othername

    #更新进度条
    def progressbar_thread(self):
        try:
            #搭建带界面的进度条
            # self.button.config(state='disable')
            fill_line = self.canvas.create_rectangle(2, 2, 0, 27, width=0, fill='#64a131')
            with open(self.filename, 'rb') as rf:
                t = 0
                while True:
                    fileneirong = rf.read(4096)
                    t += len(fileneirong)
                    self.conn.send(fileneirong)
                    value = t / self.size * 100
                    self.canvas.coords(fill_line, (0, 0, 2 * value, 30))
                    s = '\n已上传了:' + str('%.2f' % (t / self.size * 100)) + '%'
                    self.text1.insert('end', s)
                    self.text1.see('end')
                    self.win.update()
                    # time.sleep(0.1)
                    if t == self.size:
                        time.sleep(1)
                        s='发送完毕了5秒后提出程序'
                        self.text.config(state=NORMAL)
                        self.text.delete('0.0', 'end')
                        self.text.insert('end', s)
                        self.text.see('end')
                        self.text.config(state=DISABLED)
                        self.win.update()
                        time.sleep(5)
                        self.win.destroy()
                        self.conn.close()
                        break
                    # print(fileneirong)
        except :
            pass


    def main1(self):
        data=self.conn.recv(4096)
        if data == b'Y':
            self.progressbar_thread()
        else:
            s = '对方拒绝接受文件3秒后退出'
            self.text.config(state=NORMAL)
            self.text.delete('0.0', 'end')
            self.text.insert('end', s)
            self.text.see('end')
            self.text.config(state=DISABLED)
            time.sleep(3)
            self.win.destroy()
            self.conn.close()





    #选择文件的函数
    def xuanzefile(self):
        self.filename = filedialog.askopenfilename()
        self.size = os.path.getsize(self.filename)
        self.text.config(state=NORMAL)
        self.text.delete('0.0','end')
        if self.size == 0:
            self.text.insert('end', self.filename + '\n文件长度:' + str(self.size)+'请重新选择')
            self.text.config(state=DISABLED)
            return
        else:
            self.text.insert('end', self.filename + '\n文件长度:' + str(self.size))
            self.text.config(state=DISABLED)
            name=self.filename.split('/')[-1]
            s = name+'&'+str(self.size)
            self.conn.send(s.encode())
            # print('发送数据了文件名字和文件长度',s)
            # data=self.conn.recv(4096)
            t3 = Thread(target=self.main1)
            t3.start()




    def main(self):
        #界面搭建
        self.win = Toplevel(bg='#CCCCCC')
        self.win.geometry('370x250')
        self.win.iconbitmap('image/tubiao.ico')
        self.win.title('发送给 %s 的文件'%self.othername)
        l1 = Label(self.win,bg='#313131',bd=0,relief=FLAT,width=100,height=2)
        l1.place(x=0,y=0)
        self.canvas = Canvas(self.win, width=200, height=26, bg='white')
        self.out_line = self.canvas.create_rectangle(2, 2, 200, 27, width=1, outline='black')
        self.canvas.place(x=10, y=45)
        self.text1 = Text(self.win,
                          fg='green',bg='#F2F2F2',
                          font =('Asira','10','bold'),
                          relief=FLAT,width=16, height=1)
        self.text1.place(x=230,y=50)
        l2 = Label(self.win,text='你选择的文件是:',
              font=('Asria','14','bold'),bg='#CCCCCC',fg='black',
              )

        l2.place(x=10,y=75)
        self.xuanzefilename=StringVar()
        self.text=Text(self.win,
                       bg='#F2F2F2',
                       relief=FLAT,width=52,height=8)
        self.text.place(x=0,y=100)
        self.text.config(state=DISABLED)
        Button(self.win,text='选择文件',
               font=('Asria', '14', 'bold'),
               bg='#F2F2F2',
               cursor='hand2',
               command=self.xuanzefile).place(x=100,y=215)
        self.var = StringVar()
        self.var.set('开始')
        # self.button = Button(self.win, textvariable=self.var, command=self.progressbar_thread, width=5)
        # self.button.place(x=220,y=80)
        # self.win.mainloop()





if __name__ == '__main__':
    a = Wenjian('1','2')
    a.main()
