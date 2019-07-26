#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created: 2019-07-25 20:54:07
# Author : Haoyi
# Email : haoyi@buaa.edu.cn

from collections import OrderedDict


class task(object):
    """
    Task manager:
        The collection of workflow, each part is a action.
        A graph explain:
            |               config                   | |      |
            | data -> prep -> engine -> post -> stat | | view |
            |                log                     | |      |
    """

    def __init__(self, config, logger):
        self.cfg = config
        self.log = logger
        self._workflow = OrderedDict()
        # initial actions from config
        if hasattr(self.log, 'actions'):
            self.__init_actions(self.log.actions)
        else:
            self.log.write('Failed to regist')

    def run(self):
        self.log.write('Task management starting!')
        # step 1: preprocessing of data
        # step 2: run a engine
        # step 3: postprocessing of output
        # step 4: statistics of result

    def __init_actions(self, actions_in):
        if isinstance(actions_in, tuple):
            for action_name in actions_in:
                if hasattr(self.cfg, action_name):
                    self.__add_work(action_name,
                                    action(getattr(self.cfg, action_name)))
                else:
                    self.log.write('.')
        else:
            self.log.write('Wrong actions are defined.')

    def __add_work(self, name, action_obejct):
        self._workflow[name] = action_obejct


class action(object):
    """
    The action is an antomic operation in workflow.
    """

    def __init__(self, action_cfg_in):
        self.test = 1