#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/04/27 16:29:40
# @Author  : 橙橙橙心滴
# @File    : ssh.py
'''

import paramiko
from loguru import logger


class Ssh:
    def __init__(self, url, file, settings):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='43.143.216.130',
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


# Ssh('http://tc-tct.douyucdn2.cn/dyliveflv1a/1457640rTDKVcLaU_2000p.flv?wsAuth=a9d0cfe4e3c5ab1cff216d4cf29dccb1&token=cpn-androidmpro-0-1457640-2f3e9731c8986be571e13853f5b0f406b6faaed0e2aa8247&logo=0&expire=0&did=88668a81d0d5e5e8f51a21ef5fd01d3f&origin=tct&vhost=play2', '/home/code/ffm')