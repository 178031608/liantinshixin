
import socket
from threading import Thread
import queue
from AI import ServerAI
from userinfoorder import Recvinfo
from ServerScreen import ServerTkinter
import time


HOST = '0.0.0.0'
PORT = 8888
all_user = {}


infoqueue = queue.Queue()
servershowinfo = queue.Queue()


#服务器接口函数
def xianshixuanze(data):
    print(data)

#控制收的函数
def recv_info(sockfd,recv1,Aiserver,screen):
    while True:
        print('等待消息')
        try:
            data,addr = sockfd.recvfrom(4096)
        except Exception as e:
            print(e)
            continue
        data = data.decode()
        print('服务器收到的消息是',data)
        recv1.put(data,addr)
        #如果是登录信息的话
        if data[:6] == '*登录信息:':
            s = recv1.userenter(addr)
            infoqueue.put(s)
            servershowinfo.put(s+'\n')
            # sockfd.sendto(jieguo.encode(), addr)
        #是找回密码消息
        elif data[:6] == '*找回密码:':
            s = recv1.getbackzhanghaomima(data[6:],addr)
            infoqueue.put(s)
            servershowinfo.put(s)
        #如过是注册信息的话
        elif data[:6] == '*注册信息:':
            #调用用户注册函数
            s = recv1.userenroll(addr)
            infoqueue.put(s)
            servershowinfo.put(s)
                # sockfd.sendto(sss.encode(),addr)
        elif data[:8] == '*匿名聊天模式:':
                recv1.nimingmoshijinru(data[8:],addr)
        elif data[:8] == '*获取房间列表:':
            s = recv1.get_home_list(addr)
            print('获取房间列表的s',s)
            infoqueue.put(s)
            # print('返回到主模块的房间列表',data)
        elif data[:10] == '*获取房间用户信息:':
            s = recv1.get_home_user(addr,data[10:])
            print('这是用户切换房间或者进入房间的消息',s)
            for t in s:
                infoqueue.put(t)
        elif data[:7] == '*用户退出了:':
            recv1.userquit(data[7:])
            servershowinfo.put(data+'\n')
        elif data[:7] == '*机器人消息:':
            return_s =recv1.robot_ai(data[7:],addr)
            infoqueue.put(return_s)
        elif data[:9] == '*私聊机器人消息:':
            return_s = recv1.si_robot_ai(data[9:],addr)
            infoqueue.put(return_s)
        elif data[:8] == '*获取用户信息:':
            s = recv1.get_home_user_info(data[8:],addr)
            infoqueue.put(s)
        elif data[:10] == '*私聊获取用户信息:':
            s = recv1.siliao_home_user_info(data[10:], addr)
            infoqueue.put(s)
        #如果是收到的奖励私聊模式
        elif data[:5] == '*我要与:':
            # print(addr)
            msg = recv1.createpribymoshi(data[5:],addr)
            infoqueue.put(msg)
        elif data[:7] == '*发送文件给:':
            s = recv1.sendtofileother(data[7:],addr)
            infoqueue.put(s)
        #如果收到了创建房间的消息给
        elif data[:6] == '*创建房间:':
            s = recv1.usercreatehome(data[6:],addr)
            # print('创建房间返回的s',s)
            #如果长度为1就表示失败了
            if len(s) == 1:
                infoqueue.put(s[0])
            else:
                screen.sendcreatehomeinfo(s[0],s[1])
                #返回给用户创建成功的消息
                infoqueue.put(s[2])
        else:
            servershowinfo.put(data)
            #如果正常聊天消息的话调用本函数
            #调用ServerAI模块的消息过滤踢人函数
            msgreturn,username = Aiserver.kick_out(data)
            #如果msg的前两个数字是*＃就表示所花有不文明用语
            if msgreturn[:2] == '*#':
                #处理方法
                screen.tirengongneng(username)
            #如果私聊消息们问题的话过滤用户信息返回各改发回的人
            elif msgreturn[:5] == '*发送给:':
                msg = recv1.siliaomsg(msgreturn[5:])
                infoqueue.put(msg)
            else:
                # print('需要获取房间用户发给各个用户了')
                t = data.split(':')
                userdict = recv1.infoyonggethomeuser(t[0],addr)
                for x in userdict:
                    print('应该到这里了',msgreturn)
                    if msgreturn.split(":")[1] == ' \n':
                        s = msgreturn+'&'+str(len(userdict))+'#'+addr[0]+'#'+str(addr[1])
                        print('应该到这里了',s )
                        infoqueue.put(s)
                        break
                    elif x != addr:
                        s = msgreturn+'&'+str(len(userdict))+'#'+x[0]+'#'+str(x[1])
                        infoqueue.put(s)
                # print('正常信息以上传到队列',s)
#控制发送的函数
def send_info(sockfd,recv1):
    while True:
        data = infoqueue.get()
        data = data.split('#')

        try:
            sockfd.sendto(data[0].encode(),(data[1],int(data[2])))
            print('发送的成功消息', data)
        except Exception as e:
            s ='发送给用户的数据这里出问题了内容是:'+e
            servershowinfo.put(s)
            continue

#控制服务器界面的用户列表显示
def Serverlistuser(recv1,screen):
    while True:
        data =recv1.get_userdict()
        screen.userlist(data)
        time.sleep(2)

def Serveruserinfos(screen):
    while True:
        data =servershowinfo.get()
        screen.showinfott(data)


def main():
    #创建套接字
    Server_s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #重置端口
    Server_s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    #绑定
    Server_s.bind((HOST,PORT))
    #实例化对象
    recv1 = Recvinfo()
    Aiserver = ServerAI()
    screen = ServerTkinter(Server_s)

   

    #一个线程控制收
    t1 = Thread(target=recv_info,args=(Server_s,recv1,Aiserver,screen))
    #一个线程控制发
    t2 = Thread(target=send_info, args=(Server_s,recv1))
    #控制服务器界面的用户列表显示
    t3 = Thread(target=Serverlistuser,args=(recv1,screen))
    t4 = Thread(target=Serveruserinfos, args=(screen,))
    t1.setDaemon(False)
    t2.setDaemon(False)
    t3.setDaemon(False)
    t4.setDaemon(False)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    #窗口界面主循环启动
    screen.main()

if __name__ == '__main__':
    main()
