
from 数据库.UserinfoMysql import Userinfo
from 数据库.Homemysql import Homeinfo
from AI import ServerAI

#这个类用来处理用户输入数据的
class Recvinfo:
    def __init__(self):
        #初始化用户在线字典用昵称(具有唯一性)：addr
        self.userdict = {}
        #初始化生成userinfo数据库查询类的对象
        self.usermysql = Userinfo()
        self.homemysql = Homeinfo()
        self.serverAI = ServerAI()
        self.dict_home_user ={}

    #接口获取函数
    def put(self,data,addr):
        #用户发送数据data
        self.data = data
        #用户的addr
        self.addr = addr
            
    #这是个获取在线用户信息的接口
    def get_userdict(self):
        self.userdict = self.homemysql.allonlineuser()
        return self.userdict


    #如果是登信息的话
    def userenter(self,addr):
        data = self.data.split(':')
        #用户帐号
        userID= data[1]
        #用户密码
        userpassword= data[2]
        #去数据库对比返回知为(密码,昵称)
        mysqldata = self.usermysql.aster_password(userID)
        if mysqldata[0] == userpassword:
            print('c错误的地方',mysqldata)
            #调用在线用户数据数据返回所有在线用户
            self.userdict=self.homemysql.allonlineuser()
            if self.userdict:
                #如果不再用户列表里就把它加入到列比里
                if mysqldata[1] in self.userdict:
                    return '该用户已存在'+'#'+addr[0]+'#'+str(addr[1])
            #如果没有问题就返回Y加用户名
            return 'Y '+mysqldata[1]+'#'+addr[0]+'#'+str(addr[1])
        elif mysqldata == '没有这个用户':
            return mysqldata+'#'+addr[0]+'#'+str(addr[1])
        else:
            return '密码错误'+'#'+addr[0]+'#'+str(addr[1])

    #找回密码
    def getbackzhanghaomima(self,data,addr):
        s = self.usermysql.getbackzhanghaomima(data)
        info = s + '#' + addr[0] + '#' + str(addr[1])
        return info

    #注册用户
    def userenroll(self,addr):
        data = self.data.split(':')
        del data[0]
        IDnumber=data[3]
        #具体信息已逗号组合成字符串
        s = ''
        for x in data:
            s += "'"+str(x)+"'" + ','
        userinfo = s[:-1]
        # print(userinfo)
        #返回注册函数返回的结果加密码
        jieguo = str(self.usermysql.add_user_info(userinfo,IDnumber))+':'+data[0]
        jieguo = jieguo.split(':')
        # 如果输入有误
        if jieguo[0] == '昵称或者身份证重复了重复了:':
            s = jieguo[0] + '#' + addr[0] + '#' + str(addr[1])
            # sockfd.sendto(jieguo[0].encode(),addr)
        else:
            sss = 'Y 你的账号请牢记\n账号:' + jieguo[0] + '\n密码:' + jieguo[1]
            s = sss + '#' + addr[0] + '#' + str(addr[1])
        return s
    #如果是匿名聊天模式怎吧用户加入到匿名房间里
    def nimingmoshijinru(self,data,addr):
        self.homemysql.newuseradd(data,addr)

    # 获取房间的用户的详细信息用于客户端双击房间列表内的用户了
    def  get_home_user_info(self,username,addr):
        # print('username', username)
        #返回值生成包含了age：sex:likes:ctiy:phonename:meiting
        t = self.usermysql.get_homeuser_info(username)
        s = '*获取用户信息:'+t+'#'+addr[0]+'#'+str(addr[1])
        print(s)
        return s
    #用于私聊模式获取用户信息
    def siliao_home_user_info(self,username, addr):
        t = self.usermysql.get_homeuser_info(username)
        s = '*私聊获取用户信息:' + t + '#' + addr[0] + '#' + str(addr[1])
        return s


    #获取房间列表
    def get_home_list(self,addr):
        data = self.homemysql.gain_home_list()
        return '*获取房间列表:'+data+'#'+addr[0]+'#'+str(addr[1])

    #退出房间通知
    def user_qiut_home(self,username,addr):
        addrname = '<用户 ' + username + ' 退出了 ' + self.dict_home_user[username] + ' 房间>\n'
        #退出时返回用户以前的房间内内的所有成员信息（name,addr)
        allusername = self.homemysql.home_user_name_and_addr_from(self.dict_home_user[username])
        #只用来发送通知
        alluserlistmsg = []
        for uaddr in allusername:
            t = uaddr[1].split('&')
            useraddr = (t[0], int(t[1]))
            # 给每个用户发送房间列表
            # 给其他用户发送欢迎退出信息
            if useraddr != addr:
                msg = addrname + '#' + useraddr[0] + '#' + str(useraddr[1])
                alluserlistmsg.append(msg)

        return alluserlistmsg

    #欢迎房间信息
    def weclomehome(self,username,homename,addr):
        # 过来的用户的昵称
        addrname = '<欢迎用户 ' + username + ' 来到 ' + homename + ' 房间>\n'
        # 返回该房间的所有用户名字和房间内所有的用户addr
        allusername = self.homemysql.gethomeusernickname(homename,username, addr)
        # s是所有用户名字用':'组合
        s = '*获取房间用户信息:'
        for x in allusername:
            s += str(x[0]) + ':'
        alluserlistmsg = []

        for uaddr in allusername:
            t = uaddr[1].split('&')
            useraddr = (t[0], int(t[1]))
            # 给每个用户发送房间列表
            alluserlistmsg.append(s + '#' + useraddr[0] + '#' + str(useraddr[1]))
            # 给其他用户发送欢迎退出信息
            if useraddr != addr:
                msg = addrname + '#' + useraddr[0] + '#' + str(useraddr[1])
                alluserlistmsg.append(msg)
        return alluserlistmsg


    #获取房间用户信息
    def get_home_user(self,addr,homeandusername):
        listquitfanhui=qiutfanhui = []
        homename = homeandusername.split(":")[0]
        username = homeandusername.split(":")[1]
        if username not in self.dict_home_user:
            self.dict_home_user[username] = homename
            msg = self.weclomehome(username, homename, addr)
            return msg
        else:
            #先更准备好欢迎语言并更新新用户数据库内的用户房间名字
            msg=self.weclomehome(username, homename, addr)

            # 发送退出房间通知听通知后更新新的字典
            m = self.user_qiut_home(username, addr)
            print('到这里了，这是发送户退出的通知msg=',msg,'**m=',m)
            self.dict_home_user[username] = homename
            return msg+m


        #机器人消息
    def robot_ai(self,data,addr):
        s = self.serverAI.robot_ai(data)
        #根据返回数据生成
        return_s = '*机器人消息:'+s+'#'+addr[0]+'#'+str(addr[1])
        return return_s
    #私聊机器人消息
    def si_robot_ai(self,data,addr):
        s = self.serverAI.robot_ai(data)
        return_s = '*私聊机器人消息:'+s+'#'+addr[0]+'#'+str(addr[1])
        return return_s

    #获取房间内用户信息发消息用的
    def infoyonggethomeuser(self,username,addr):
        data = self.homemysql.gethomeuser(username,addr)
        return data

    #用户退出消息
    def userquit(self,data):
        self.homemysql.userquit(data)
        # self.get_userdict()
        print('这是用户退出后的用户列表',self.userdict)

    #如果是建立私聊模式的消息addr是发送者的addr
    def createpribymoshi(self,data,addr):
        t = data.split(':')
        # print('t',t)
        #要建立连接的对象的名字
        othername = t[0]
        #发起者的名字
        myname = t[1]
        #获取ohernamde的addr还有
        otheradd = self.homemysql.siliaomishi_get_othername_addr(othername)
        otheraddr = otheradd[0].split('&')
        print('otheraddr',otheraddr)
        msg = '*与:'+myname+':建立私聊'+'#'+otheraddr[0]+'#'+str(otheraddr[1])
        print('建立私聊的用户的返回消息:',msg)
        return msg
    #私聊消息的haul
    def siliaomsg(self,data):
        #data=测试3:测试1:FASFASD
        s = data.split(':')

        otheradd = self.homemysql.siliaomishi_get_othername_addr(s[0])
        otheraddr = otheradd[0].split('&')
        # print('otheraddr', otheraddr)
        msg = '*私聊消息来自:' +s[1]+ ':'+s[2] + '#' + otheraddr[0] + '#' + str(otheraddr[1])
        return msg

    #根据其他用户名字获取addr并返回要给他发送文件
    def sendtofileother(self,data,addr):
        print('data',data)
        othername=data.split(':')[1]
        otheradd=self.homemysql.siliaomishi_get_othername_addr(othername)
        otheraddr=otheradd[0].split('&')
        print('获取到用户是：',otheraddr)
        #返回给目标用户数据准备接受文件+发送者addr+&+端口
        msg ='*准备接受文件:'+addr[0]+'&'+data.split(":")[0]+'#'+otheraddr[0]+'#'+str(otheraddr[1])
        return msg

    #用户创建房间的话
    def usercreatehome(self,data,addr):
        # 使用管理员广播功能给所有用户发送创建成功的消息，失败则返回创建用户
        t = data.split(':')
        username=t[0]
        homename=t[1]
        if len(t) == 3:
            homepwd=t[2]
            print('userinfoorder创建放假pwd',homepwd)
            createreturn = self.homemysql.createhome(homename,username,homepwd)
        # 用于创建房间的功能,房间名字，创建者，密码可以为空默认值
        else:
            createreturn = self.homemysql.createhome(homename,username)
        if createreturn == '创建失败':
            return ['*创建房间:创建失败'+'#'+addr[0]+'#'+str(addr[1])]
        else:
            #创建成功 则用管理员名义给所有用户发送管理员信息，并给用户发送成功数据
            return [homename,username,'*创建房间:创建成功'+'#'+addr[0]+'#'+str(addr[1])]