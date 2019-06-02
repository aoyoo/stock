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
    logging.info('start')

    util = stock_util.StockUtil()
    util.init()
    
    execute_mgr = execute_manager.get_manager()
    
    hk_reits_codes =  [u'HK.00823', u'HK.87001', u'HK.00778', u'HK.02778', u'HK.00405', u'HK.00808']

    for code in hk_reits_codes:
    #for code in [u'HK.00823']:
        rehab = execute_mgr.execute(util.get_rehab, code)
        if rehab is None:
            continue
        rehab['code'] = code
        for i in range(len(rehab) - 1,len(rehab)):
            ex_div_date = rehab.iloc[i].ex_div_date
            per_cash_div = rehab.iloc[i].per_cash_div
            logging.info("code:%s get ex_div_date:%s per_cash_div:%s", code, ex_div_date, per_cash_div)
        update_rehab_to_sql(rehab)

        page = None
        count = 0
        while True:
            #res = util.request_history_kline(code, yestoday_day, today_day, page)
            res = execute_mgr.execute(util.request_history_kline, code, history_start_day, today_day, page)
            if res[0] != RET_OK:
                logging.error("code:%s get_history fail:%s", code, res[1])
                break

            count += 1
            update_histroy_to_sql(res[1])

            if res[2] != None:
                logging.info("code:%s get_history has page:%d", code, count)
                page = res[2]
                continue
            else:
                break
            
#def get_history(self, code, day):

    logging.info('end')
    util.close()


