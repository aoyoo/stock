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
import info

day_today = datetime.datetime.now().strftime("%Y-%m-%d")
day_yesteday = (datetime.datetime.now() - datetime.timedelta(days = 100)).strftime("%Y-%m-%d")
day_100_ago = (datetime.datetime.now() - datetime.timedelta(days = 100)).strftime("%Y-%m-%d")

def get_date(delta):
    return (datetime.datetime.now() - datetime.timedelta(days = delta)).strftime("%Y-%m-%d")

def get_avg_volume(code, start_day, end_day):
#    "SELECT AVG(volume) FROM history WHERE code='600000' AND date>'2018-01-01'     AND date<'2018-03-05' GROUP BY code;"
    sql = "SELECT AVG(volume) FROM history WHERE code='%s' AND date>'%s' AND date<'%s' GROUP BY code;" % (code, start_day, end_day)
    logging.info('TEST1:%r', sql)
    cursor.execute(sql)
    data = cursor.fetchone()
    logging.info('TEST1:%r', data)

def get_last_trade_date():
    df = ts.trade_cal()
    df2 = df.set_index(['calendarDate'])
    for day in range(1,10):
        date = get_date(day)
        logging.info('date:%r', date)
        is_open = df2.loc[date]['isOpen']
        if is_open == 1:
            #logging.info('date:%r is_open', date)
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
        
        d.days = td
        d.start_date = get_date(d.days)
        d.open = info.get_info(code, d.start_date).open
        d.close = info.get_info(code, d.start_date).close
        d.avg_vol = get_avg_volume(code, d.start_date, e.start_date)
        
        c.days = tc
        c.start_date = get_date(c.days + d.days)
        c.open = info.get_info(code, c.start_date).open
        c.close = info.get_info(code, c.start_date).close
        c.avg_vol = get_avg_volume(code, c.start_date, d.start_date)
        
        b.days = tb
        b.start_date = get_date(b.days + c.days + d.days)
        b.open = info.get_info(code, b.start_date).open
        b.close = info.get_info(code, b.start_date).close
        b.avg_vol = get_avg_volume(code, b.start_date, c.start_date)
        
        a.days = ta
        a.start_date = get_date(a.days + b.days + c.days + d.days)
        a.open = info.get_info(code, a.start_date).open
        a.close = info.get_info(code, a.start_date).close
        a.avg_vol = get_avg_volume(code, a.start_date, b.start_date)
        
        logging.info('TEST code:%r A:%r B:%r C:%r D:%r a.close:%r b.close:%r c.close:%r d.close:%r', \
                code, a.start_date, b.start_date, c.start_date, d.start_date, \
                a.close, b.close, c.close, d.close)
        if b.close < a.open * 0.7 and c.close > b.open * 1.2 and tc > tb*0.8 and tc < tb *1.2:
            logging.info('GET code:%r A:%r B:%r C:%r D:%r a.close:%r b.close:%r c.close:%r d.close:%r',\
                code, a.start_date, b.start_date, c.start_date, d.start_date, \
                a.close, b.close, c.close, d.close)
    except Exception as e:
        #logging.info('exception:%s', e)
        #print traceback.format_exc()
        pass

def get_type_1():
    print 'day_today:', day_today
    print 'day_yesteday:', day_yesteday

    code = '600000'

    global db
    db = MySQLdb.connect("127.0.0.1","root","password","stock" )
    global cursor
    cursor = db.cursor()

    avg_vol_100 = get_avg_volume(code, get_date(100), get_date(1))
    logging.info('code:%r avg_vol_100:%r', code, avg_vol_100)
    count = 0
    return

    last_trade_day, before_today_days = get_last_trade_date()
    for td in range(1, 11):
        if td < before_today_days:
            continue
        for tc in range(1, 11):
            for tb in range(1, 11):
                for ta in range(1, 11):
                    count += 1
                    logging.info('calc %r:%r:%r:%r total:%r', ta, tb, tc, td, count)
                    chose_one(code, last_trade_day, ta, tb, tc, td)
                    #if count >= 10:
                    #    break
    db.close()

if __name__ == '__main__':
    log.init_log('./log', level=logging.DEBUG)
    logging.info('start')

    logging.info('day_start:%r day_end:%r', day_100_ago, day_today)

    get_type_1()

    logging.info('end')

