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

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class Stock(Base):
    # 表的名字:
    __tablename__ = 'history'

    # 表的结构:
    index = Column(Integer(), primary_key=True)
    date = Column(String())
    open = Column(Float())
    close = Column(Float())
    code = Column(String())

def get_info(code):
    # 初始化数据库连接:
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    
    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    stock = session.query(Stock).filter(Stock.code==code, Stock.date=='2018-01-30').all()
    # 打印类型和对象的name属性:
    for s in stock:
        print 'date:', s.date, 'open:', s.open
    # 关闭Session:
    session.close()

if __name__ == '__main__':
    log.init_log('./log', level=logging.DEBUG)
    logging.info('start')

    get_info('600000')

    logging.info('end')

