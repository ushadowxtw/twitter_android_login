#twitter Authorization algorithm
# -*- coding: utf-8 -*-
import urlutils
from urllib.parse import urlparse
from urllib.parse import quote
import base64
import hmac
from hashlib import sha1
import random
import time

def getAuthorization(remethod,url,oauth_token,oauth_token_secret):

    oauth_nonce = ''.join(random.choice('0123456789') for i in range(31))
    print (oauth_nonce)
    oauth_timestamp=int(time.time())

    datastr=constructSignatureBase(remethod,url,oauth_nonce,oauth_timestamp,oauth_token)
    signedstr=calculateSignature(datastr,oauth_token_secret,'Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys')

    # OAuth realm="http://api.twitter.com/", oauth_version="1.0", oauth_token="1182458614415421440-Q8DItbOuFfd5Q3NIAjROFyGYj1roh4", 
    # oauth_nonce="9527278473446947868915479494016", oauth_timestamp="1571102027", oauth_signature="QgyqrG0KwOirCUFmz3A4RoSAqP4%3D", oauth_consumer_key="3nVuSoBZnx6U4vzUxf5w", oauth_signature_method="HMAC-SHA1"
    retstr='OAuth realm="http://api.twitter.com/", oauth_version="1.0", oauth_token="'
    retstr+=oauth_token
    retstr+='", oauth_nonce="'
    retstr+=oauth_nonce
    retstr+='", oauth_timestamp="'
    retstr+=str(oauth_timestamp)
    retstr+='", oauth_signature="'
    retstr+=signedstr
    retstr+='", oauth_consumer_key="3nVuSoBZnx6U4vzUxf5w", oauth_signature_method="HMAC-SHA1"'
    return retstr

def constructSignatureBase(method,uristr,nonce,timestamp,oauthtoken):

    parsed_uri = urlparse(uristr)
    print (parsed_uri)
    baseUrl = parsed_uri.scheme + "://" + parsed_uri.netloc + parsed_uri.path
    print (baseUrl)
    requsetstr=parsed_uri.query
   # print (requsetstr)
    xmap=urlytils.get_requestmap(requsetstr)
  
    xmap['oauth_consumer_key']='3nVuSoBZnx6U4vzUxf5w'
    xmap['oauth_nonce']=nonce
    xmap['oauth_signature_method']='HMAC-SHA1'
    xmap['oauth_timestamp']=timestamp
    xmap['oauth_version']='1.0'
    xmap['oauth_token']=oauthtoken
    xmap=sorted(xmap.items(),key=lambda x:x[0])
    
    retdata=method
    retdata+='&'
    retdata+=quote(baseUrl,'')
    retdata+='&'
    retdata+=getEncodedQueryParams(xmap)
    print (retdata)
    return retdata

def getEncodedQueryParams(xmap):
    ret=''
    #print (xmap)
    for ki in xmap:
        print(ki)
        key=(ki[0])
        value=str(ki[1])
        print(key)
        print('value:'+value) 
        ukey=quote(key)
        uvalue=quote(value)
        ret+=quote(ukey)
        ret+='%3D'
        ret+=quote(uvalue)
        ret+='%26'
    ret=ret[:-3]
    print(ret)
    return ret
def calculateSignature(datastr,tokenSecret,ConsumerSecret):
    signkey=getSigningKey(tokenSecret,ConsumerSecret)
    hmac_code = hmac.new(str.encode(signkey,'utf8'), str.encode(datastr,'utf8'), sha1).digest()
    return quote(base64.b64encode(hmac_code).decode())




def getSigningKey(tokenSecret,ConsumerSecret):
    retstr=quote(ConsumerSecret)
    retstr+='&'
    retstr+=quote(tokenSecret)
    return retstr



         

        
    