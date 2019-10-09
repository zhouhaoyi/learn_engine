#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created: 2019-10-08 19:25:40
# Author : Haoyi
# Email : haoyi@buaa.edu.cn

class Runtime(object):
    r"""
    The runtime is a open-box running environment for all the actions.
    But it requires a fundamental check-in for action running on native & docker.
    """

    def __init__(self, cfg_in):
        super().__init__()
        # initial
        self.runtime_base = cfg_in['base']
        self.interpreter_path = cfg_in['path']
        self.extra_args = cfg_in['args']
        self.tensor_platform = cfg_in['platform']

    def call_native(self, python_file_path):
        print('test')

    def call_docker(self):
        raise NotImplementedError