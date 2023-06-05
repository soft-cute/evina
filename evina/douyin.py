#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/05/29 22:12:38
# @Author  : 橙橙橙心滴
# @File    : douyin.py
'''

import json
import os
import re
import sys
from urllib import parse

import requests
from faker import Faker
from loguru import logger


class Douyin:
    def start(self, name, uid=None):
        self.name = name
        self.cookies = os.getenv('DOUYIN-COOKIES')
        self.ua = Faker(locale="zh_CN").user_agent()

        if uid == None:
            sys.exit()
        if uid.endswith('/'):
            uid = uid.rsplit('/', 1)[0]
        uid = uid.rsplit('/', 1)
        if len(uid) == 1:
            uid = uid[0]

        if uid[1] == '':
            uid = uid[0].rsplit('/', 1)[1]
        if type(uid).__name__ == 'list':
            uid = uid[1]

        if not uid.isdigit():
            url = 'https://v.douyin.com/' + uid
            uid = self.phone(url)
        url = 'https://live.douyin.com/' + uid
        return self.geturl(url)

    def geturl(self, url):
        headers = {
            'user-agent': self.ua,
            'referer': 'https://live.douyin.com/',
            'cookie': self.cookies,
            'accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language':
            'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
        }
        response = requests.get(url=url, headers=headers).text
        response = parse.unquote(response)
        try:
            data = json.loads(
                re.findall(
                    r'<script id="RENDER_DATA" type="application/json">(.*?)</script>',
                    response, re.S)[0])
            stream_url = data['app']['initialState']['roomStore']['roomInfo'][
                'room']['stream_url']
            if self.name == None:
                name = data['app']['initialState']['roomStore']['roomInfo'][
                    'anchor']['nickname']
            else:
                name = self.name
            list = []
            flv_pull_url = stream_url['flv_pull_url']
            for key, value in flv_pull_url.items():
                list.append(value)
            hls_pull_url_map = stream_url['hls_pull_url_map']
            for key, value in hls_pull_url_map.items():
                list.append(value)
                logger.info('抖音直播间 - {} - {} | 源地址为 - {}'.format(
                    name,
                    url.rsplit('/', 1)[1], list[0]))
                return {name: {'rtmp_url': list[0]}}

        except:
            logger.info('抖音直播间 - {} | 暂未开播'.format(url.rsplit('/', 1)[1]))

    def phone(self, url):
        resp = requests.get(url=url)
        data = resp.url.split('?')[0].split('user')
        if len(data) != 2:
            logger.info('抖音直播间 - {} | 链接已失效'.format(url.rsplit('/', 1)[1]))
            sys.exit()
        if len(data) == 2:
            link = 'user'.join(data) + '?app_code_link'
            headers = {
                'accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language':
                'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'cookie':self.cookies,
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44',
            }
            response = requests.get(url=link, headers=headers).text
            try:
                uid = re.findall(r'<a href="https://live.douyin.com/(\d+)\?',
                                 response, re.S)[0]
                return uid
            except:
                logger.info('抖音直播间 - {} | 暂未开播'.format(url.rsplit('/', 1)[1]))
                sys.exit()