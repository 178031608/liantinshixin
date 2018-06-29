import pymysql

def main():
    db = pymysql.connect('localhost','root','123456',charset='utf8')
    #上来删除库先
    try:
        cursr = db.cursor()
        drop = 'drop database alluser;'
        cursr.execute(drop)
        db.commit()
    except:
        pass
    finally:
        cursr.close()

    #删除第二个库
    try:
        cursr = db.cursor()
        drop = 'drop database Homeuserinfos;'
        cursr.execute(drop)
        db.commit()
    except:
        pass
    finally:
        cursr.close()



    #创建库
    try:
        cursr = db.cursor()
        drop = "create database alluser default charset='utf8';"
        cursr.execute(drop)
        db.commit()
    except:
        pass
    finally:
        cursr.close()

    #创建第二个库
    try:
        cursr = db.cursor()
        drop = "create database Homeuserinfos default charset='utf8';"
        cursr.execute(drop)
        db.commit()
    except:
        pass
    finally:
        cursr.close()
        db.close()

    #创建用户信息表
    db = pymysql.connect('localhost', 'root', '123456',"alluser", charset='utf8')
    cursr=db.cursor()
    # 创建用户信息表
    createalluserinfos=\
    '''
    create table alluserinfos(
    id int  auto_increment,
    password varchar(25),
    nickname varchar(20),
    realname varchar(10),
    IDnumber varchar(18),
    age char(3),
    sex char(3),
    likes varchar(30),
    city varchar(20),
    phonenumber char(11),
    meeting timestamp,
    unique(id),
    unique(nickname),
    unique(IDnumber)
    )auto_increment=10000 default charset='utf8';
    '''
    cursr.execute(createalluserinfos)
    db.commit()
    s = \
    '''
    insert into alluserinfos(password,nickname,realname,IDnumber,age,sex,likes,city,phonenumber) values
    ('1','测试','3','4','15','16','7','8','19'),
    ('1','测试2','33','35','35','36','37','38','39'),
    ('1','测试3','23','25','25','26','27','28','29'),
    ('1','测试4','43','45','45','46','47','48','49'),
    ('1','测试5','53','55','55','56','57','58','59'),
    ('1','测试9','33','95','95','96','97','98','99'),
    ('1','测试8','83','85','85','826','827','828','829'),
    ('1','测试6','63','65','65','646','467','488','489'),
    ('1','测试15','153','155','155','156','157','158','159');
    '''
    cursr.execute(s)
    db.commit()
    db.close()

    # 创建房间列表信息
    db = pymysql.connect('localhost','root','123456','Homeuserinfos',charset= 'utf8')
    cursr = db.cursor()
    createhomelist=\
    '''
    create table homelist(
    id int auto_increment,
    homename varchar(60),
    createuser varchar(60),
    homepassword varchar(100),
    unique(id),
    unique(homename)
    )default charset = 'utf8';
    '''
    cursr.execute(createhomelist)
    db.commit()

    #插入一些房间
    inserthome= \
        '''
        insert into homelist(homename,createuser,homepassword) values
        ('东方','管理员','*'),
        ('南方','管理员','*'),
        ('北方','管理员','*'),
        ('西方','管理员','*'),
        ('中方','管理员','*'),
        ('诸葛亮','管理员','*'),
        ('周瑜','管理员','*'),
        ('三国','管理员','*'),
        ('曹操','管理员','*'),
        ('黄盖','管理员','*');
        '''
    cursr.execute(inserthome)
    db.commit()
    cursr.close()

    # #创建房间内用户列表
    cursr = db.cursor()
    createhomealluser=\
    '''
    create table homealluser(
    homename varchar(20),
    usernickname varchar(20),
    useraddr varchar(30),
    unique(usernickname))default charset = 'utf8';
    '''
    cursr.execute(createhomealluser)
    db.commit()
    db.close()
#

#
# #房间内插入一些用户
# insert into homealluser values
# ('东方','东方10','192.168.1.116&51166'),
# ('东方','动方１','192.168.1.116&15566'),
# ('东方','东方２','192.168.1.116&51866'),
# ('东方','东方３','192.168.1.116&52966'),
# ('东方','东方４','192.168.1.116&63566'),
# ('东方','东方５','192.168.1.116&60666'),
# ('东方','东方６','192.168.1.116&16766'),
# ('东方','东方７','192.168.1.116&26866'),
# ('东方','东方８','192.168.1.116&61966'),
# ('东方','东方９','192.168.1.116&19966');


if __name__ == '__main__':
    main()