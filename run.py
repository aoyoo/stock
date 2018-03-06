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
day_10_ago = (datetime.datetime.now() - datetime.timedelta(days = 10)).strftime("%Y-%m-%d")
day_100_ago = (datetime.datetime.now() - datetime.timedelta(days = 100)).strftime("%Y-%m-%d")

index_flag = False

def get_all_code():
    all_code = []
    #today_all = ts.get_today_all()
    #for index,value in today_all.code.iteritems():
    #    #print index,value
    #    all_code.append(value)
    #logging.info('all code num:%d', len(all_code))
    for c in ts.get_stock_basics().index:
        all_code.append(c)
    return all_code

def update_data(code):

    dtypedict = {
        'date': NVARCHAR(length=255),
        'code': NVARCHAR(length=255)
    }

    df = ts.get_k_data(code = code, start = day_100_ago, end = day_today)
    df.to_sql(name='history', con=mysql, if_exists='append', dtype=dtypedict)

    global index_flag
    if not index_flag:
        with mysql.connect() as con:
            con.execute('ALTER TABLE `history` ADD INDEX `index_code`(`code`);')
            con.execute('ALTER TABLE `history` ADD INDEX `index_date`(`date`);')
        index_flag = True

    logging.info('update_data:%r', code)

if __name__ == '__main__':
    log.init_log('./log', level=logging.DEBUG)
    logging.info('start')

    logging.info('day_start:%r day_end:%r', day_100_ago, day_today)

    all_code = get_all_code()
    for code in all_code:
        update_data(code)
#    update_data(u'600000')

    logging.info('end')

