import pymysql
import re

class Homeinfo:
    def __init__(self):
        self.db = pymysql.connect\
        ('localhost','root','123456','Homeuserinfos',charset='utf8')
        
    #匿名模式的话加入匿名房间列表
    def newuseradd(self,data,useraddr):
        addr = useraddr[0]+'&'+str(useraddr[1])
        cursr=self.db.cursor()
        insert = """insert into homealluser values('匿名房间','%s','%s');
        """%(data,addr)
        cursr.execute(insert)
        self.db.commit()
        cursr.close()


    #获取所有房间列表
    def gain_home_list(self):
        cursr = self.db.cursor()
        select = 'select homename,homepassword from homelist;'
        cursr.execute(select)
        self.db.commit()
        data = cursr.fetchall()
        cursr.close()
        homel = ''
        for x in data:
            if x[0] == '匿名房间':
                continue
            #房间名字加房间密码&连接
            homel += x[0]+'@'+x[1]+':'

        # print('房间数据库里的所有房间列表',homel)
        return homel



    #管理员获取的所有房间函数，包含所有信息
    def getallhome(self):
        cursr = self.db.cursor()
        select = 'select * from homelist;'
        cursr.execute(select)
        self.db.commit()
        data = cursr.fetchall()
        cursr.close()
        return data

    #获取房间内的所有用户信息
    def gethomeusernickname(self,homename,nickname,addr):
        #先把该用户插入到数据库所在房间内在查询房间的用户列表
        useradd = addr[0]+'&'+str(addr[1])
        print(useradd,"这是useraddr",len(useradd))
        #下面是插入语句
        cursr = self.db.cursor()
        try:
            sqlinsert = \
            'insert into homealluser values('+"'"+homename+"'"+','+"'"+nickname+"'"+','+"'"+useradd+"');"
            cursr.execute(sqlinsert)
            # print('插入成功')
            self.db.commit()
            cursr.close()
        except Exception as e:
            print('插入不成功e',e)
            cursr.close()
            pass
        cursr = self.db.cursor()
        #也有可能是更新
        try:
            updata = \
            "update homealluser set homename='"+homename+"' where usernickname='"+\
                nickname +"';"
            cursr.execute(updata)
            self.db.commit()
            # print('更新成功现在的房间是',homename)
            cursr.close()
        except Exception as e:
            cursr.close()
            print('服务器更新用户的所在房间信息错了错误内容是,',e)
            pass
        try:
            #查询根据名字获取所有房间用户和用户addr
            cursr = self.db.cursor()
            select = \
            "select usernickname,useraddr from homealluser \
            where homename='"+homename+"';"
            cursr.execute(select)
            self.db.commit()
        except:
            pass
        finally:
            cursr.close()
        data = cursr.fetchall()
        print('data',data)
        return data

    #用于用户退出通知的给定房间名字返回房间所有的用户和addr
    def home_user_name_and_addr_from(self,homename):
        cursr = self.db.cursor()
        select = \
            "select usernickname,useraddr from homealluser \
            where homename='" + homename + "';"
        print('退出房间的时候的homename查询的时候的的值', homename)
        cursr.execute(select)
        self.db.commit()
        data = cursr.fetchall()
        print('data', data)
        cursr.close()
        return data


    #如果用户退出了
    def userquit(self,data):
        cursr = self.db.cursor()
        try:
            sqlinsert = \
                'delete from homealluser where usernickname=' + "'" + data + "';"
            cursr.execute(sqlinsert)
            self.db.commit()
        except:
            pass
        finally:
            cursr.close()
        # print(data,"用户已删除它退出了")

    #获取所有在线用户用户新用户登录判断
    def allonlineuser(self):
        cursr = self.db.cursor()
        try:
            sqlinsert = \
                'select usernickname from homealluser;'
            cursr.execute(sqlinsert)
            self.db.commit()
            data = cursr.fetchall()
            cursr.close()
        except:
            return
        user = []
        for u in data:
            user.append(u[0])
        # print('数据库得到的所有在线用户',user)
        return user

    #信息转发用的gethomeuser
    def gethomeuser(self,username,addr):
        cursr = self.db.cursor()
        selectqitayonghuaddr = \
        'select useraddr from homealluser where homename=(select homename from homealluser where '+\
        'usernickname='+"'"+username+"'"+');'
        cursr.execute(selectqitayonghuaddr)
        self.db.commit()
        data = cursr.fetchall()
        user = []
        for u in data:
            t = u[0].split('&')
            s = (t[0],int(t[1]))
            user.append(s)
        cursr.close()
        # print('这是房间所有用户除了发送者其他人的addr所在模块homemysql',user)
        #user是以列表形式的addr返回
        return user

    #服务器用的函数根据用户名字获得房间所有用户还有addr
    def severtirenyong(self,username):
        cursr = self.db.cursor()
        selectqitayonghuaddr = \
            'select usernickname,useraddr from homealluser where homename=(select homename from homealluser where ' + \
            'usernickname=' + "'" + username + "'" + ');'
        cursr.execute(selectqitayonghuaddr)
        self.db.commit()
        data = cursr.fetchall()
        #数据库的放回形式(('你好', '127.0.0.1&55292'),)
        # print('踢出用户数据库的返回值',data)
        cursr.close()
        return data

    #私聊模式用的addr
    def siliaomishi_get_othername_addr(self,othername):
        cur = self.db.cursor()
        select = """select useraddr from homealluser where usernickname='"""+othername+"';"
        cur.execute(select)
        self.db.commit()
        add = cur.fetchall()
        print('数据库的addr',add)
        addr = add[0]
        return addr

    #用于删除房间的功能
    def removehome(self,homename):
        cur = self.db.cursor()
        drop = '''delete from homelist where homename="%s";'''%(homename)
        cur.execute(drop)
        self.db.commit()
        cur.close()
        return '删除成功'

    #用于创建房间的功能,房间名字，创建者，密码可以为空默认值
    def createhome(self,homename,createuser,homepassword='*'):
        #对房间数据表进行操作，判断是否已存在房间，如果存在则返回创建失败，不存在则创建房间还有房间密码
        #房间字段设置，id自增长，homename(具有唯一性）,homeuser,homepassword,id不管
        cur=self.db.cursor()
        #直接创建使用try语句接受如果出现错误直接返回创建失败，名字已存在
        try:
            creahome="""
            insert into homelist(homename,createuser,homepassword) value
            ('%s','%s','%s');"""%(homename,createuser,homepassword)
            print(creahome)
            cur.execute(creahome)
            self.db.commit()
        except Exception as e:
            print('服务器或者用户创建房间时出错内容,',e)
            return '创建失败'
        finally:
            cur.close()
        return '创建成功'

    #用于获取所有在线用户的
    def getalluseradd(self):
        cur=self.db.cursor()
        select='''select useraddr from homealluser;'''
        cur.execute(select)
        self.db.commit()
        alladdr=cur.fetchall()
        return alladdr


if __name__ == '__main__':
    t = Homeinfo()
    t.gain_home_list()
    t.gain_home_user('东方')
    