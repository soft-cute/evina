#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/06/22 22:35:39
# @Author  : 橙橙橙心滴
# @File    : main.py
'''

import evina
import time
from importlib import reload
from loguru import logger


if __name__ == '__main__' :
    logger.add('evina.log')
    while True:
        reload(evina)
        from evina import Start
        Start()
        time.sleep(300)
