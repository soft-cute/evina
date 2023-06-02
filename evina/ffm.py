#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/05/31 22:42:44
# @Author  : 橙橙橙心滴
# @File    : ffm.py
'''

import datetime
import os
import shutil
import sys
import threading

from box import Box
from loguru import logger

import alipan


class Ffm:
    def __init__(self) -> None:
        self.dict = {}
        file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'config',
                         'config.yml'))
        self.conf = Box.from_yaml(filename=file)
        self.dict['evina'] = {}
        for key, value in self.conf.evina.items():
            if value['status'] == 'stopping':
                value['status'] = 'running'
                self.conf.to_yaml(filename=file)
                self.dict['evina'][key] = value
        os.system(
            'bash -c "git add ./config/config.yml ./evina.log && git commit -a -m Add changes && git push"'
        )
        if self.dict == {}:
            sys.exit()
        else:
            self.work()

    def work(self):

        for key, value in self.dict['evina'].items():
            time = str(datetime.datetime.now().date())
            if 'douyu' in value.rtmp_url:
                file = f'~/download/斗鱼录播/{key}/{time}'
                ali_file = os.path.join('录播', '斗鱼录播', key,
                                        time).replace('\\', '/')
                if not os.path.exists(file):
                    os.makedirs(file)
            if 'douyin' in value.rtmp_url:
                file = f'~/download/抖音录播/{key}/{time}'
                ali_file = os.path.join('录播', '抖音录播', key,
                                        time).replace('\\', '/')
                if not os.path.exists(file):
                    os.makedirs(file)
            data = ' '.join([
                'bash -c "ffmpeg -t 19800 -i ', "'", value.rtmp_url, "'",
                '-c:a copy -c:v copy -preset ultrafast -f segment -segment_time 3600 -strftime 1 ',
                os.path.join(file, "%Y-%m-%d-%H-%M-%S.mp4").replace('\\',
                                                                    '/'), '"'
            ])
            threading.Thread(target=self.ffm,
                             args=(
                                 data,
                                 file,
                                 ali_file,
                                 key,
                                 value,
                             )).start()

    def ffm(self, data, file, ali_file, key, value):
        delfile = os.path.abspath(os.path.join(file, '../../aaa'))
        subout = os.system(data)
        logger.info(subout)

        alipan.Backup(local_file=file, ali_file=ali_file)

        shutil.rmtree(delfile)
        if value.status == 'running':
            del self.conf[key]
            os.system(
                'bash -c "git add ./config/config.yml && git commit -a -m Add changes && git push"'
            )


if __name__ == '__main__':

    Ffm()
