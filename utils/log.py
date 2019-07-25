#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : log.py
# Author            : haoyi <haoyi@buaa.edu.cn>
# Date              : 24.07.2019
# Last Modified Date: 24.07.2019

import time
from multiprocessing import Manager, Pool
from functools import partial


class logger(object):
    """
    A stadard logger for tracking information (a queue).
    """

    def __init__(self, name='noname'):
        self.init_time = time.localtime()
        self.name = name
        self.log_queue = Manager().Queue()
        self.pool = Pool()

    def write(self, str_in):
        # pusher = partial(logger._push, self.log_queue)
        # self.pool.map(pusher, str_in)
        self.pool.apply(logger._push, args=(self.log_queue, str_in))
        # poper = partial(logger._pop, self.log_queue)
        # self.pool.map(poper, [])
        self.pool.apply(logger._pop, args=(self.log_queue,))

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


class logger_es(logger):
    """
    A simple logger flush data into a elasticserach database
    """

    def __init__(self, name='noname'):
        super(logger_es, self).__init__(name)
        self.out = 1
