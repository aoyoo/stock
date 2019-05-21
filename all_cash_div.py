#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import base64
import logging
import datetime

import log
import stock_util


def close(ctx):
    ctx.close()

if __name__ == '__main__':
    log.init_log('./log', level=logging.DEBUG)
    logging.info('start')

    util = stock_util.StockUtil()
    util.init()
    
    stock_ids = util.get_hk_stock_code()

    logging.info('end')
    util.close()


