import requests
from lxml import etree
import urllib
import urllib3
import time
import re
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
urllib3.disable_warnings() # 禁用安全请求警告

class Git():
    def __init__(self,username,password):
        self.headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }
        self.loginurl='https://github.com/login'
        self.posturl='https://github.com/session'
        self.username=username
        self.password=password
        '''
        会话对象让你能够跨请求保持某些参数。它也会在同一个 Session 实例发出的所有请求之间保持 cookie， 
        期间使用 urllib3 的 connection pooling 功能。所以如果你向同一主机发送多个请求，
        底层的 TCP 连接将会被重用，从而带来显著的性能提升。
        '''
        self.session=requests.Session()
        # self.session.cookies = cookielib.LWPCookieJar(filename='github_cookie')
    def get_token(self):
        response=self.session.get(self.loginurl,headers=self.headers,verify=False)
        html=etree.HTML(response.text)
        utf8=html.xpath('//form/input[@name="utf8"]/@value')[0]
        token=html.xpath('//form/input[@name="authenticity_token"]/@value')[0]
        # token = re.findall('<input name="authenticity_token" type="hidden" value="(.*?)" />', r.content, re.S)
        return {
            'token':token,
            'utf8':utf8
        }
    def login(self):
        token=self.get_token()
        params={
            'commit': 'Sign in',
            'utf8': token['utf8'],
            'authenticity_token':token['token'],
            'login':self.username,
            'password':self.password
        }
        response=self.session.post(self.posturl,data=params,headers=self.headers)
        if response.status_code==200:
            print('Success')
            return True
        else:
            raise Exception('Fail')
    # 获取url中的参数
    def getUrlParams(self,url):
        query = urlparse(url).query
        return dict([(k, v[0]) for k, v in urllib.parse.parse_qs(query).items()])
if __name__=='__main__':
    git=Git('用户名','密码')
    git.login()