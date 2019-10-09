#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created: 2019-07-26 22:14:28
# Author : Haoyi
# Email : haoyi@buaa.edu.cn

from utils.task import Action
import os

class TOY_gen2(Action):
    r"""
    Generate toy data for long term time series forecasting.
    Config Example ==>
        'input_type': list,
        'data_name': 'TOY',
        'data_root': './data/nasdaq100/',
        'data_size': [1000, 50, 50],
    """
    # def __init__(self, action_name, action_cfg_in):
    #     super(TOY_processing, self).__init__(action_name, action_cfg_in)

    def __init__(self, action_name, action_cfg_in):
        super().__init__(action_name, action_cfg_in)
        self.python_file_path = os.path.abspath(__file__)

    def _run(self, input_object, logger):
        r"""
        Run the action
        """
        print('run prep->TOY2.')
        print(f'TOY2 run at {self.python_file_path}')
        return None