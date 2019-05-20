#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import base64
import logging
import datetime

import tushare as ts
import pandas as pd

import log

#url: 
#  https://bingwong.org/2019/01/05/136.html
#  https://cnvar.cn/2019/02/16/cash-dividend-DCF-stock-selection/

def get_dividend():
    pro = ts.pro_api('c292290c8b403eeb48c1448f5f95c4ee868664cb3f63beee0de2d7ce')

    #获取最新的股票列表
    stock_tickers = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name')
    print stock_tickers.head()


if __name__ == '__main__':
    log.init_log('./log', level=logging.DEBUG)
    logging.info('start')

    get_dividend()

    logging.info('end')

