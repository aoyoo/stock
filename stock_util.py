import os
import logging

from futu import *
import log

class StockUtil:
  ctx = None

  def init(self):
    self.ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    SysConfig.set_all_thread_daemon
    logging.info("init QuoteContext success")

  def get_hk_stock_code(self):
    res = self.ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK)
    if res[0] != RET_OK:
        logging.error("get_stock_basicinfo fail:", res[1])
        return None

    content = res[1]
    logging.info("get HK stock size:%d", content.code.size)
    return content.code

  def close(self):
    if self.ctx != None:
      self.ctx.close()
 

 get_market_snapshot
get_market_snapshot(self, code_list)
"earning_per_share"
参数	类型	说明
code	str	股票代码
update_time	str	更新时间(yyyy-MM-dd HH:mm:ss)（港股A股默认是北京时间）
last_price	float	最新价格
open_price	float	今日开盘价
high_price	float	最高价格
low_price	float	最低价格
prev_close_price	float	昨收盘价格
volume	int	成交数量
turnover	float	成交金额
turnover_rate	float	换手率（该字段为百分比字段，默认不展示%）
suspension	bool	是否停牌(True表示停牌)
listing_date	str	上市日期 (yyyy-MM-dd)
equity_valid	bool	是否正股（为true时以下正股相关字段才有合法数值）
issued_shares	int	发行股本
total_market_val	float	总市值
net_asset	int	资产净值
net_profit	int	净利润
earning_per_share	float	每股盈利
outstanding_shares	int	流通股本
net_asset_per_share	float	每股净资产

get_rehab
get_rehab(self, code)
获取给定股票的复权因子

Parameters:	code – 需要查询的股票代码.
Returns:	(ret, data)
ret != RET_OK 返回错误字符串

ret == RET_OK 返回pd dataframe数据

参数	类型	说明
ex_div_date	str	除权除息日
split_ratio	float	拆合股比例（该字段为比例字段，展示为小数表示）例如，对于5股合1股为5.0，对于1股拆5股为0.2
per_cash_div	float	每股派现
per_share_div_ratio	float	每股送股比例（该字段为比例字段，展示为小数表示）
per_share_trans_ratio	float	每股转增股比例（该字段为比例字段，展示为小数表示）
allotment_ratio	float	每股配股比例（该字段为比例字段，展示为小数表示）