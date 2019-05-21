#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import base64
import logging
import datetime

import pandas as pd
from futu import *

import log

def get():

    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    SysConfig.set_all_thread_daemon

    rehab_res = quote_ctx.get_rehab("HK.00700")
    if rehab_res[0] != 0:
        logging.info("quote_ctx.get_rehab fail:", rehab_res[1])
        return

    logging.info("quote_ctx.get_rehab get success")
    rehab = rehab_res[1]

    print rehab
    print rehab.columns.values.tolist()

    quote_ctx.close()

if __name__ == '__main__':
    log.init_log('./log', level=logging.DEBUG)
    logging.info('start')


    get()

    logging.info('end')

