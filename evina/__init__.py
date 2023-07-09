#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/06/22 22:35:33
# @Author  : 橙橙橙心滴
# @File    : __init__.py
'''

import os
import threading
import time

from box import Box
from dynaconf import Dynaconf
from loguru import logger

from evina.ffmpeg import FFmpeg
from evina.terrace import Douyin, Douyu


class Config:
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

    def read(self):
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
        logger.info('读取配置文件')
        for start in self.dict:
            for url, name in self.dict[start].items():
                logger.info('平台 - {} | ID/URL - {}'.format(start, url))


class Check(Config):
    def __init__(self) -> None:
        super().__init__()
        super().read()
        print('\n' + '==' * 50 + '\n')
        logger.info('程序开始运行')
        self.url_dict = {}
        for start in self.dict:
            if start == 'douyu':
                for url, name in self.dict[start].items():
                    if 'http' in url and not url.endswith('/'):
                        url = url.rsplit('/', 1)[1]
                    douyu_url = Douyu().start(url, name)
                    time.sleep(5)
                    if douyu_url != None:
                        self.url_dict.update(douyu_url)

            if start == 'douyin':
                for url, name in self.dict[start].items():
                    douyin_url = Douyin().start(name, url)
                    time.sleep(5)
                    if douyin_url != None:
                        self.url_dict.update(douyin_url)


class Start(Check):
    def __init__(self) -> None:
        super().__init__()
        dict = Box(self.url_dict)
        for name, rtmp in dict.items():
            if not self.check(name):
                threading.Thread(target=FFmpeg, args=(name, rtmp),
                                 name=name).start()

    def check(self, name):
        for thread in threading.enumerate():
            if name == thread.name:
                return True
        return False
