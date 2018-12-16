import requests
import time
import datetime


class MySeat:
    def __init__(self, uname, pwd):
        self.login_url = 'http://seat.lib.whu.edu.cn/rest/auth'
        self.user_url = 'http://seat.lib.whu.edu.cn/rest/v2/user/reservations'
        self.book_url = 'http://seat.lib.whu.edu.cn/rest/v2/freeBook'
        # 结束使用
        self.stop_url='http://seat.lib.whu.edu.cn/rest/v2/stop'
        # 取消
        self.cancel_url='http://seat.lib.whu.edu.cn/rest/v2/cancel'
        self.search_url='http://seat.lib.whu.edu.cn/rest/v2/room/layoutByDate/6/'
        self.headers = {
            'Host': 'seat.lib.whu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
        }
        self.today = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.username = uname
        self.password = pwd
        self.token = self.getTocken()

    # 登陆获取token
    def getTocken(self):
        params = {
            'username': self.username,
            'password': self.password
        }

        r = requests.get(self.login_url, params=params, headers=self.headers)

        if r.status_code==200:
            data=r.json()

            if data['status'] == 'success':

                return data['data']['token']
            else:
                print('登陆失败')
        else:
            print("登陆失败")

    # 利用token查询用户预约状态
    def getUserInfo(self):
        params = {
            'token': self.token
        }
        r = requests.get(self.user_url, params=params, headers=self.headers).json()
        if r['status'] == 'success':
            if r['data']:
                info = r['data'][0]

                print('预约时间:%s' % (info['begin'] + '--' + info['end']))
                print('预约位置:%s' % info['location'])
                return r
            else:
                print('当前没有预约')
        else:
            print('需要重新登陆')

    def bookSeat(self, startTime, endTime,seat_num):
        params = {
            'token': self.token,
            'seat': seat_num,
            'date': self.today,
            'startTime': startTime,
            'endTime': endTime
        }

        r = requests.post(self.book_url, params=params, headers=self.headers).json()
        if r['status'] == 'success':
            print('时间:%s\n位置:%s' % (r['data']['begin'] + '--' + r['data']['end'], r['data']['location']))
            return True
        else:
            # print(params)
            print('预约失败')
            return False

    def waitFor(nextDay=False):
        if nextDay:
            time_run = datetime.datetime.replace(datetime.datetime.now(), hour=22,
                                             minute=45, second=0)
            while True:
                delta = time_run - datetime.datetime.now()
                if delta.total_seconds() <= 0:
                    print('\n', end='')
                    break
                print('\r正在等待系统开放,剩余' + str(int(delta.total_seconds())) + '秒')
                time.sleep(0.5)
    # 改签
    def changeTime(self,start,end,seat_num):
        status=self.getUserInfo()

        params={'token':self.token}
        # {'RESERVE': '预约', 'CHECK_IN': '履约中', 'AWAY': '暂离'}
        r=''
        id=status['data'][0]['id']
        if status['status']=='CHECK_IN':
            r=requests.get(self.stop_url,params,headers=self.headers).json()

        else:
            r=requests.get(self.cancel_url+'/'+str(id), params,headers=self.headers).json()
        print("*****改签座位*****")
        self.bookSeat(start,end,seat_num)

    # 通过作为编号获取作为id
    def getSeatIdByName(self,seat_num):
        params = {'token': self.token}
        date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        url=self.search_url+date

        r=requests.get(url,params=params,headers=self.headers).json()

        layout=r['data']['layout']
        for key in layout:
            if 'name' in layout[key] and layout[key]['name']==seat_num:
                return layout[key]['id']

def book(seatnum,uname,pwd):
    my = MySeat(uname, pwd)
    seat_id = my.getSeatIdByName(seatnum)
    # print(seat_id)
    # my.waitFor(True)
    r = my.bookSeat(int(9 * 60), int(22 * 60), seat_id)
if __name__ == '__main__':
    # 3664--74
    # 3638--73
    # 3639--75
    # 3665--76
    # start=float(input('请输入起始时间(8-22):'))
    # end=float(input('请输入起始时间(8-22):'))
    # 1--3680
    # 5--3113
    # seat_num='073'
    MySeat.waitFor(True)

    book('073','用户名','密码')
    # my.changeTime(int(9.5*60),int(14*60),seat_id)