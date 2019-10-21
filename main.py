import sys
import time
import os
import json
# -*- coding: utf-8 -*-
import urllib.request
import ssl
from io import StringIO
import twitter_auth
import twitter_rich
import gzip 
import uuid
import publicfun
import names
import base64
Host_api = "https://api.twitter.com"
g_oauth_token=''
g_oauth_token_secret=''
g_user_id=''
g_kdt=''
g_uuid=''
g_deviceid=''
g_useragent=''
g_login_success=False
#解压gzip
def gzdecode(data) :
    return gzip.decompress(data)


def out_error():
    print('TWitter ERROR')
    sys.exit(0)
#获取 guest_token
def get_guest_token():
    # POST  HTTP/1.1
    Uripara = Host_api
    Uripara += "/1.1/guest/activate.json"
    webheader = {
        'Geolocation': '0',
        'X-B3-TraceId': publicfun.getTraceId(),
        'User-Agent': g_useragent,
        'Accept-Encoding': 'gzip, deflate',
        'X-Twitter-Client': 'TwitterAndroid',
        'X-Twitter-Client-Language': 'zh-CN',
        'X-Twitter-Client-DeviceID': g_deviceid,
        'X-Twitter-API-Version': '5',
        'X-Twitter-Polling': 'True',
        'X-Twitter-Client-Version': '6.43.0',
        'X-Twitter-Active-User': 'no',
        'X-Client-UUID': g_uuid,
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F',
        'Accept-Language': 'zh-CN',
        'Host': 'api.twitter.com',
        'Connection': 'Keep-Alive'
    }
    print(Uripara)
    print(webheader)
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url=Uripara, headers=webheader,data=None,method='POST')
    try:
        webPage = urllib.request.urlopen(req,context=context)
    except Exception as e:
        print (e)
        return ''
        
    data =gzdecode( webPage.read()).decode('utf-8')
    print(data)
    y = json.loads(data)

    return y["guest_token"]
#{"guest_token":"1182940238265475072"}


#登录
def  twitter_login(guest_token,userstr,passwd):
    dataStr='x_auth_identifier='
    dataStr+=userstr
    dataStr+='&x_auth_password='
    dataStr+=passwd
    dataStr+='&send_error_codes=true&x_auth_login_verification=1&x_auth_login_challenge=1&x_auth_country_code=CN='
    dataStrLen=len(dataStr)
    Uripara = Host_api
    Uripara += "/auth/1/xauth_password.json"
    webheader = {
        'Cache-Control': 'no-store',
        'X-B3-TraceId': publicfun.getTraceId(),
        'User-Agent':g_useragent ,
        'Accept-Encoding': 'gzip, deflate',
        'Timezone': 'Asia/Shanghai',        
        'X-Twitter-Client': 'TwitterAndroid',
        'X-Twitter-Client-Language': 'zh-CN',
        'X-Twitter-Client-DeviceID': g_deviceid,
        'X-Twitter-API-Version': '5',
        'X-Twitter-Polling': 'True',
        'X-Twitter-Client-Version': '6.43.0',
        'X-Twitter-Active-User': 'yes',
        'X-Guest-Token': guest_token,
        'X-Client-UUID': g_uuid,
        'Accept': 'application/json',
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F',
        'Accept-Language': 'zh-CN',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': dataStrLen,
        'Host': 'api.twitter.com',
        'Connection': 'Keep-Alive'
    }

    context = ssl._create_unverified_context()
    req = urllib.request.Request(Uripara, headers=webheader, data= bytes(dataStr, encoding = "utf8"))
    try:
        webPage = urllib.request.urlopen(req,context=context)
    except Exception as e:
        print (e)
        return -1
    data =gzdecode( webPage.read()).decode('utf-8')
    print(data)
    retcode=webPage.getcode()
    print(retcode)
    global g_oauth_token
    global g_oauth_token_secret
    global g_user_id
    global g_kdt
    global g_login_success
    if retcode==200:
        y = json.loads(data)
        g_oauth_token=y["oauth_token"]
        g_oauth_token_secret=y["oauth_token_secret"]
        g_user_id=y["user_id"]
        g_kdt=y["kdt"]
        g_login_success=True
        print('g_login_success ：TRUE')
        return 0
    return -1
