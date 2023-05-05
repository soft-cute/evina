#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/04/28 15:17:09
# @Author  : 橙橙橙心滴
# @File    : check.py
'''

import threading
import time

import config
import douyin
import douyu


class Evina(config.Arg, config.Env):
    def __init__(self) -> None:

        super().__init__()
        for start in self.dict:
            if start == 'douyu':
                for url, name in self.dict[start].items():
                    if 'http' in url and not url.endswith('/'):
                        url = url.rsplit('/', 1)[1]
                    if not self.check(url):
                        threading.Thread(target=douyu.Douyu,
                                         args=(url, name, self.conf.settings),
                                         name=url).start()
            if start == 'douyin':
                for url, name in self.dict[start].items():
                    if not self.check(str(url)):
                        threading.Thread(target=douyin.Douyin,
                                         args=(name, self.conf.settings, url),
                                         name=url).start()

    def check(self, name):
        for thread in threading.enumerate():
            if name == thread.name:
                return True
        return False


if __name__ == '__main__':
    while True:
        sleep = config.Conf().conf.settings.sleep
        Evina()
        time.sleep(sleep)
