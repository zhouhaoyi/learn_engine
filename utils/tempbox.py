#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created: 2019-10-09 10:29:50
# Author : Haoyi
# Email : haoyi@buaa.edu.cn

import os
import pickle as pk
import uuid


class TempBox(object):
    r"""
    A simple container manages the temporary files
    """

    def __init__(self, temp_path, filename, logger):
        super().__init__()
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
        self.dir_path = temp_path
        if filename is None:
            filename = str(uuid.uuid4()) + '.hy'
        else:
            if not os.path.exists(os.path.join(temp_path, filename)):
                return None
        self.filename = filename
        self.container = None
        self.log = logger

    def put(self, object):
        """
        put a object in the TempBox
        """
        pass

    def get(self, object):
        """
        get a object from the TempBox
        """
        pass

    def load(self, filename):
        load_file_path = os.path.join(self.dir_path, filename)
        with open(load_file_path) as load_file:
            try:
                self.container = pk.load(load_file)
                self.log.info(f'{filename} was loaded at {save_file_path}')
            except:
                self.log.error(
                    f'Fail to load the {filename} file at {load_file_path}.')
                return None
        return self.container

    def save(self, filename, object):
        save_file_path = os.path.join(self.dir_path, filename)
        with open(save_file_path) as save_file:
            try:
                pk.dump(save_file, object)
                self.log.info(f'{filename} was dumped at {save_file_path}')
            except:
                self.log.error(f'Fail to dump the {filename} file.')
                return False
        return True