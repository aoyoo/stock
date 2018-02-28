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

def get_type_1():
    ta = 10
    tb = 10
    tc = 10
    td = 10

    code = '600000'

def get_info(code, date):
    sqlalchemy
    pass

if __name__ == '__main__':
    log.init_log('./log', level=logging.DEBUG)
    logging.info('start')

    logging.info('day_start:%r day_end:%r', day_100_ago, day_today)

    get_type_1()

    logging.info('end')

