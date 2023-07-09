#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/06/26 16:44:02
# @Author  : 橙橙橙心滴
# @File    : ffmpeg.py
'''


import subprocess
import time
import threading
import os
import datetime
from loguru import logger
import shutil
from evina.alipan import Backup


class FFmpeg:
    def __init__(self,name,rtmp) -> None:
        time = str(datetime.datetime.now().date())
        if 'did=10000000000000000000000000001501' in rtmp.rtmp_url:
            file = f'download/斗鱼录播/{name}/{time}'
            ali_file = os.path.join('录播', '斗鱼录播', name,
                                    time).replace('\\', '/')
            if not os.path.exists(file):
                os.makedirs(file)
        if 'douyin' in rtmp.rtmp_url:
            file = f'download/抖音录播/{name}/{time}'
            ali_file = os.path.join('录播', '抖音录播', name,
                                    time).replace('\\', '/')
            if not os.path.exists(file):
                os.makedirs(file)

        mp4_file = os.path.join(file, "%Y-%m-%d-%H-%M-%S.mp4").replace(
            "\\", "/")
        data = f"""bash -c 'ffmpeg -i "{rtmp.rtmp_url}" -c:a copy -c:v copy -f segment -segment_time 3600 -strftime 1 {mp4_file}'"""
        delfile = os.path.abspath(os.path.join(file, '../..'))
        subout = subprocess.run(data, shell=True)
        logger.info(subout)

        Backup(local_file=file, ali_file=ali_file)

        shutil.rmtree(delfile)
