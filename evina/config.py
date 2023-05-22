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
            os.path.join(os.environ.get('HOME'), '.evina', 'config.conf'))
        if not os.path.exists(conf_file):
            logger.error(
                ' 未发现配置文件 config.conf | 请输入: wget -O ~/.evina/config.conf https://raw.githubusercontent.com/Softcute-Ezong/type/main/evina/config.conf'
            )
            sys.exit()
        evina_file = os.path.join(
            os.path.join(os.environ.get('HOME'), '.evina', 'evina.conf'))
        if not os.path.exists(evina_file):
            logger.error(
                ' 未发现配置文件 evina.conf | 请输入: wget -O ~/.evina/evina.conf https://raw.githubusercontent.com/Softcute-Ezong/type/main/evina/evina.conf'
            )
            sys.exit()

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
        if self.conf.settings.email_user == 'XXXXXX':
            logger.error(
                " 未配置验证邮箱 | 修改 config.conf EVINA_SETTINGS__EMAIL_USER = 'XXXXXX'"
            )
            sys.exit()
        if self.conf.settings.email_password == 'XXXXXX':
            logger.error(
                " 未配置邮箱 SMTP | 修改 config.conf EVINA_SETTINGS__EMAIL_PASSWORD = 'XXXXXX'"
            )
            sys.exit()
        email_host = self.conf.settings.email_user.split('@')[1].split('.')
        email_config = replacement.EMailConfig(
            email=self.conf.settings.email_user,
            host='smtp.{}.{}'.format(email_host[0], email_host[1]),
            port=465,
            password=self.conf.settings.email_password,
            user=self.conf.settings.email_user,
            content='阿里云盘登录二维码验证')
        Aligo(email=email_config)


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
