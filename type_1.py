#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import base64
import logging
import datetime
import traceback

import MySQLdb

import tushare as ts

import log
import run 
import info

day_today = datetime.datetime.now().strftime("%Y-%m-%d")
day_yesteday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
day_100_ago = (datetime.datetime.now() - datetime.timedelta(days = 100)).strftime("%Y-%m-%d")

def get_date(delta):
    return (datetime.datetime.now() - datetime.timedelta(days = delta)).strftime("%Y-%m-%d")

def get_avg_volume(code, start_date, end_date):
    sql = "SELECT AVG(volume) FROM history WHERE code='%s' AND date>='%s' AND date<='%s' GROUP BY code;" % (code, start_date, end_date)
    #logging.info('TEST1:%r', sql)
    cursor.execute(sql)
    data = cursor.fetchone()
    #logging.info('code:%r start:%r end:%r avg_vol:%r', code, start_date, end_date, data[0])
    return data[0]

def get_last_trade_date():
    df = ts.trade_cal()
    df2 = df.set_index(['calendarDate'])
    for day in range(1,10):
        date = get_date(day)
        #logging.info('date:%r', date)
        is_open = df2.loc[date]['isOpen']
        if is_open == 1:
            #logging.info('date:%r delta:%r is_open', date, day)
            return date, day
    return None

class Type1:
    days = 0
    start_date = ''
    end_date = ''
    open = 0.0
    close = 0.0
    avg_vol = 0.0

def chose_one(code, last_trade_day, ta, tb, tc, td):
    try:
        a = Type1()
        b = Type1()
        c = Type1()
        d = Type1()
        e = Type1()
        
        e.days = 0
        e.start_date = last_trade_day
        e.open = info.get_info(code, e.start_date).open
        e.close = info.get_info(code, e.start_date).close
        e.avg_vol = get_avg_volume(code, e.start_date, e.start_date)
        
#        logging.info('code:%r e days:%r start_date:%r open:%r close:%r avg_vol:%r', \
#                code, e.days, e.start_date, e.open, e.close, e.avg_vol)

        d.days = td
        d.start_date = get_date(d.days)
        d.avg_vol = get_avg_volume(code, d.start_date, e.start_date)
#        logging.info('code:%r d days:%r start_date:%r open:%r close:%r avg_vol:%r', \
#                code, d.days, d.start_date, d.open, d.close, d.avg_vol)
        d.open = info.get_info(code, d.start_date).open
        d.close = info.get_info(code, d.start_date).close
        
        c.days = tc
        c.start_date = get_date(c.days + d.days)
        c.avg_vol = get_avg_volume(code, c.start_date, d.start_date)
#        logging.info('code:%r c days:%r start_date:%r open:%r close:%r avg_vol:%r', \
#                code, c.days, c.start_date, c.open, c.close, c.avg_vol)
        c.open = info.get_info(code, c.start_date).open
        c.close = info.get_info(code, c.start_date).close
        
        b.days = tb
        b.start_date = get_date(b.days + c.days + d.days)
        b.avg_vol = get_avg_volume(code, b.start_date, c.start_date)
#        logging.info('code:%r b days:%r start_date:%r open:%r close:%r avg_vol:%r', \
#                code, b.days, b.start_date, b.open, b.close, b.avg_vol)
        b.open = info.get_info(code, b.start_date).open
        b.close = info.get_info(code, b.start_date).close
        
        a.days = ta
        a.start_date = get_date(a.days + b.days + c.days + d.days)
        a.avg_vol = get_avg_volume(code, a.start_date, b.start_date)
#        logging.info('code:%r a days:%r start_date:%r open:%r close:%r avg_vol:%r', \
#                code, a.days, a.start_date, a.open, a.close, a.avg_vol)
        a.open = info.get_info(code, a.start_date).open
        a.close = info.get_info(code, a.start_date).close
        
        logging.info('ALL_DATA code:%r A:%r B:%r C:%r D:%r a.close:%r b.close:%r c.close:%r d.close:%r', \
                code, a.start_date, b.start_date, c.start_date, d.start_date, \
                a.close, b.close, c.close, d.close)
#        logging.info('ALL_DATA code:%r b.close:%r a.open*0.7:%r c.close:%r b.open*1.2:%r', \
#                code, b.close, a.open*0.7, c.close, b.open*1.2)
        if b.close < a.open * 0.7 and c.close > b.open * 1.2:
            #and tc > tb*0.8 and tc < tb *1.2:
            logging.info('GET code:%r A:%r B:%r C:%r D:%r a.close:%r b.close:%r c.close:%r d.close:%r',\
                code, a.start_date, b.start_date, c.start_date, d.start_date, \
                a.close, b.close, c.close, d.close)
    except Exception as e:
        #logging.info('exception:%s', e)
        #print traceback.format_exc()
        pass

def get_type_1():
    print 'day_today:', day_today

    global db
    db = MySQLdb.connect("127.0.0.1","root","password","stock" )
    global cursor
    cursor = db.cursor()

    all_count = 0
    all_code = run.get_all_code()
    for code in all_code:
        #avg_vol_100 = get_avg_volume(code, get_date(100), get_date(1))
        #logging.info('code:%r avg_vol_100:%r', code, avg_vol_100)
        count = 0

        last_trade_day, before_today_days = get_last_trade_date()
        for td in range(1, 30):
            if td < before_today_days:
                continue
            for tc in range(5, 20):
                for tb in range(5, 20):
                    for ta in range(5, 20):
                        all_count += 1
                        count += 1
                        logging.info('calc %r:%r:%r:%r count:%r total:%r', ta, tb, tc, td, count, all_count)
                        chose_one(code, last_trade_day, ta, tb, tc, td)
    db.close()

if __name__ == '__main__':
    log.init_log('./type_1', level=logging.DEBUG)
    logging.info('start')

    logging.info('day_start:%r day_end:%r', day_100_ago, day_today)

    get_type_1()

    logging.info('end')

