#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/04/27 16:29:40
# @Author  : 橙橙橙心滴
# @File    : ssh.py
'''

import sys

import paramiko
from loguru import logger


class Ssh:
    def __init__(self, url, file, settings):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if settings.ip == 'XXXXXX':
            logger.error(
                "未配置主机IP | 修改 config.conf EVINA_SETTINGS__IP = 'XXXXXX'")
            sys.exit()
        ssh.connect(hostname=settings.ip,
                    port=6666,
                    username='root',
                    password='03456',
                    timeout=5)
        # data = "bash -lc 'ffmpeg -i " + '"{}"'.format(url) + " -c:a copy -c:v copy -threads 5 -preset ultrafast -f segment -segment_time 3600 -strftime 1 {}'".format(file)
        data = "bash -lc 'ffmpeg -i " + '"{}"'.format(
            url
        ) + " -c:a copy -c:v copy -bsf:a aac_adtstoasc -threads {} -preset {} -f {}  -f segment -segment_time {} -strftime 1 ".format(
            str(settings.thread), settings.preset, settings.scheme,
            str(settings.time)) + '"{}"'.format(file) + "'"
        stdin, stdout, stderr = ssh.exec_command(data)
        logger.info(stderr.read())
        logger.info(stdout.read().decode())


