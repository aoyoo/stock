#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import base64
import logging
import datetime

from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import log

engine = create_engine('mysql://root:password@127.0.0.1/stock?charset=utf8')
DBSession = sessionmaker(bind=engine)
session = DBSession()

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class Stock(Base):
    # 表的名字:
    __tablename__ = 'history'

    # 表的结构:
    index = Column(Integer(), primary_key=True)
    code = Column(String())
    date = Column(String())
    open = Column(Float())
    close = Column(Float())
    volume = Column(Float())

def get_info(code, date = 0):
    # 初始化数据库连接:
    # 创建DBSession类型:
    #DBSession = sessionmaker(bind=engine)
    
    # 创建Session:
    #session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    stock = session.query(Stock).filter(Stock.code==code, Stock.date==date).all()
    if len(stock) == 0:
        #logging.info('get_info failed code:%r date:%r', code, date)
        raise Exception("code:%r date:%r empty", code, date)
    #logging.info('date:%r open:%r', stock[0].date, stock[0].open)
    # 关闭Session:
    #session.close()
    return stock[0]

if __name__ == '__main__':
    log.init_log('./log', level=logging.DEBUG)
    logging.info('start')

    get_info(code = '600000', date = '2018-03-01')

    logging.info('end')

