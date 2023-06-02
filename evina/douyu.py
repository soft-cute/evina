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


class Douyu:
    def start(self, rid, name):
        self.name = name
        self.rid = rid
        self.ua = Faker(locale="zh_CN").user_agent()
        try:
            return self.api()
        except:
            self.data = self.js()
            return self.rea_rid()

    def api(self):
        url = 'https://web.sinsyth.com/lxapi/douyujx.x?rid={}'.format(self.rid)
        response = requests.get(url=url)
        self.response = json.loads(response.text)
        if self.response['state'] == 'NO':
            logger.info('斗鱼直播间 - {} | 暂未开播'.format(self.rid))
        if self.response['state'] == 'SUCCESS':
            if self.name == None:
                filename = self.response['Rendata']['data']['nickname']
            else:
                filename = self.name
            link = self.response['Rendata']['link']
            logger.info('斗鱼直播间 - {} | 源地址为 - {}'.format(self.rid, link))
            return {filename: {'rtmp_url': link}}

    def js(self):
        file = os.path.join(
            os.path.dirname(__file__),
            str(datetime.datetime.now()).replace(':', '-') + '.js')
        jstime = str(int(time.time()))
        did = '10000000000000000000000000001501'
        url = 'https://www.douyu.com/{}'.format(self.rid)
        response = requests.get(url=url)
        try:
            self.rid = re.findall(r'ROOM.room_id =(\d+)', response.text,
                                  re.S)[0]
        except:
            self.rid = re.findall(r'ROOM.room_id = (\d+)', response.text,
                                  re.S)[0]
        jsdate = re.findall(
            r'<script type="text/javascript">.*?var vdwdae325w_64we = .*?;(.*?)</script>',
            response.text, re.S)[0]
        # js = 'module.paths.push("D:/node/node_modules");const CryptoJS = require("crypto-js");' + jsdate + \
        #     "let arguments=process.argv.splice(2).join('').split(',');for(var i = 0; i < arguments.length; i++) {}console.log(ub98484234(arguments[0],arguments[1],arguments[2]))"
        js = 'module.paths.push("{}");const CryptoJS = require("crypto-js");'.format('/opt/hostedtoolcache/node/14.8.0/x64/lib/node_modules') + jsdate + \
            "let arguments=process.argv.splice(2).join('').split(',');for(var i = 0; i < arguments.length; i++) {}console.log(ub98484234(arguments[0],arguments[1],arguments[2]))"
        js = js.replace(';', ';\n').replace('}', '}\n')
        f = open(file=file, mode='w', encoding='utf8')
        f.write(js)
        f.close()
        # thenum = os.popen('{} "{}" {},{},{}'.format(os.path.join('D:\\', 'node', 'node.exe'), file, self.rid, did, jstime)).read().replace('\n', '')
        thenum = os.popen('{} "{}" {},{},{}'.format(
            '/opt/hostedtoolcache/node/14.8.0/x64/bin/node', file, self.rid,
            did, jstime)).read().replace('\n', '')

        dict = {
            'cdn': '',
            'rate': '-1',
            'iar': '1',
            'ive': '0',
            'hevc': '0',
            'fa': '0'
        }
        for date in thenum.split('&'):
            dict[date.split('=')[0]] = date.split('=')[1]
        os.remove(file)
        return dict

    def rea_rid(self):
        time = datetime.datetime.now().ctime().replace(':', '-')
        url = 'https://www.douyu.com/lapi/live/getH5Play/{}'.format(self.rid)
        headers = {
            'accept':
            'application/json, text/plain, */*',
            'accept-language':
            'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'origin':
            'https://www.douyu.com',
            'referer':
            'https://www.douyu.com/topic/pubg-3yhd?rid={}'.format(self.rid),
            'user-agent':
            self.ua
        }
        response = requests.post(url=url, headers=headers, data=self.data)
        if response.status_code != 200:
            logger.info('斗鱼直播间 - {} | 暂未开播'.format(self.rid))
            sys.exit()
        data = json.loads(response.text)
        if '房间未开播' in data.values():
            logger.info('斗鱼直播间 - {} | 暂未开播'.format(self.rid))
            sys.exit()
        rtmp_url = data['data']['rtmp_url']
        rtmp_live = data['data']['rtmp_live']
        rea_rid = rtmp_live.split('?')[0]
        http = os.path.join(random.choice(['http://hdltc1.douyucdn.cn/live', 'http://hw-tct.douyucdn.cn/live']))  \
            + '/' + rea_rid
        if self.name == None:
            name = self.get_name()
        else:
            name = self.name

        logger.info('斗鱼直播间 - {} - {} | 源地址为 - {}'.format(name, self.rid, http))
        return {name: {'rtmp_url': http}}

    def get_name(self):
        url = 'https://www.douyu.com/betard/{}'.format(self.rid)
        headers = {
            'accept':
            'application/json, text/plain, */*',
            'accept-language':
            'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'referer':
            'https://www.douyu.com/topic/pubg-3yhd?rid={}'.format(self.rid),
            'user-agent':
            self.ua
        }
        response = requests.get(url=url, headers=headers).text
        data = json.loads(response)
        name = data['room']['owner_name']
        return name