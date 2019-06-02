#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import base64
import logging
import datetime

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer

from futu import RET_OK

import log
import stock_util
import execute_manager

mysql = create_engine('mysql://root:password@127.0.0.1/stock?charset=utf8')

today_day = datetime.datetime.now().strftime("%Y-%m-%d")
yestoday_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

history_start_day = '2006-01-01'
history_end_day = today_day

def status(x) : 
    return pd.Series([x.count(),x.min(),x.idxmin(),x.quantile(.25),x.median(),
                      x.quantile(.75),x.mean(),x.max(),x.idxmax(),x.mad(),x.var(),
                      x.std(),x.skew(),x.kurt()],index=['总数','最小值','最小值位置','25%分位数',
                    '中位数','75%分位数','均值','最大值','最大值位数','平均绝对偏差','方差','标准差','偏度','峰度'])

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

def date_to_year(date_str):
    #date_str: '2019-00-01'
    return date_str[0:4]

if __name__ == '__main__':
    log.init_log('./log', level=logging.DEBUG)
    logging.debug('start')

    #util = stock_util.StockUtil()
    #util.init()
    
    execute_mgr = execute_manager.get_manager()
    
    hk_reits_codes =  [u'HK.00823', u'HK.87001', u'HK.00778', u'HK.02778', u'HK.00405', u'HK.00808']

    df = pd.DataFrame(columns=['code', 'date', 'dividend_ratio', 'price'])
    #for code in [u'HK.00823']:
    for code in hk_reits_codes:
        logging.debug('*' * 20 + code + '*' * 20)
        rehabs = stock_util.get_rehabs(code)
        if rehabs is None:
            continue
        for stock in rehabs:
            logging.debug(stock.to_string())
            if not stock.is_legal():
                continue
            historys = stock_util.get_historys(code, stock.ex_div_date_to_time_key())
            if historys is None:
                continue
            for hist in historys:
                logging.debug(hist.to_string())
                if not hist.is_legal():
                    continue
                #logging.info("stock:%r date:%r cash_div:%r eps:%r", code, stock.ex_div_date, stock.per_cash_div, stock.per_cash_div/hist.close)
                df.loc[df.shape[0]] = {'code': code, 'date': stock.ex_div_date, 'dividend_ratio': stock.per_cash_div/hist.close, 'price': hist.close}

    #print df
    #print '-' * 40

    for code in hk_reits_codes:
        filtered = df.loc[(df['code'] == code) & (df['date'] > '2015-00-00')]
        filtered['year'] = filtered['date'].map(date_to_year)
        #print filtered
        grouped = filtered['dividend_ratio'].groupby(filtered['year'])
        print filtered.tail(1)
        #print grouped.mean()
        print grouped.sum()
    #logging.debug('end')
    #util.close()


