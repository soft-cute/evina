#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/05/29 23:32:14
# @Author  : 橙橙橙心滴
# @File    : douyu.py
'''

import datetime
import json
import os
import random
import re
import sys
import time

import requests
from faker import Faker
from loguru import logger


import datetime
import json
import os
import random
import re
import sys
import time

import requests
from faker import Faker
from loguru import logger
import execjs,hashlib


class Douyu:
    def start(self,rid, name) -> None:
        self.ua = Faker(locale="zh_CN").user_agent()
        self.s = requests.Session()
        self.res = self.s.get('https://m.douyu.com/' + str(rid), timeout=30).text

        result = re.search(r'rid":(\d{1,8}),"vipId', self.res)
        if result:
            self.rid = result.group(1)
        else:
            logger.warning('斗鱼房间号错误 - {} - 请检查'.format(rid))
            exit(1)
        if name == None:
            self.name = re.findall(r'nickname":"(.*?)",',self.res)[0]
        else:self.name = name
        return self.pc_url()

    @staticmethod
    def md5(data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def pc_url(self, cdn='ws-h5', rate=4):
        self.did = '10000000000000000000000000001501'
        res = self.s.get('https://www.douyu.com/' + str(self.rid), timeout=30).text
        result = re.search(r'(vdwdae325w_64we[\s\S]*function ub98484234[\s\S]*?)function', res).group(1)
        func_ub9 = re.sub(r'eval.*?;}', 'strc;}', result)
        js = execjs.compile(func_ub9)
        res = js.call('ub98484234')

        v = re.search(r'v=(\d+)', res).group(1)
        t10 = str(int(time.time()))
        rb = self.md5(self.rid + self.did + t10 + v)

        func_sign = re.sub(r'return rt;}\);?', 'return rt;}', res)
        func_sign = func_sign.replace('(function (', 'function sign(')
        func_sign = func_sign.replace('CryptoJS.MD5(cb).toString()', '"' + rb + '"')
        js = execjs.compile(func_sign)
        params = js.call('sign', self.rid, self.did, t10)

        params += '&cdn={}&rate={}'.format(cdn, 4)

        url = 'https://www.douyu.com/lapi/live/getH5Play/{}'.format(self.rid)
        res = self.s.post(url, params=params, timeout=30).json()
        if res['msg'] == '房间未开播':
            logger.info('斗鱼直播间 - {} - {} | 暂未开播'.format(self.name,self.rid))
        else : 
            logger.info('斗鱼直播间 - {} - {} | 源地址为 - {}'.format(self.name, self.rid, res['data']['rtmp_url'] + '/' + res['data']['rtmp_live']))
            return {self.name: {'rtmp_url': res['data']['rtmp_url'] + '/' + res['data']['rtmp_live']}}
    
