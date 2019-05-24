#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import base64
import logging
import datetime

import log
import stock_util
import execute_manager

from futu import RET_OK

from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer

mysql = create_engine('mysql://root:password@127.0.0.1/stock?charset=utf8')

today_day = datetime.datetime.now().strftime("%Y-%m-%d")
yestoday_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

history_start_day = '2006-01-01'
history_end_day = today_day

def update_histroy_to_sql(info):
    dtypedict = {
        'code': NVARCHAR(length=255)
    }

    info.to_sql(name='history', con=mysql, if_exists='append', dtype=dtypedict)

def update_rehab_to_sql(info):

    dtypedict = {
        'code': NVARCHAR(length=255)
    }

    #info.to_sql(name='rehab', con=mysql, if_exists='append')
    info.to_sql(name='rehab', con=mysql, if_exists='append', dtype=dtypedict)

if __name__ == '__main__':
    log.init_log('./log', level=logging.DEBUG)
    logging.debug('start')

    #util = stock_util.StockUtil()
    #util.init()
    
    execute_mgr = execute_manager.get_manager()
    
    hk_reits_codes =  [u'HK.00823', u'HK.87001', u'HK.00778', u'HK.02778', u'HK.00405', u'HK.00808']

    #for code in [u'HK.00823']:
    for code in hk_reits_codes:
        rehabs = stock_util.get_rehabs(code)
        if rehabs is None:
            continue
        for stock in rehabs:
            logging.debug(stock.to_string())
            historys = stock_util.get_historys(code, stock.ex_div_date_to_time_key())
            if historys is None:
                continue
            for hist in historys:
                logging.debug(hist.to_string())
                logging.info("stock:%r date:%r cash_div:%r eps:%r", code, stock.ex_div_date, stock.per_cash_div, stock.per_cash_div/hist.close)

    #logging.debug('end')
    #util.close()


