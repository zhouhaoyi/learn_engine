#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : log.py
# Author            : haoyi <haoyi@buaa.edu.cn>
# Date              : 24.07.2019
# Last Modified Date: 24.07.2019

import time
from multiprocessing import Manager, Pool

# unused
# from functools import partial


class Logger(object):
    """
    A stadard logger for tracking information (a queue).
    """

    def __init__(self, name='noname'):
        self.init_time = time.localtime()
        self.name = name
        self.log_queue = Manager().Queue()
        self.pool = Pool()

    def write(self, str_in):
        # pusher = partial(Logger._push, self.log_queue)
        # self.pool.map(pusher, str_in)
        self.pool.apply(Logger._push, args=(self.log_queue, str_in))
        # poper = partial(Logger._pop, self.log_queue)
        # self.pool.map(poper, [])
        self.pool.apply(Logger._pop, args=(self.log_queue,))

    def error(self, str_in):
        self.write('[ERROR] ' + str_in)

    def info(self, str_in):
        self.write('[INFO] ' + str_in)

    def time(self, str_in):
        self.write('[TIME] ' + str_in)

    def quit(self):
        self.pool.close()
        self.pool.join()
        print("Logger is closed!")

    @staticmethod
    def _push(queue, item_in):
        queue.put(item_in)

    @staticmethod
    def _pop(queue):
        if queue.empty():
            raise Exception("LogQueueUnderflow in .pop()")
        item = queue.get()
        print(item)
        return item


class LoggerEs(Logger):
    """
    A simple logger flush data into a elasticserach database
    """

    def __init__(self, name='noname'):
        super(LoggerEs, self).__init__(name)
        raise NotImplementedError
