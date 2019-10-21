# -*- coding: utf-8 -*-
import random
def getTraceId():
    traceid = ''.join(random.choice('0123456789abcdf') for i in range(16))
    return traceid