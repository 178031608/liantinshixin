'''
该类为智能机器人类．

包含select_black_user方法是进行查询黑名单用户判断的方法．
包含black_user_add方法是进行黑名单加入的方法
包含bick_out方法是踢出用户的方法
包含robot_ai方法是智能机器人交互的方法，它在数据库自由一个交互信息数据表
如果数据表没有内容利用图灵机器人实现，然后加入本地数据表
'''
import requests
import json
import random

#定义机器人类
class ServerAI:

    #黑名单过滤
    def select_black_user(self,user):
        #数据库查询语句获取数据库黑名单列表
        black_user = ['a','abc','cba']
        if user in black_user:
            return "你是黑名单了！"

    #黑名单加入
    def black_user_add(self,message):
        msg = message.split[':']
        lst = ['65544']
        i = 0
        for x in lst:
            if x in msg[1]:
                i += 1
        if i == 0:
            #没问题直接返回该数据发送到目的地
            return message
        else:
            pass
            '踢出＋msg[0]'
            '全网通告'
            '加入黑名单'


    #踢人功能
    def kick_out(self,message):
        un = message.split(':')
        username=''
        if len(un) == 2:
            username = un[0]
        elif len(un) == 4:
            username = un[2]
        lst = ['草',]
        i = 0
        for x in lst:
            if x in message:
                break
            else:
                # 没问题直接返回该数据发送到目的地
                return message,username
        return '*#消息中含有了不文明用语',username





    #智能机器人相关
    def robot_ai(self,message):
        #调用数据库筛选数据返回列表
        lst = []
        if len(lst) != 0:
            data = random.choice(lst)
            return data

        else:
            key = '561925ade4d142d8b754fd1003a1951b'
            url = 'http://www.tuling123.com/openapi/api?key='+key+'&info='+message
            res = requests.get(url)
            res.encoding = 'utf-8'
            jd = json.loads(res.text)
            #向数据库中插入刷据
            # (message,jd['text'])
            return jd['text']

if __name__ == '__main__':
    s = ServerAI()

    s.robot_ai('服务器价格')
