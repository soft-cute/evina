#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/04/26 23:03:42
# @Author  : 橙橙橙心滴
# @File    : douyin.py
'''

import datetime
import json
import os
import random
import re
import shutil
import subprocess
import sys
import threading
import time
from urllib import parse

from evina import alipan
import requests
from evina import ssh
from faker import Faker
from loguru import logger


class Douyin:
    def __init__(self, name, settings, uid=None):
        logger.info('线程创建成功 | 线程名 - {} | PID - {}'.format(
            threading.current_thread().name,
            threading.current_thread().ident))
        self.name = name
        self.settings = settings
        self.open = self.settings.open
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
        self.geturl(url)

    def geturl(self, url):
        headers = {
            'user-agent': self.ua,
            'referer': 'https://live.douyin.com/',
            'cookie':
            'passport_csrf_token=f318cdce9b1c5216963fca3485bccd3f; passport_csrf_token_default=f318cdce9b1c5216963fca3485bccd3f; d_ticket=a5fed545b2d955efe44ab55959d23e29678c4; passport_assist_user=Cj0KPtHcW5iThx-PhqaJpip0EKwFjPKEmuMJUZ3xXN_XBfUDO8XcF3NB9CYheOE1Gm8yN_4AO7iecqC6izjTGkgKPKtXUX9cEgksIj-3SCpAhZLvbZy7OnlXMulNE4KEy0wJVJMe3yE4BdT_iIX-8_AWIQ7152-nwwhc_klB8xDS6qsNGImv1lQiAQM2bBSI; n_mh=GT6wTBJ9o6Wqu7VnHmuTt9Ok7MEOH2FanRKJ3PV1f3Q; sso_auth_status=62990bf8ea80b19f2f9474dfc016c69e; sso_auth_status_ss=62990bf8ea80b19f2f9474dfc016c69e; sso_uid_tt=47c1a304af205e748b5069ede4b1e42c; sso_uid_tt_ss=47c1a304af205e748b5069ede4b1e42c; toutiao_sso_user=505e59ea51501ea246465f621ad82efc; toutiao_sso_user_ss=505e59ea51501ea246465f621ad82efc; sid_ucp_sso_v1=1.0.0-KGY5MGEyMGFmOGRjZWVmNmE5YzRmMDcwZTgzYzMxNjI2ZGU1YTRhNjMKHQi16eH4mAMQ4rLGoAYY2hYgDDD0_bzhBTgCQPEHGgJobCIgNTA1ZTU5ZWE1MTUwMWVhMjQ2NDY1ZjYyMWFkODJlZmM; ssid_ucp_sso_v1=1.0.0-KGY5MGEyMGFmOGRjZWVmNmE5YzRmMDcwZTgzYzMxNjI2ZGU1YTRhNjMKHQi16eH4mAMQ4rLGoAYY2hYgDDD0_bzhBTgCQPEHGgJobCIgNTA1ZTU5ZWE1MTUwMWVhMjQ2NDY1ZjYyMWFkODJlZmM; passport_auth_status=839459bf55015c784f5f2fa274263893%2Cac420ca1295ff697c305f23343bfc12f; passport_auth_status_ss=839459bf55015c784f5f2fa274263893%2Cac420ca1295ff697c305f23343bfc12f; uid_tt=bec1bdb91eda06f172209890927557a2; uid_tt_ss=bec1bdb91eda06f172209890927557a2; sid_tt=2c2f8a23bb185b78c0895b9b98d0fd49; sessionid=2c2f8a23bb185b78c0895b9b98d0fd49; sessionid_ss=2c2f8a23bb185b78c0895b9b98d0fd49; store-region=cn-ha; store-region-src=uid; ttwid=1%7CsugdjtQfTgQYF-ojxrw3tYC26tUSdPw3JBf3jASbbGA%7C1678982803%7C85a549f1f64a8074675c31803be45ffc75452132fd04a001ace0637c4615be43; strategyABtestKey=%221679376293.82%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1679981093848%2C%22type%22%3A1%7D; odin_tt=2d2fb436b0583d3f315d4f051fac31cbbcce351103d40606b100e0a13fb933381ecdc6930b924369128e31ce8baa69e4; sid_guard=2c2f8a23bb185b78c0895b9b98d0fd49%7C1679376298%7C4682680%7CSun%2C+14-May-2023+10%3A09%3A38+GMT; sid_ucp_v1=1.0.0-KGJhNWZkZGNkM2Q0ZDk5ZDFiMWJkZjhkOTJkN2M2NGEwNDE1NGZlOGMKFwi16eH4mAMQqv_koAYY2hYgDDgCQPEHGgJscSIgMmMyZjhhMjNiYjE4NWI3OGMwODk1YjliOThkMGZkNDk; ssid_ucp_v1=1.0.0-KGJhNWZkZGNkM2Q0ZDk5ZDFiMWJkZjhkOTJkN2M2NGEwNDE1NGZlOGMKFwi16eH4mAMQqv_koAYY2hYgDDgCQPEHGgJscSIgMmMyZjhhMjNiYjE4NWI3OGMwODk1YjliOThkMGZkNDk; SEARCH_RESULT_LIST_TYPE=%22single%22; home_can_add_dy_2_desktop=%221%22; __ac_nonce=06419402000f37bb05f17; __ac_signature=_02B4Z6wo00f01zjRG5wAAIDCza7xAeVjiHs48R8AAKo312; __live_version__=%221.1.0.7556%22; device_web_cpu_core=4; device_web_memory_size=8; csrf_session_id=08f4add92308ff8b04ebcc86c522ce38; xgplayer_user_id=356776839587; ttcid=c0554a88abd2487ba83cf3822f1bda6675; download_guide=%223%2F20230321%22; live_can_add_dy_2_desktop=%220%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAHUap3JrG49wzgZGqrcdwxWPmuU8fPVxYq3u46HxzQcg%2F1679414400000%2F0%2F0%2F1679379232177%22; msToken=y387NvRl64R-lTVMX_MwmLgLcRBOk1MrK0s3Whzxpryg930CVhpMB3-eI-OWaIlpyeLtr2lvY56z7cwG6wEQwh2LoGK2MFPi67NO8OPLAX-h9Gs7vmArqg==; tt_scid=XBtd0zcY8B9szCJRohRwlGDVOLSFaZjnLKnBPTKcOIper6e.wSljUm21q4metV1S8230; msToken=SAYfKKCwDLjjNXaB9CpEL3lQ36tif0F-OE1N1N054up7W5t_T9nL8B7tLz45vfFEc4_YNA6u9oJKW9Cyfm5P5xHx7_Mb_t-APciIOBje2w9qLJh-5IlSOA==; passport_fe_beating_status=false',
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
            # pprint(stream_url)
            flv_list = []
            m3u8_list = []
            flv_pull_url = stream_url['flv_pull_url']
            for key, value in flv_pull_url.items():
                flv_list.append(value)
            hls_pull_url_map = stream_url['hls_pull_url_map']
            for key, value in hls_pull_url_map.items():
                m3u8_list.append(value)
            list = flv_list + m3u8_list
            time = datetime.datetime.now().ctime().replace(':', '-')
            if 'FILE' in self.settings.keys() and self.settings.file != '':
                file = os.path.join(self.settings.file, 'download', '抖音录播',
                                    name, time)
            else:
                file = os.path.join(os.getcwd(), 'download', '抖音录播', name,
                                    time)
            ali_file = os.path.join('录播', '抖音录播', name,
                                    time).replace('\\', '/')
            if not os.path.exists(file):
                os.makedirs(file)
            # time = str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
            f = open('{}/直播源.txt'.format(file), mode='w', encoding='utf8')
            f.write(list[0])
            f.close()
            logger.info('抖音直播间 - {} - {} | 源地址为 - {}'.format(
                name,
                url.rsplit('/', 1)[1], list[0]))
            if self.open == False:
                logger.info('抖音直播间 - {} - {} | 已成功保存直播源地址到文件'.format(
                    name,
                    url.rsplit('/', 1)[1]))
            if self.open:
                logger.info('抖音直播间 - {} - {} 开始录制'.format(
                    name,
                    url.rsplit('/', 1)[1]))
                if self.settings.docker == False:
                    subout = subprocess.run(
                        "ffmpeg -i " + '"{}"'.format(list[0]) +
                        " -c:a copy -c:v copy -bsf:a aac_adtstoasc -threads {} -preset {} -f {}  -f segment -segment_time {} -strftime 1 "
                        .format(str(self.settings.thread),
                                self.settings.preset, self.settings.scheme,
                                str(self.settings.time)) +
                        '"{}"'.format(
                            os.path.join(file, '%Y-%m-%d-%H-%M-%S.ts')))
                    logger.info(subout)
                if self.settings.docker == True:
                    ssh.Ssh(list[0], os.path.join(file,
                                                  '%Y-%m-%d-%H-%M-%S.ts'),
                            self.settings)
                    alipan.Backup(local_file=file, ali_file=ali_file)
                    shutil.rmtree(
                        os.path.join(
                            os.path.abspath(
                                os.path.join(os.path.dirname(__file__), '..')),
                            'download', '抖音录播', name))
                    # 分段录制
                    # ffmpeg -i -c:a copy -c:v copy -f segment -segment_time 60 -strftime 1 仙某某_%H.ts

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
                'cookie':
                'douyin.com; passport_csrf_token=f318cdce9b1c5216963fca3485bccd3f; passport_csrf_token_default=f318cdce9b1c5216963fca3485bccd3f; d_ticket=a5fed545b2d955efe44ab55959d23e29678c4; passport_assist_user=Cj0KPtHcW5iThx-PhqaJpip0EKwFjPKEmuMJUZ3xXN_XBfUDO8XcF3NB9CYheOE1Gm8yN_4AO7iecqC6izjTGkgKPKtXUX9cEgksIj-3SCpAhZLvbZy7OnlXMulNE4KEy0wJVJMe3yE4BdT_iIX-8_AWIQ7152-nwwhc_klB8xDS6qsNGImv1lQiAQM2bBSI; n_mh=GT6wTBJ9o6Wqu7VnHmuTt9Ok7MEOH2FanRKJ3PV1f3Q; sso_auth_status=62990bf8ea80b19f2f9474dfc016c69e; sso_auth_status_ss=62990bf8ea80b19f2f9474dfc016c69e; sso_uid_tt=47c1a304af205e748b5069ede4b1e42c; sso_uid_tt_ss=47c1a304af205e748b5069ede4b1e42c; toutiao_sso_user=505e59ea51501ea246465f621ad82efc; toutiao_sso_user_ss=505e59ea51501ea246465f621ad82efc; sid_ucp_sso_v1=1.0.0-KGY5MGEyMGFmOGRjZWVmNmE5YzRmMDcwZTgzYzMxNjI2ZGU1YTRhNjMKHQi16eH4mAMQ4rLGoAYY2hYgDDD0_bzhBTgCQPEHGgJobCIgNTA1ZTU5ZWE1MTUwMWVhMjQ2NDY1ZjYyMWFkODJlZmM; ssid_ucp_sso_v1=1.0.0-KGY5MGEyMGFmOGRjZWVmNmE5YzRmMDcwZTgzYzMxNjI2ZGU1YTRhNjMKHQi16eH4mAMQ4rLGoAYY2hYgDDD0_bzhBTgCQPEHGgJobCIgNTA1ZTU5ZWE1MTUwMWVhMjQ2NDY1ZjYyMWFkODJlZmM; passport_auth_status=839459bf55015c784f5f2fa274263893%2Cac420ca1295ff697c305f23343bfc12f; passport_auth_status_ss=839459bf55015c784f5f2fa274263893%2Cac420ca1295ff697c305f23343bfc12f; uid_tt=bec1bdb91eda06f172209890927557a2; uid_tt_ss=bec1bdb91eda06f172209890927557a2; sid_tt=2c2f8a23bb185b78c0895b9b98d0fd49; sessionid=2c2f8a23bb185b78c0895b9b98d0fd49; sessionid_ss=2c2f8a23bb185b78c0895b9b98d0fd49; store-region=cn-ha; store-region-src=uid; ttwid=1%7CsugdjtQfTgQYF-ojxrw3tYC26tUSdPw3JBf3jASbbGA%7C1678982803%7C85a549f1f64a8074675c31803be45ffc75452132fd04a001ace0637c4615be43; douyin.com; strategyABtestKey=%221679376293.82%22; s_v_web_id=verify_lfhta9v2_KWt5nfRL_lOTH_45b6_9aEb_mXzmu3kigz61; odin_tt=2d2fb436b0583d3f315d4f051fac31cbbcce351103d40606b100e0a13fb933381ecdc6930b924369128e31ce8baa69e4; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWNsaWVudC1jc3IiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLVxyXG5NSUlCRGpDQnRRSUJBREFuTVFzd0NRWURWUVFHRXdKRFRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxXHJcbllYSmtNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUVjem1zeHo3TkRFKzUzV0V1SEdieUE5a1pcclxuTlRwdVZGWC96cG9mTWY5ZjlxclQ3bTJFVEEvMDR4Q0drZDFVRjVRWnlMZ2VNWEtQSVNDNXd3VE0vYUZieUtBc1xyXG5NQ29HQ1NxR1NJYjNEUUVKRGpFZE1Cc3dHUVlEVlIwUkJCSXdFSUlPZDNkM0xtUnZkWGxwYmk1amIyMHdDZ1lJXHJcbktvWkl6ajBFQXdJRFNBQXdSUUloQUlVdkNBZzNPbThlazlJTnZIbVdQc0xXQW1XczJhQlJyallNdDI1T282VkFcclxuQWlCckxuYXh4bEhvUGxzRGhDTTFDL2hJSlVUT1ovVmM1SWJNa3pONEJIK0N4Zz09XHJcbi0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLVxyXG4ifQ==; sid_guard=2c2f8a23bb185b78c0895b9b98d0fd49%7C1679376298%7C4682680%7CSun%2C+14-May-2023+10%3A09%3A38+GMT; sid_ucp_v1=1.0.0-KGJhNWZkZGNkM2Q0ZDk5ZDFiMWJkZjhkOTJkN2M2NGEwNDE1NGZlOGMKFwi16eH4mAMQqv_koAYY2hYgDDgCQPEHGgJscSIgMmMyZjhhMjNiYjE4NWI3OGMwODk1YjliOThkMGZkNDk; ssid_ucp_v1=1.0.0-KGJhNWZkZGNkM2Q0ZDk5ZDFiMWJkZjhkOTJkN2M2NGEwNDE1NGZlOGMKFwi16eH4mAMQqv_koAYY2hYgDDgCQPEHGgJscSIgMmMyZjhhMjNiYjE4NWI3OGMwODk1YjliOThkMGZkNDk; csrf_session_id=08f4add92308ff8b04ebcc86c522ce38; ttcid=325974535c744f9d8e4fc77616a2a7f442; SEARCH_RESULT_LIST_TYPE=%22single%22; __live_version__=%221.1.0.7556%22; download_guide=%223%2F20230321%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAHUap3JrG49wzgZGqrcdwxWPmuU8fPVxYq3u46HxzQcg%2F1679414400000%2F0%2F0%2F1679379232177%22; __ac_nonce=06419589e00af60b7ab67; __ac_signature=_02B4Z6wo00f01cHmW3AAAIDANJmx7A.0YhnBxl.AABRic4Vi8JsU3bqMb5YpkgwRHHk2f3cj2b8jJFpmgwxAOZcS7oIaHTptsCUoNAs4XpPWmZGFIwFsJ9W6BcBG4w1MQE6tg-7Ou-rpFl5Oe9; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1679987488763%2C%22type%22%3A1%7D; live_can_add_dy_2_desktop=%221%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAHUap3JrG49wzgZGqrcdwxWPmuU8fPVxYq3u46HxzQcg%2F1679414400000%2F0%2F0%2F1679383390675%22; home_can_add_dy_2_desktop=%221%22; tt_scid=9lGBLFw4Kmd4clqwNnoiP.dSqiw0SkZrbj1i5h5ekHcbVuZrUclmLLa0Q-jdMAiibd11; msToken=ma7RRNHy1eeJggxa2CtSeLf6EcCn7pVdBTdOIg1JiCVmjhoa4Q0qJKf9ywDpZZ-qW_chRL5SIk4Tvc2lL_bc2ny609l343ZdcD8YEisB6neUVldZuI0Lh0QnKJzM8Zg=; msToken=G0KbcQ6Cms18KChmR9KBqYHf4w90ShWuiMlwLtrn8c3nLjeOXWEdOC5Bi7FoQ0uNRZ_UAtTotaZHMJHVDz378r9-jng_AKKMvmfboU624G-ZJeuZFTDTuMJODww7O9g=; passport_fe_beating_status=false',
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