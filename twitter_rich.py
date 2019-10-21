# -*- coding: utf-8 -*-
import sys
import time
import os
import json
import urllib.request
import ssl
import twitter_auth
import gzip
import publicfun
Host_api = "https://api.twitter.com"
def gzdecode(data) :
    return gzip.decompress(data)
def get_loginuserinfo(useragent,deviceid,clientuuid,oauth_token,oauth_token_secret):
    Uripara = Host_api
    Uripara += "/1.1/account/verify_credentials.json?include_user_entities=true&include_profile_interstitial_type=true&include_nsfw_user_flag=true"
#remethod,url,oauth_token,oauth_token_secret
    Authorization=twitter_auth.getAuthorization('GET',Uripara,oauth_token,oauth_token_secret)
    webheader = {
        'Cache-Control': 'no-store',
        'X-B3-TraceId': publicfun.getTraceId(),
        'User-Agent': useragent,
        'Accept-Encoding': 'gzip, deflate',
        'Timezone': 'Asia/Shanghai',
        'X-Twitter-Client': 'TwitterAndroid',
        'X-Twitter-Client-Language': 'zh-CN',
        'X-Twitter-Client-DeviceID': deviceid,
        'X-Twitter-API-Version': '5',
        'X-Twitter-Client-Version': '6.43.0',
        'X-Twitter-Active-User': 'yes',
        'X-Client-UUID': clientuuid,
        'Authorization': Authorization,
        'Accept-Language': 'zh-CN',
        'Host': 'api.twitter.com',
        'Connection': 'Keep-Alive'
    }
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url=Uripara, headers=webheader)
    try:
        webPage = urllib.request.urlopen(req,context=context)
    except Exception as e:
        print (e)
        return ''
        
    data =gzdecode( webPage.read()).decode('utf-8')
    print(data)
    y = json.loads(data)

    return y["id"]

def get_blocklist(useragent,deviceid,clientuuid,oauth_token,oauth_token_secret,userid):
    Uripara = Host_api
    Uripara += '/1.1/blocks/list.json?skip_status=true&include_user_entities=true&include_profile_interstitial_type=true&user_id='
    Uripara +=str(userid)
    Uripara+='&cursor=-1'
    Authorization=twitter_auth.getAuthorization('GET',Uripara,oauth_token,oauth_token_secret)
    webheader = {
        'Cache-Control': 'no-store',
        'X-B3-TraceId': publicfun.getTraceId(),
        'User-Agent': useragent,
        'Accept-Encoding': 'gzip, deflate',
        'Timezone': 'Asia/Shanghai',
        'X-Twitter-Client': 'TwitterAndroid',
        'X-Twitter-Client-Language': 'zh-CN',
        'X-Twitter-Client-DeviceID': deviceid,
        'X-Twitter-API-Version': '5',
        'X-Twitter-Client-Version': '6.43.0',
        'X-Twitter-Active-User': 'no',
        'X-Client-UUID': clientuuid,
        'Authorization': Authorization,
        'Accept-Language': 'zh-CN',
        'Host': 'api.twitter.com',
        'Connection': 'Keep-Alive'
    }
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url=Uripara, headers=webheader)
    try:
        urllib.request.urlopen(req,context=context)
    except Exception as e:
        print (e)
        return -1
    return 0


def get_blockidst(useragent,deviceid,clientuuid,oauth_token,oauth_token_secret,userid):
    Uripara = Host_api
    Uripara += '/1.1/blocks/ids.json?cursor=-1&skip_status=true&user_id='
    Uripara +=str(userid)
    Authorization=twitter_auth.getAuthorization('GET',Uripara,oauth_token,oauth_token_secret)
    webheader = {
        'Cache-Control': 'no-store',
        'X-B3-TraceId': publicfun.getTraceId(),
        'User-Agent': useragent,
        'Accept-Encoding': 'gzip, deflate',
        'Timezone': 'Asia/Shanghai',
        'X-Twitter-Client': 'TwitterAndroid',
        'X-Twitter-Client-Language': 'zh-CN',
        'X-Twitter-Client-DeviceID': deviceid,
        'X-Twitter-API-Version': '5',
        'X-Twitter-Client-Version': '6.43.0',
        'X-Twitter-Active-User': 'no',
        'X-Client-UUID': clientuuid,
        'Authorization': Authorization,
        'Accept-Language': 'zh-CN',
        'Host': 'api.twitter.com',
        'Connection': 'Keep-Alive'
    }
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url=Uripara, headers=webheader)
    try:
        urllib.request.urlopen(req,context=context)
    except Exception as e:
        print (e)
        return -1
    return 0

        