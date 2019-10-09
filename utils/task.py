#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created: 2019-07-25 20:54:07
# Author : Haoyi
# Email : haoyi@buaa.edu.cn

from collections import OrderedDict
import importlib
import uuid
import time

from utils.runtime import Runtime

STR_SEP = '\n'


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
            self.log.error(
                r"The config contains no {actions} and fails to register.")

    def run(self):
        r"""
        Run the task with specific moves (fire all the actions)
        """
        self.log.info("Task management starting!")
        feed_in = []  # initial input
        for action_name, action_object in self._workflow.items():
            feed_in = action_object.take(feed_in, self.log)
            action_object.print_cfg(self.log)

        # step 1: preprocessing of data
        # step 2: run a engine
        # step 3: postprocessing of output
        # step 4: statistics of result

    def __init_actions(self, actions_in):
        r"""
        A registartion for all the actions
        """
        if isinstance(actions_in, list):
            for (action_name, action_class) in actions_in:
                if hasattr(self.cfg, action_name):
                    # import modules
                    action_lib = importlib.import_module(action_name)
                    # acquire actions
                    action_object = getattr(action_lib, action_class)(
                        action_name, getattr(self.cfg, action_name))
                    # add actions
                    action_id = str(uuid.uuid4())
                    self.__add_work(action_id, action_object)
                else:
                    self.log.error(f"Missing action: {action_name}.")
        else:
            self.log.error("Wrong actions are defined.")

    def __add_work(self, action_id, action_object):
        self._workflow[action_id] = action_object


class Action(object):
    """
    The action is an auto operation in workflow.
    """

    class Utils(object):
        move_time_dict = dict()

        @classmethod
        def record_move_time(cls, move_func):
            r"""
            Calc the running time of moves in the action.
            """

            def wrapper(*args, **kw):
                start_time = time.time()
                result = move_func(*args, **kw)
                during_time = time.time() - start_time
                cls.move_time_dict[move_func.__name__] = during_time
                print('running time: ', during_time)
                return result

            return wrapper

    def __init__(self, action_name, action_cfg_in):
        self.cfg_dict = action_cfg_in
        self.name = action_name
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @Utils.record_move_time
    def take(self, input_object, logger):
        r"""
        A wrapper to fire the action
        """
        # build the action runtime environment
        assert 'runtime' in self.cfg_dict.keys()
        rt_cfg = self.cfg_dict['runtime']
        rt_cfg_base = rt_cfg['base']
        logger.write(f">> Build runtime: {rt_cfg_base}")
        if rt_cfg_base == 'builtin':
            # the action will run in the main thread
            # the interface is transfering the variables
            rt = None
        elif rt_cfg_base == 'native':
            # the action will run in the native system
            # the interface is a file system or database
            # TODO: add native interface
            # Reg the runtime
            assert hasattr(self, 'python_file_path')
            rt = Runtime(rt_cfg)
            # Call the native interpreter to exec the action file
            rt.call_native(self.python_file_path)
        elif rt_cfg_base == 'docker':
            # the action will firstly start a docker container and run on it
            # the interface is a file system or database
            raise EOFError
            # TODO: add docker interface
        else:
            logger.error(f"Runtime basic type {rt_cfg_base} is not supported.")
            return None

        # run this action at once
        assert 'input_type' in self.cfg_dict.keys()
        if isinstance(input_object, self.cfg_dict['input_type']):
            logger.write(f'>> Into Action: {self.name}')
            output_object = self._run(input_object, logger)
        else:
            logger.error(
                f"Action {self.name} input type mismatch: " +
                f"{type(input_object)} -> {self.cfg_dict['input_type']}.")
        return output_object

    def print_cfg(self, logger):
        r"""
        Print the configuration in this action.
        """
        cfg_str = self.name + ' configuration:' + STR_SEP
        for cfg_key, cfg_value in self.cfg_dict.items():
            cfg_str += f"{cfg_key}:{cfg_value}" + STR_SEP
        logger.info(cfg_str)

    def _run(self, input_object, logger):
        r"""
        Run the action
        """
        raise NotImplementedError
