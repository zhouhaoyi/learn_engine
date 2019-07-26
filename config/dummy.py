#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : dummy.py
# Author            : haoyi <haoyi@buaa.edu.cn>
# Date              : 24.07.2019
# Last Modified Date: 24.07.2019


class Task_Config(object):
    name = 'LTTT_TOY_train_StdM'
    actions = ('prep', 'engine', 'post', 'stat')

    prep = {
        'data_name': 'TOY',
        'data_root': './data/nasdaq100/',
        'data_size': [1000, 50, 50],
    }

    engine = {
        'runtime': {
            'platform': 'pytorch',
            'args': {'local_rank': ('0', 'int'), 'nproc_per_node': ('1', 'int')}
        },
        'model_name': 'transformer',
        'model_args': {
            'enc_size': 82,
            'dec_size': 82,
            'output_size': 1,
            'e_layers': [4, 3, 2],
            'd_layers': 6,
            'load_model_path': None
        },
        'type': 'train',
        'train': {
            'use_gpu': True,
            'batch_size': 16,
            'gpu_nums': 4,
            'max_epoch': 5
        }
    }

    post = {}

    stat = {}

    view = {}

    log = {}
