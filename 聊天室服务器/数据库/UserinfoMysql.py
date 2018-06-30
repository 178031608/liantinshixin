import pymysql


class Userinfo:
    #初始化本地数据库链接用的参数
    def __init__(self):
        self.db =pymysql.connect('localhost','root','123456','alluser',charset='utf8')

    #判断用户密码是否正确
    def aster_password(self,id):
        cursor = self.db.cursor()
        s = \
        'select password,nickname from alluserinfos where id=%s;'%id
        #注册时间测试　返回值2018-05-22 13:15:38
        # s = 'select meeting from alluserinfos where id=%s;'%id
        t = cursor.execute(s)
        self.db.commit()
        if t == 0:
            print('没有这个用户')
            return '没有这个用户'
        data = cursor.fetchone()

        cursor.close()
        return data
    #z找回密码功能
    def getbackzhanghaomima(self,daa):
        data = daa.split(':')
        cursr = self.db.cursor()
        select = \
            'select id,password from alluserinfos where IDnumber='+"'"+data[0]+"' and "+\
            'phonenumber='+"'"+data[1]+"';"
        t = cursr.execute(select)
        self.db.commit()
        cursr.close()
        if t == 0:
            return '身份证号或手机号不正确'
        info = cursr.fetchall()
        print(info)
        s = '用户账号:'+str(info[0][0])+'\n'+'用户密码:'+str(info[0][1])
        return s



    #注册用户
    def add_user_info(self,userinfo,IDnumber):
        cursr = self.db.cursor()
        #插入注册用户信息
        insert = \
        'insert into alluserinfos(password,nickname,realname,IDnumber,age,sex,likes,city,phonenumber) values(%s);'\
        %userinfo
        # print('inserer插入语句中的值',insert)
        try:
            cursr.execute(insert)
            self.db.commit()
        except Exception as a:
            print('错误是',a)
            return "昵称或者身份证重复了重复了!"
        #生成的最后一个ＩＤ
        zhanghanfanhui = '''select id from alluserinfos where IDnumber='%s';'''%IDnumber
        t = cursr.execute(zhanghanfanhui)
        self.db.commit()
        print('查询返回值',t)
        data = cursr.fetchone()
        print('查询的返回数据',data)
        cursr.close()
        return data[0]

    #获取用户详细信息格式
    def get_homeuser_info(self,username):
        # 返回值生成包含了age：sex: likes:ctiy: phonename:meiting
        #创建游标
        cur = self.db.cursor()
        select ="""select age,sex,likes,city,phonenumber,meeting from alluserinfos where nickname='"""+\
            username+"';"
        cur.execute(select)
        self.db.commit()
        data = cur.fetchall()
        s=''
        for i in data[0]:
           s += str(i)+':'
        #s=35:36:37:38:39:2018-05-27 14:03:28:
        return s

if __name__ == '__main__':
    s1 = Userinfo()
    # s1.aster_password(10001)

