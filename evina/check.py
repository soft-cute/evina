#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/05/26 23:00:18
# @Author  : 橙橙橙心滴
# @File    : check.py
'''

import os
import time

from box import Box
from dynaconf import Dynaconf
from loguru import logger

import douyin
import douyu


class Check:
    def __init__(self) -> None:
        evina_file = os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
            'config', 'evina.conf')

        self.douyu = Dynaconf(envvar_prefix='douyu',
                              load_dotenv=True,
                              dotenv_path=evina_file,
                              dotenv_override=True)

        self.douyin = Dynaconf(envvar_prefix='douyin',
                               load_dotenv=True,
                               dotenv_path=evina_file,
                               dotenv_override=True)


class Env(Check):
    def __init__(self) -> None:
        super().__init__()
        self.dict = {}
        try:
            self.douyin.url
        except:
            self.douyin.url = None
        try:
            self.douyu.url
        except:
            self.douyu.url = None
        if self.douyin.url != None:
            self.dict['douyin'] = {}
            for key, value in self.douyin.url.items():
                self.dict['douyin'][str(value).strip()] = None
        if self.douyu.url != None:
            self.dict['douyu'] = {}
            for key, value in self.douyu.url.items():
                self.dict['douyu'][str(value).strip()] = None
        logger.info('程序开始执行')
        for start in self.dict:
            for url, name in self.dict[start].items():
                logger.info('平台 - {} | ID/URL - {}'.format(start, url))


class Evina(Env):
    def __init__(self) -> None:

        super().__init__()
        list = []
        dict = {}
        for start in self.dict:
            if start == 'douyu':
                for url, name in self.dict[start].items():
                    if 'http' in url and not url.endswith('/'):
                        url = url.rsplit('/', 1)[1]
                    douyu_url = douyu.Douyu().start(url, name)
                    time.sleep(3)
                    if douyu_url != None:
                        # list.append(douyu_url)
                        dict.update(douyu_url)

            if start == 'douyin':
                for url, name in self.dict[start].items():
                    douyin_url = douyin.Douyin().start(name, url)
                    time.sleep(3)
                    if douyin_url != None:
                        # list.append(douyin_url)
                        dict.update(douyin_url)

        # dict['evina'] = {}
        file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'config',
                         'config.yml'))

        setting = Box.from_yaml(filename=file)
        for key, value in dict.items():
            if setting.evina != {}:
                if dict != {}:
                    if dict[key] == setting.evina[key] and setting.evina[key][
                            'status'] == 'running':
                        dict[key]['status'] = 'running'
                    else:
                        dict[key]['status'] = 'stopping'
                else:
                    dict = setting.evina
            else:
                dict[key]['status'] = 'stopping'
        setting.evina.merge_update(dict)
        setting.to_yaml(filename=file)
        print(os.getcwd())


if __name__ == '__main__':

    Evina()