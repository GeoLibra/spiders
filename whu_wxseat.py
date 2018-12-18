import requests
from lxml import etree
import json
import datetime
import time
import sys
class Whu_wxseat():
    def __init__(self,account,password):
        # 账号绑定
        self.bundle_url='http://system.lib.whu.edu.cn/libseat-wechat/bundle'
        # 当前预约
        self.current_book='http://system.lib.whu.edu.cn/libseat-wechat/currentBook'
        # 取消预约
        self.cancel_book='http://system.lib.whu.edu.cn/libseat-wechat/cancleBook'
        # buildId=1 信息馆 buildId=2 工学分馆 buildId=3 医学分馆  buildId=4 总管
        self.room_url='http://system.lib.whu.edu.cn/libseat-wechat/loadRooms'
        # 预约地址
        self.book_url='http://system.lib.whu.edu.cn/libseat-wechat/saveBook'
        # 座位信息
        'http://system.lib.whu.edu.cn/libseat-wechat/loadStartTime?seatId=3088&date=2018-12-17'
        # 查询座位的id
        self.seat_id='http://system.lib.whu.edu.cn/libseat-wechat/seats'
        # 获取时间
        self.time_url='http://system.lib.whu.edu.cn/libseat-wechat/loadStartTime'
        # 查看自习室
        self.house_url='http://system.lib.whu.edu.cn/libseat-wechat/loadRooms'
        self.session=requests.Session()
        self.account=account
        self.password=password
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1; MI 8 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044405 Mobile Safari/537.36 MMWEBID/3193 MicroMessenger/6.7.3.1360(0x2607033C) NetType/WIFI Language/zh_CN Process/tools'
        }
    def login(self):
        params = {
            'account': self.account,
            'password': self.password,
            'weChat': 'oCSNdswl242to6qNhaiRmojh9vq4',
            'linkSign': 'currentBook',
            'type': 'currentBook',
            'msg': ''
        }
        response=self.session.post(self.bundle_url,data=params,headers=self.headers)
        if response.status_code==200:
            print('登陆成功')
            return True
        else:
            print('登陆失败')
            return False
    def getCurBook(self):
        current = self.session.get(self.current_book,headers=self.headers)
        html = etree.HTML(current.text)
        html_data = html.xpath('//input[@id="book"]/@value')

        if html_data[0]:
            info = json.loads(html_data[0])
            bookId = info['id']
            print(
                "当前预约信息:\n" + info['location'] + '\n时间:' + info['begin'] + '--' + info['end'] + '\n' + info['message'])
            return bookId
        else:
            print("当前无预约")

    def get_seatId(self,roomId,seat_num,book_time):
        '?roomId=11&date=2018-12-17&linkSign=activitySeat&endTime='
        params={
            'roomId':roomId,
            'date':book_time,
            'linkSign':'activitySeat',
            'endTime':''
        }
        response=self.session.get(self.seat_id,params=params,headers=self.headers).json()
        seats = response['params']['seats']
        for i in seats:
            try:
                if i['name']==seat_num:

                    return i['id']
            except:
                pass
    def cancelBook(self,bookId):
        if bookId:
            params={'bookId':bookId}
            cancel = self.session.get(self.cancel_book,params=params,headers=self.headers)
            if cancel.status_code==200:
                print("取消预约")
            else:
                print("取消失败")
        else:
            return None
    def book(self):
        bookId=self.getCurBook()
        if bookId:
            x=input("当前已有预约,是否取消重新预约(y/n):")
            if x!="y":
                return
            else:
                self.cancelBook(bookId)

        book_day = input("请输入是否预约当天:t表示当天,m表示明天(默认):")
        nextDay = True if book_day != 't' else False
        seat.waitFor(nextDay)
        if not book_day:
            book_day = "m"
        book_time = input("请输入预约时间:如8:00-10:00(默认):")
        if not book_time:
            start = "8:00"
            end = "10:00"
        else:
            start = book_time.split("-")[0]
            end = book_time.split("-")[1]
        flag = input("是否严格匹配时间:y/n(默认严格匹配):")
        roomId = input("请输入自习室(roomId):")
        seat_num = input("请输入座位号(如023):")

        if book_day=='t':
            book_time=datetime.date.today()
        else:
            book_time=datetime.date.today()+datetime.timedelta(days=1)
        # book_time=book_time.strftime("%Y-%m-%d")
        seatId=self.get_seatId(roomId,seat_num,book_time)
        if seatId:
            start_time=self.get_time(seatId,start,book_time,flag)
            if not start_time:
                return
            end_time=self.get_time(seatId,end,book_time,flag,False)
            if not end_time:
                return
            params={
                'seatId':seatId,
                'date':book_time,
                'type':1,
                'start':start_time,
                'end':end_time,
            }
            response=self.session.get(self.book_url,params=params).json()
            response=json.loads(response)
            if response["status"]=="success":
                print("日期:",response["data"]["onDate"])
                print("位置:",response["data"]["location"])
                print("时间:",response["data"]["begin"]+'--'+response["data"]["end"])
                return True
            else:
                print("预约失败")
                print(response["message"])
        else:
            print("输入的座位号有误")
    def get_time(self,seatId,stime,book_time,flag,is_s=True):
        '?seatId=9158&date=2018-12-17'
        params = {'seatId': seatId,'date': book_time}
        response = self.session.get(self.time_url, params=params,headers=self.headers)
        time_range = response.json().split('/')
        if len(time_range)==0:
            print("当前暂无可用时间")
            return
        # 当时间不匹配时,开始时间返回最早的可预约时间,结束时间返回最晚的可预约时间
        if is_s:
            for i in json.loads(time_range[0]):
                if i['value'] == stime:
                    return i['id']
            if flag=='y':
                print("开始时间不匹配")
                return
            else:
                return json.loads(time_range[0])[0]['id']
        else:
            for i in json.loads(time_range[1]):
                if i['value'] == stime:
                    return i['id']
            if flag=='y':
                print("结束时间不匹配")
                return
            else:
                return json.loads(time_range[1])[-1]['id']
    def get_room(self,buildId=1):
        params={
            'buildId':buildId
        }
        response=self.session.get(self.house_url,params=params,headers=self.headers).json()
        rooms=response['params']['rooms']
        for i in rooms:
            print("roomId:%s, 自习室:%s楼%s, 剩余座位:%s" % (i['roomId'],i['floor'],i['room'],i['free']))
    def waitFor(self,nextDay=False):
        if nextDay:
            time_run = datetime.datetime.replace(datetime.datetime.now(), hour=22,
                                             minute=45, second=0)
            while True:
                delta = time_run - datetime.datetime.now()
                if delta.total_seconds() <= 0:
                    print('\n', end='')
                    break
                self.progressbar('正在等待系统开放,剩余' + str(int(delta.total_seconds())) + '秒')
                time.sleep(0.5)

    def progressbar(self,t_n):
        sys.stdout.write('\r')
        sys.stdout.write(t_n)
        sys.stdout.flush()
if __name__=="__main__":
    username = input("输入用户名:")
    password = input("输入密码:")
    seat=Whu_wxseat(username,password)
    seat.login()
    seat.get_room()
    result=seat.book()