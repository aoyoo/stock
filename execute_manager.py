#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import base64
import logging
import datetime
import time

import log

def now():
    return int(time.time())

class context:
    name = ""
    max_count = 0
    refresh_time = 0

    count = 0
    last_execute_time = 0

    def __init__(self, name, refresh_time, max_count):
        self.name = name
        self.max_count = max_count
        self.refresh_time = refresh_time

        self.count = 0
        self.last_execute_time = now()
        logging.info("function execute context init name:%r:%r", self.name, self.last_execute_time)

    def refresh(self):
        self.count = 0
        self.last_execute_time = now()

    def execute(self, f, *args):
        if (now() - self.last_execute_time > self.refresh_time):
            self.refresh()

        if self.count > self.max_count:
            self.count += 1
            self.last_execute_time = now()
            logging.info("name:%r can not execute. count:%r last_execute_time:%r", self.name, self.count, self.last_execute_time)
            return None

        self.count += 1
        self.last_execute_time = now()
        logging.info("name:%r execute. count:%r last_execute_time:%r", self.name, self.count, self.last_execute_time)
        return f(*args)


class execute_manager:
    execute_context = {}

    def execute(self, f, *args):
        func_name = f.__name__
        ctx = self.execute_context.get(func_name)
        if ctx is None:
            ctx = context(func_name, 30, 10)
            self.execute_context[func_name] = ctx
        return ctx.execute(f, *args)

manager = execute_manager()

def get_manager():
    return manager

if __name__ == '__main__':
    log.init_log('./log', level=logging.DEBUG)
    logging.info('start')

    logging.info('end')

