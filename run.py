#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import base64
import logging
import datetime

import tushare as ts
from sqlalchemy import create_engine

import log

mysql = create_engine('mysql://root:password@127.0.0.1/stock?charset=utf8')

day_today = datetime.datetime.now().strftime("%Y-%m-%d")
day_100_ago = (datetime.datetime.now() - datetime.timedelta(days = 100)).strftime("%Y-%m-%d")

def get_all_code():
    all_code = []
    today_all = ts.get_today_all()
    for index,value in today_all.code.iteritems():
        #print index,value
        all_code.append(value)
    logging.info('all code num:%d', len(all_code))
    return all_code

def update_data(code):
    df = ts.get_k_data(code = code, start = day_100_ago, end = day_today)
    df.to_sql('history', mysql, if_exists='append')
    logging.info('update_data:%r', code)

if __name__ == '__main__':
    log.init_log('./log', level=logging.DEBUG)
    logging.info('start')

    logging.info('day_start:%r day_end:%r', day_100_ago, day_today)

    all_code = get_all_code()
    for code in all_code:
        update_data(code)

    logging.info('end')

