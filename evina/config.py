#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/04/25 15:40:14
# @Author  : 橙橙橙心滴
# @File    : config.py
'''

import argparse
import os
import sys

from aligo import Aligo
from dynaconf import Dynaconf
from loguru import logger

from evina import replacement


class Conf:
    def __init__(self) -> None:
        replacement.DotEnv._get_stream = replacement.ReplaceMent.new_get_stream
        conf_file = os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__))),
            'disposition', 'config.conf')
        evina_file = os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__))),
            'disposition', 'evina.conf')

        parse = argparse.ArgumentParser()
        parse.add_argument('--start', '-s', nargs=1, help='选择需要录制的平台。')
        parse.add_argument('--url', '-u', nargs='*', help='需要录制的直播间URL/ID。')
        parse.add_argument('--name', '-n', nargs='*', help='自定义文件夹名称')
        self.arg = parse.parse_args()

        self.conf = Dynaconf(envvar_prefix='evina',
                             load_dotenv=True,
                             dotenv_path=conf_file,
                             dotenv_override=True)

        self.evina_douyu = Dynaconf(envvar_prefix='douyu',
                                    load_dotenv=True,
                                    dotenv_path=evina_file,
                                    dotenv_override=True)

        self.evina_douyin = Dynaconf(envvar_prefix='douyin',
                                     load_dotenv=True,
                                     dotenv_path=evina_file,
                                     dotenv_override=True)

        replacement.Auth._EMAIL_USER = self.conf.settings.email_user
        replacement.Auth._EMAIL_PASSWORD = self.conf.settings.email_password
        email_host = replacement.Auth._EMAIL_USER.split('@')[1].split('.')
        replacement.Auth._EMAIL_HOST = 'smtp.{}.{}'.format(
            email_host[0], email_host[1])
        Aligo(email=(self.conf.settings.email_user, '阿里云盘登录二维码验证'))


class Arg(Conf):
    def __init__(self) -> None:
        super().__init__()
        if self.arg.start != None:
            self.start = self.arg.start[0]
            if self.arg.url != None:
                self.dict = {}
                self.dict[self.start] = {}
                if self.arg.name != None:
                    if len(self.arg.url) == len(self.arg.name):
                        for num in range(len(self.arg.url)):
                            self.dict[self.start][
                                self.arg.url[num]] = self.arg.name[num]
                    else:
                        logger.warning('url和name参数不一致!!')
                        sys.exit()
                    logger.info('程序开始执行')
                    for url, name in self.dict[self.start].items():
                        logger.info('平台 - {} | ID/URL - {} | name - {}'.format(
                            self.arg.start[0], url, name))
                else:
                    logger.info('未定义名称，使用直播间默认名称')
                    logger.info('程序开始执行')
                    for url in self.arg.url:
                        self.dict[self.start][url] = None
                        logger.info('平台:{}--ID/URL:{}'.format(
                            self.arg.start[0], url))
            else:
                logger.warning('URL/ID定义错误!!')
                sys.exit()


class Env(Conf):
    def __init__(self) -> None:
        super().__init__()
        if self.arg.start == None:
            self.dict = {}
            try:
                self.evina_douyin.url
            except:
                self.evina_douyin.url = None
            try:
                self.evina_douyu.url
            except:
                self.evina_douyu.url = None
            self.dict = {}
            if self.evina_douyin.url != None:
                self.dict['douyin'] = {}
                for key, value in self.evina_douyin.url.items():
                    self.dict['douyin'][str(value).strip()] = None
            if self.evina_douyu.url != None:
                self.dict['douyu'] = {}
                for key, value in self.evina_douyu.url.items():
                    self.dict['douyu'][str(value).strip()] = None
            logger.info('程序开始执行')
            for start in self.dict:
                for url, name in self.dict[start].items():
                    logger.info('平台 - {} | ID/URL - {}'.format(start, url))
