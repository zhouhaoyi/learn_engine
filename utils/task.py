#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created: 2019-07-25 20:54:07
# Author : Haoyi
# Email : haoyi@buaa.edu.cn

from collections import OrderedDict
import importlib

STR_SEP = '\n\l'

class Task(object):
    r"""
    Task manager:
        The collection of workflow, each part is a action.
        A graph explain:
            |               config                   | |      |
            | data -> prep -> engine -> post -> stat | | view |
            |                log                     | |      |
    """

    def __init__(self, config, logger):
        # initial
        self.cfg = config
        self.log = logger
        self._workflow = OrderedDict()
        # register actions from config
        if hasattr(self.cfg, 'actions'):
            self.__init_actions(self.cfg.actions)
        else:
            self.log.error(r"The config contains no {actions} and fails to register.")

    def run(self):
        r"""
        Run the task (fire all the actions)
        """
        self.log.info("Task management starting!")
        feed_in = []  # initial input
        for action_name, action_object in self._workflow.items():
            feed_in = action_object.take(feed_in, self.log)

        # step 1: preprocessing of data
        # step 2: run a engine
        # step 3: postprocessing of output
        # step 4: statistics of result

    def __init_actions(self, actions_in):
        r"""
        A registartion for all the actions
        """
        if isinstance(actions_in, dict):
            for action_name, action_class in actions_in.items():
                if hasattr(self.cfg, action_name):
                    # import modules
                    action_lib = importlib.import_module(action_name)
                    # add actions
                    action_object = getattr(action_lib, action_class)(
                        action_name, getattr(self.cfg, action_name))
                    self.__add_work(action_name, action_object)
                else:
                    self.log.error(f"Missing action: {action_name}.")
        else:
            self.log.error("Wrong actions are defined.")

    def __add_work(self, name, action_obejct):
        self._workflow[name] = action_obejct


class Action(object):
    """
    The action is an antomic operation in workflow.
    """

    def __init__(self, action_name, action_cfg_in):
        self.cfg_dict = action_cfg_in
        self.name = action_name

    def take(self, input_object, logger):
        r"""
        A wrapper to fire the action
        """
        assert 'input_type' in self.cfg_dict.keys()
        if isinstance(input_object, self.cfg_dict['input_type']):
            logger.write(f'>> Into Action: {self.name}')
            output_object = self._run(input_object, logger)
        else:
            logger.error(
                f"Action {self.name} input type mismatch: \
                    {type(input_object)} -> {self.cfg_dict['input_type']}."
            )

        return output_object

    def print_cfg(self, logger):
        r"""
        Print the configuration in this action.
        """
        cfg_str = ''
        for cfg_key, cfg_value in self.cfg_dict.items():
            cfg_str += f"{cfg_key}:{cfg_value}" + STR_SEP
        logger.info(cfg_str)

    def _run(self, input_object, logger):
        r"""
        Run the action
        """
        raise NotImplementedError
