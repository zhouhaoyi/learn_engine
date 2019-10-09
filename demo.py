#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : demo.py
# Author            : haoyi <haoyi@buaa.edu.cn>
# Date              : 21.07.2019
# Last Modified Date: 24.07.2019

# basic
import argparse
import time

# need
from utils.log import Logger
from utils.task import Task

# change
from config import dummy

def test2():
    tlog = Logger(name='test_logger')
    tcfg = dummy.Task_Config()
    ttask = Task(tcfg, tlog)
    ttask.run()

def test():
    """
    A simple tester to Tasks
    """
    tlog = Logger(name='test_logger')
    tlog.write('test you are right!')
    tlog.write('test you are 1!')
    tlog.write('test you are 2!')
    tlog.write('test you are 3!')
    time.sleep(3)
    tlog.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--local_rank", default=0, type=int)
    parser.add_argument("--nproc_per_node", default=1, type=int)
    args = parser.parse_args()

    test2()
