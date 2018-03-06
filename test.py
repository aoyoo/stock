#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import base64
import logging
import datetime

import tushare as ts
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer

import log


mysql = create_engine('mysql://root:password@127.0.0.1/stock?charset=utf8')

day_today = datetime.datetime.now().strftime("%Y-%m-%d")
#print type(day_today), day_today
day_10_ago = (datetime.datetime.now() - datetime.timedelta(days = 10)).strftime("%Y-%m-%d")
day_100_ago = (datetime.datetime.now() - datetime.timedelta(days = 100)).strftime("%Y-%m-%d")

df = ts.trade_cal()

#'calendarDate', 'isOpen'

df2 = df.set_index(['calendarDate'])
#print df2.head()
#print df2.index
#for i in df2.index:
#    if i == u'2018-12-31':
#        print 'xxxxxxxxxxxxx'
#print df2[u'2018-12-31']
print type(df2.loc[u'2018-03-05']), df2.loc[u'2018-03-05']
is_open = df2.loc[u'2018-03-05']['isOpen']
print 'is_open:', is_open, is_open == 1, type(is_open)

#[day_today]
#print type(df)