#
def write_logininfo():
    wdata='{"oauth_token":"'
    wdata+=g_oauth_token
    wdata+='","oauth_token_secret":"'
    wdata+=g_oauth_token_secret
    wdata+='","user_id":"'
    wdata+=str(g_user_id)
    wdata+='","uuid":"'
    wdata+=g_uuid
    wdata+='","useragent":"'
    wdata+= base64.b64encode(bytes(g_useragent, encoding = "utf8")).decode()  
    wdata+='","deviceid":"'
    wdata+=g_deviceid
    wdata+='","kdt":"'
    wdata+=g_kdt
    wdata+='"}'
    with open('login_data.txt','w') as f:    #设置文件对象
        f.write(wdata)                 #将字符串写入文件中

def read_logininfo():
    global g_oauth_token
    global g_oauth_token_secret
    global g_user_id
    global g_kdt
    global g_uuid
    global g_useragent
    global g_deviceid
    try:
        f = open("login_data.txt","r")   #设置文件对象
        str = f.read()     #将txt文件的所有内容读入到字符串str中
        f.close()   #将文件关闭        
        y = json.loads(str)
        g_oauth_token=y["oauth_token"]
        g_oauth_token_secret=y["oauth_token_secret"]
        g_user_id=y["user_id"]
        g_kdt=y["kdt"]
        g_uuid=y["uuid"]
        g_useragent=y["useragent"]
        g_useragent=base64.decodebytes(bytes(g_useragent, encoding = "utf8")).decode() 
        g_deviceid=y["deviceid"]
    except Exception as e:
        print (e)
        return -1
    return 0
def login_go():
    global g_uuid
    global g_useragent
    global g_deviceid
 #登录
    user='phonenumber'
    passwd='xxxxxxxx'
    g_uuid=str( uuid.uuid1())
    print(g_uuid)
    g_useragent='TwitterAndroid/6.43.0 (7110066-r-934) PLK-110/6.0 (HUAWEI;PLK-110;HONOR;PLK-110;0;;1)'
    g_deviceid='16e98f793f9f35et'

    guest_token=get_guest_token()
    if guest_token=='':
        print('Get guest_token is error')
        return 
    print('get guest_token is:'+guest_token)        
    ret=twitter_login(guest_token,user,passwd)
    if ret!=0:
        print('twitter_login is error')
        return -1
    else:
        #记录登录的信息
        print('write logininfo')
        write_logininfo()
    print('g_oauth_token:'+g_oauth_token)
    print('g_oauth_token_secret'+g_oauth_token_secret)
    print('g_kdt'+g_kdt)
    print('g_user_id'+str(g_user_id))

    return 0
def rich_go():
    mid=twitter_rich.get_loginuserinfo(g_useragent,g_deviceid,g_uuid,g_oauth_token,g_oauth_token_secret)#(useragent,deviceid,clientuuid,oauth_token,oauth_token_secret):
    if mid=='':
        print('Get user id is error')
        return 
    print('get_blocklist run')       
    twitter_rich.get_blocklist(g_useragent,g_deviceid,g_uuid,g_oauth_token,g_oauth_token_secret,mid) 
    twitter_rich.get_blockidst(g_useragent,g_deviceid,g_uuid,g_oauth_token,g_oauth_token_secret,mid)
    print('rich_go end')

def runwork():
    if read_logininfo()!=0:
        if login_go()!=0:
            print('login_go error!')
            return
        rich_go()
        return
    #rich_go()
    #爬取
    time.sleep(1)
    print('goto main work')
    return

def main():
    runwork()

if __name__ == '__main__':
	main()

