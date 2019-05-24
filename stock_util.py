#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

from sqlalchemy import Column, Float, Integer, String, create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from futu import *

import log

engine = create_engine('mysql://root:password@127.0.0.1/stock?charset=utf8')
DBSession = sessionmaker(bind=engine)
session = DBSession()

class StockUtil:
  ctx = None

  def init(self):
    SysConfig.set_all_thread_daemon
    self.ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    logging.info("init QuoteContext success")

  def close(self):
    if self.ctx != None:
      self.ctx.close()
 
  def get_all_hk_code(self):
    res = self.ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK)
    if res[0] != RET_OK:
        logging.error("get_stock_basicinfo fail:%s", res[1])
        return None

    content = res[1]
    print content
    logging.info("get HK stock size:%d", content.code.size)
    return content.code

#
#get_rehab
#get_rehab(self, code)
#获取给定股票的复权因子
#
#Parameters:	code – 需要查询的股票代码.
#Returns:	(ret, data)
#ret != RET_OK 返回错误字符串
#ret == RET_OK 返回pd dataframe数据
#
#参数	类型	说明
#ex_div_date	str	除权除息日
#split_ratio	float	拆合股比例（该字段为比例字段，展示为小数表示）例如，对于5股合1股为5.0，对于1股拆5股为0.2
#per_cash_div	float	每股派现
#per_share_div_ratio	float	每股送股比例（该字段为比例字段，展示为小数表示）
#per_share_trans_ratio	float	每股转增股比例（该字段为比例字段，展示为小数表示）
#allotment_ratio	float	每股配股比例（该字段为比例字段，展示为小数表示）

  def get_rehab(self, code):
    res = self.ctx.get_rehab(code)
    if res[0] != RET_OK:
        logging.error("get_rehab fail:%s", res[1])
        return None

    return res[1]

#"""
#get_market_snapshot(self, code_list)
#"earning_per_share"
#参数	类型	说明
#code	str	股票代码
#update_time	str	更新时间(yyyy-MM-dd HH:mm:ss)（港股A股默认是北京时间）
#last_price	float	最新价格
#open_price	float	今日开盘价
#high_price	float	最高价格
#low_price	float	最低价格
#prev_close_price	float	昨收盘价格
#volume	int	成交数量
#turnover	float	成交金额
#turnover_rate	float	换手率（该字段为百分比字段，默认不展示%）
#suspension	bool	是否停牌(True表示停牌)
#listing_date	str	上市日期 (yyyy-MM-dd)
#equity_valid	bool	是否正股（为true时以下正股相关字段才有合法数值）
#issued_shares	int	发行股本
#total_market_val	float	总市值
#net_asset	int	资产净值
#net_profit	int	净利润
#earning_per_share	float	每股盈利
#outstanding_shares	int	流通股本
#net_asset_per_share	float	每股净资产
#"""
  def get_market_snapshot(self, code):
    pass

#request_history_kline(self, code, start=None, end=None, ktype=KLType.K_DAY, autype=AuType.QFQ, fields=[KL_FIELD.ALL], max_count=1000, page_req_key=None)
#获取k线，不需要事先下载k线数据。
#
#Parameters:	
#code – 股票代码
#start – 开始时间，例如‘2017-06-20’
#end –
#结束时间，例如‘2017-07-20’。 start和end的组合如下：
#
#start类型	end类型	说明
#str	str	start和end分别为指定的日期
#None	str	start为end往前365天
#str	None	end为start往后365天
#None	None	end为当前日期，start为end往前365天
#ktype – k线类型， 参见 KLType 定义
#autype – 复权类型, 参见 AuType 定义
#fields – 需返回的字段列表，参见 KL_FIELD 定义 KL_FIELD.ALL KL_FIELD.OPEN ....
#max_count – 本次请求最大返回的数据点个数，传None表示返回start和end之间所有的数据。
#page_req_key – 分页请求的key。如果start和end之间的数据点多于max_count，那么后续请求时，要传入上次调用返回的page_req_key。初始请求时应该传None。

#Returns:	
#(ret, data, page_req_key)
#ret != RET_OK 返回错误字符串
#ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下。
#              page_req_key在分页请求时（即max_count>0）可能返回，并且需要在后续的请求中传入。如果没有更多数据，page_req_key返回None。

#参数	类型	说明
#code	str	股票代码
#time_key	str	k线时间（港股A股默认是北京时间）
#open	float	开盘价
#close	float	收盘价
#high	float	最高价
#low	float	最低价
#pe_ratio	float	市盈率（该字段为比例字段，默认不展示%）
#turnover_rate	float	换手率
#volume	int	成交量
#turnover	float	成交额
#change_rate	float	涨跌幅
#last_close	float	昨收价

#Example:	
#from futu import *
#ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start='2017-06-20', end='2018-06-22', max_count=50) #请求开头50个数据
#print(ret, data)
#ret, data, page_req_key = quote_ctx.request_history_kline('HK.00700', start='2017-06-20', end='2018-06-22', max_count=50, page_req_key=page_req_key) #请求下50个数据
#print(ret, data)
#quote_ctx.close()

  def request_history_kline(self, code, start, end, page_req_key):
    return self.ctx.request_history_kline(code=code, start=start, end=end, ktype=KLType.K_DAY, autype=AuType.QFQ, fields=[KL_FIELD.ALL], max_count=1000, page_req_key=page_req_key)

  def get_history(self, code, start=None, end=None, max_count=1000, page_req_key=None):
    res = self.ctx.request_history_kline(code, day, day)
    if res[0] != RET_OK:
        logging.error("request_history_kline fail:%s", res[1])
        return None
    return res[1]

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class Rehab(Base):
  # 表的名字:
  __tablename__ = 'rehab'

  # 表的结构:
  index = Column(Integer(), primary_key=True)
  code = Column(String())
  ex_div_date = Column(String())
  per_cash_div = Column(Float())

  def to_string(self):
    return "code:" + self.code + " ex_div_date:" + self.ex_div_date + " per_cash_div:" + str(self.per_cash_div)

  def ex_div_date_to_time_key(self):
    return self.ex_div_date + " 00:00:00"

class History(Base):
  __tablename__ = 'history'
  
  index = Column(Integer(), primary_key=True)
  code = Column(String())
  time_key = Column(String())
  open = Column(Float())
  close = Column(Float())

  def to_string(self):
    return "code:" + self.code + " time_key:" + self.time_key + " open:" + str(self.open)


def get_rehabs(code):
  # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
  stocks = session.query(Rehab).filter(Rehab.code==code).all()
  if len(stocks) == 0:
      logging.info('code:%r get rehab none', code)
      return None
  #logging.info('date:%r open:%r', stock[0].date, stock[0].open)
  # 关闭Session:
  #session.close()
  return stocks

def get_historys(code, date):
  # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
  stocks = session.query(History).filter(History.code == code).filter(History.time_key == date).all()
  #filter(or_(User.name == 'ed', User.name == 'wendy'))
  #filter(User.name.in_(['Alice', 'Bob', 'Carl']))
  if len(stocks) == 0:
      logging.info('code:%r date:%r get history none', code, date)
      return None
  return stocks

