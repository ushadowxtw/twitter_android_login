# -*- coding: utf-8 -*-
from urllib.parse import quote
def get_requestmap(requeststr):
    xmap={}
    list=str.split(requeststr,'&', -1)
    for kv in list:
     #   print(kv)
        lk=str.split(kv,'=', -1)
        if len(lk)==2:
            key=quote(lk[0])
            value=quote(lk[1])
            xmap[key]=value
    return xmap
