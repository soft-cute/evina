#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/06/22 22:35:05
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
        while True:
            self.ua = Faker(locale='zh_cn').safari()
            if 'iPhone' not in self.ua and 'Windows CE' not in self.ua:
                break

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
        self.s = requests.Session()
        cookies = {
            'passport_csrf_token':
            'e1afb9ce99fa7ea626d23c40a180b2f6',
            'passport_csrf_token_default':
            'e1afb9ce99fa7ea626d23c40a180b2f6',
            'xgplayer_user_id':
            '969136724075',
            's_v_web_id':
            'verify_li8za4se_VqCr8qb3_4sxa_4x6d_BDJH_kx2WZeYFz6Le',
            'pwa2':
            '%223%7C0%22',
            'd_ticket':
            '4cd21e3b754e1a41c0d29cea6be14f17d8601',
            'passport_assist_user':
            'Cj1YjhwapK2cp-xkeh29QX1Snqy2nMC4BtXqkWPi2etXdnoRs-Ne85vJkMvhVQzsZBDrqLFTQ2jlLdVZSic2GkgKPBFULU1wZBODcqrcHpvewvbyjehIM5kDZE1D5l0mQqVs9fuY9cwqqE4EGj9GThiYYph_9WfRxgDFP-VC9BCGv7INGImv1lQiAQPOTK8C',
            'n_mh':
            'GT6wTBJ9o6Wqu7VnHmuTt9Ok7MEOH2FanRKJ3PV1f3Q',
            'sso_auth_status':
            '12ddcde3bbb915dd00ed4ea610ac7b7a',
            'sso_auth_status_ss':
            '12ddcde3bbb915dd00ed4ea610ac7b7a',
            'sso_uid_tt':
            'a603e3572c6df0f7bb5dce5056ca8e64',
            'sso_uid_tt_ss':
            'a603e3572c6df0f7bb5dce5056ca8e64',
            'toutiao_sso_user':
            '8ad0db4ea40760bea6da3e1d42d38691',
            'toutiao_sso_user_ss':
            '8ad0db4ea40760bea6da3e1d42d38691',
            'passport_auth_status':
            '56d274100c4267c85627f3eaa7c46eab%2Cb9c2e3d08a268859ead62530a919ba51',
            'passport_auth_status_ss':
            '56d274100c4267c85627f3eaa7c46eab%2Cb9c2e3d08a268859ead62530a919ba51',
            'uid_tt':
            'ca62c1c1071eb97af712d6df012ea53c',
            'uid_tt_ss':
            'ca62c1c1071eb97af712d6df012ea53c',
            'sid_tt':
            '4dba1971e76b056ed10587eb1562e9e3',
            'sessionid':
            '4dba1971e76b056ed10587eb1562e9e3',
            'sessionid_ss':
            '4dba1971e76b056ed10587eb1562e9e3',
            'LOGIN_STATUS':
            '1',
            'store-region':
            'cn-ha',
            'store-region-src':
            'uid',
            'odin_tt':
            '54ee03eeaa6a0a591ce1ffa0eacd48ffdc4d096e5f4d4e1de937b56e4e22b4c8d38bb94afe29d7f3f8abc72548529184a327801411d6d698691afba792c293d9',
            'ttwid':
            '1%7C0y0tGmzVAZ_ajbyNUQjDF79qGoPoUUjPyAXdzeZzc_k%7C1685629323%7Ceec9018aca3dc968bc3a163ece7a4e3690ccfc3eb8b0a6832d7866ec9481c4e2',
            'publish_badge_show_info':
            '%220%2C0%2C0%2C1687594287181%22',
            'sid_ucp_sso_v1':
            '1.0.0-KDNiNWU1ZmIwOWM0ZDljNDdhZWFhYTA1NDlmMzA3N2E0NDI3NDA1MzAKHQi16eH4mAMQsMrapAYY7zEgDDD0_bzhBTgCQPEHGgJsZiIgOGFkMGRiNGVhNDA3NjBiZWE2ZGEzZTFkNDJkMzg2OTE',
            'ssid_ucp_sso_v1':
            '1.0.0-KDNiNWU1ZmIwOWM0ZDljNDdhZWFhYTA1NDlmMzA3N2E0NDI3NDA1MzAKHQi16eH4mAMQsMrapAYY7zEgDDD0_bzhBTgCQPEHGgJsZiIgOGFkMGRiNGVhNDA3NjBiZWE2ZGEzZTFkNDJkMzg2OTE',
            'sid_guard':
            '4dba1971e76b056ed10587eb1562e9e3%7C1687594288%7C5184000%7CWed%2C+23-Aug-2023+08%3A11%3A28+GMT',
            'sid_ucp_v1':
            '1.0.0-KGZjYWE3MjAxMTk1ODk4NzQ4YmI5ODQ1YTBmMDRlZTFhNDdhYmM4MWEKFwi16eH4mAMQsMrapAYY7zEgDDgCQPEHGgJscSIgNGRiYTE5NzFlNzZiMDU2ZWQxMDU4N2ViMTU2MmU5ZTM',
            'ssid_ucp_v1':
            '1.0.0-KGZjYWE3MjAxMTk1ODk4NzQ4YmI5ODQ1YTBmMDRlZTFhNDdhYmM4MWEKFwi16eH4mAMQsMrapAYY7zEgDDgCQPEHGgJscSIgNGRiYTE5NzFlNzZiMDU2ZWQxMDU4N2ViMTU2MmU5ZTM',
            '__live_version__':
            '%221.1.1.709%22',
            'download_guide':
            '%223%2F20230624%2F1%22',
            'strategyABtestKey':
            '%221687683507.151%22',
            'VIDEO_FILTER_MEMO_SELECT':
            '%7B%22expireTime%22%3A1688288307185%2C%22type%22%3Anull%7D',
            'FOLLOW_NUMBER_YELLOW_POINT_INFO':
            '%22MS4wLjABAAAAHUap3JrG49wzgZGqrcdwxWPmuU8fPVxYq3u46HxzQcg%2F1687708800000%2F0%2F1687685592747%2F0%22',
            'FOLLOW_LIVE_POINT_INFO':
            '%22MS4wLjABAAAAHUap3JrG49wzgZGqrcdwxWPmuU8fPVxYq3u46HxzQcg%2F1687708800000%2F0%2F1687685594605%2F0%22',
            'device_web_cpu_core':
            '4',
            'device_web_memory_size':
            '8',
            'webcast_local_quality':
            'origin',
            'csrf_session_id':
            'fcd8d1a177fe8a8f26881f50dc03bb58',
            'home_can_add_dy_2_desktop':
            '%221%22',
            'passport_fe_beating_status':
            'true',
            '__ac_nonce':
            '0649809f200039e90a651',
            '__ac_signature':
            '_02B4Z6wo00f01Iw7EHwAAIDADDnqPUAJmHyMGxTAAEebZ0pC.FOlWpqBzlSPy2x4hJZ1FY63PSH2dDZ9Eht76yN4BeARRDS3uW8wUseGUyuhELkcsKrdtkR0CCdc5wTqSqeKn7rYaqjYPyHg1f',
            'webcast_leading_last_show_time':
            '1687685626215',
            'webcast_leading_total_show_times':
            '1',
            'live_can_add_dy_2_desktop':
            '%220%22',
            'msToken':
            'ECXtFxaM0bGtOo5dUj_gdlNGUXYomsd9Rj5sj9NtbZBM1JzDMl3g_fGeGeLHetjPpAT7U8LyzyFWFQbus3MWQwcx0gDc2CK5VE8l7tvnELZ2IIBkQgKAcfdXRW12jtM=',
            'tt_scid':
            'gQ7kBueXBmHnokdKyqZt.DfSzAib-a-lu9HEZPpOTs12c5reu9Z2Sf8ECjFzNyxCcaae',
            'msToken':
            'lb9lhAdmfYMAkoc7PMKVW6_ucWKZOadYO1oIa7yVwbRzazBIc-CJzlTX0rnt13Yd-jszfJxAd30GMYTLovGSZrwRt2UxAFMhhPrh78Rw2L46CtA9CPS6lcsb2rpdn_w=',
        }
        self.s.cookies = requests.utils.cookiejar_from_dict(cookies,
                                                            cookiejar=None,
                                                            overwrite=True)

        return self.geturl(url)

    def geturl(self, url):
        headers = {
            'authority': 'live.douyin.com',
            'cookie':
            'passport_csrf_token=e1afb9ce99fa7ea626d23c40a180b2f6; passport_csrf_token_default=e1afb9ce99fa7ea626d23c40a180b2f6; xgplayer_user_id=969136724075; s_v_web_id=verify_li8za4se_VqCr8qb3_4sxa_4x6d_BDJH_kx2WZeYFz6Le; pwa2=%223%7C0%22; d_ticket=4cd21e3b754e1a41c0d29cea6be14f17d8601; passport_assist_user=Cj1YjhwapK2cp-xkeh29QX1Snqy2nMC4BtXqkWPi2etXdnoRs-Ne85vJkMvhVQzsZBDrqLFTQ2jlLdVZSic2GkgKPBFULU1wZBODcqrcHpvewvbyjehIM5kDZE1D5l0mQqVs9fuY9cwqqE4EGj9GThiYYph_9WfRxgDFP-VC9BCGv7INGImv1lQiAQPOTK8C; n_mh=GT6wTBJ9o6Wqu7VnHmuTt9Ok7MEOH2FanRKJ3PV1f3Q; sso_auth_status=12ddcde3bbb915dd00ed4ea610ac7b7a; sso_auth_status_ss=12ddcde3bbb915dd00ed4ea610ac7b7a; sso_uid_tt=a603e3572c6df0f7bb5dce5056ca8e64; sso_uid_tt_ss=a603e3572c6df0f7bb5dce5056ca8e64; toutiao_sso_user=8ad0db4ea40760bea6da3e1d42d38691; toutiao_sso_user_ss=8ad0db4ea40760bea6da3e1d42d38691; passport_auth_status=56d274100c4267c85627f3eaa7c46eab%2Cb9c2e3d08a268859ead62530a919ba51; passport_auth_status_ss=56d274100c4267c85627f3eaa7c46eab%2Cb9c2e3d08a268859ead62530a919ba51; uid_tt=ca62c1c1071eb97af712d6df012ea53c; uid_tt_ss=ca62c1c1071eb97af712d6df012ea53c; sid_tt=4dba1971e76b056ed10587eb1562e9e3; sessionid=4dba1971e76b056ed10587eb1562e9e3; sessionid_ss=4dba1971e76b056ed10587eb1562e9e3; LOGIN_STATUS=1; store-region=cn-ha; store-region-src=uid; odin_tt=54ee03eeaa6a0a591ce1ffa0eacd48ffdc4d096e5f4d4e1de937b56e4e22b4c8d38bb94afe29d7f3f8abc72548529184a327801411d6d698691afba792c293d9; ttwid=1%7C0y0tGmzVAZ_ajbyNUQjDF79qGoPoUUjPyAXdzeZzc_k%7C1685629323%7Ceec9018aca3dc968bc3a163ece7a4e3690ccfc3eb8b0a6832d7866ec9481c4e2; publish_badge_show_info=%220%2C0%2C0%2C1687594287181%22; sid_ucp_sso_v1=1.0.0-KDNiNWU1ZmIwOWM0ZDljNDdhZWFhYTA1NDlmMzA3N2E0NDI3NDA1MzAKHQi16eH4mAMQsMrapAYY7zEgDDD0_bzhBTgCQPEHGgJsZiIgOGFkMGRiNGVhNDA3NjBiZWE2ZGEzZTFkNDJkMzg2OTE; ssid_ucp_sso_v1=1.0.0-KDNiNWU1ZmIwOWM0ZDljNDdhZWFhYTA1NDlmMzA3N2E0NDI3NDA1MzAKHQi16eH4mAMQsMrapAYY7zEgDDD0_bzhBTgCQPEHGgJsZiIgOGFkMGRiNGVhNDA3NjBiZWE2ZGEzZTFkNDJkMzg2OTE; sid_guard=4dba1971e76b056ed10587eb1562e9e3%7C1687594288%7C5184000%7CWed%2C+23-Aug-2023+08%3A11%3A28+GMT; sid_ucp_v1=1.0.0-KGZjYWE3MjAxMTk1ODk4NzQ4YmI5ODQ1YTBmMDRlZTFhNDdhYmM4MWEKFwi16eH4mAMQsMrapAYY7zEgDDgCQPEHGgJscSIgNGRiYTE5NzFlNzZiMDU2ZWQxMDU4N2ViMTU2MmU5ZTM; ssid_ucp_v1=1.0.0-KGZjYWE3MjAxMTk1ODk4NzQ4YmI5ODQ1YTBmMDRlZTFhNDdhYmM4MWEKFwi16eH4mAMQsMrapAYY7zEgDDgCQPEHGgJscSIgNGRiYTE5NzFlNzZiMDU2ZWQxMDU4N2ViMTU2MmU5ZTM; __live_version__=%221.1.1.709%22; download_guide=%223%2F20230624%2F1%22; strategyABtestKey=%221687683507.151%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1688288307185%2C%22type%22%3Anull%7D; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAHUap3JrG49wzgZGqrcdwxWPmuU8fPVxYq3u46HxzQcg%2F1687708800000%2F0%2F1687685592747%2F0%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAHUap3JrG49wzgZGqrcdwxWPmuU8fPVxYq3u46HxzQcg%2F1687708800000%2F0%2F1687685594605%2F0%22; device_web_cpu_core=4; device_web_memory_size=8; webcast_local_quality=origin; csrf_session_id=fcd8d1a177fe8a8f26881f50dc03bb58; home_can_add_dy_2_desktop=%221%22; webcast_leading_last_show_time=1687685626215; webcast_leading_total_show_times=1; live_can_add_dy_2_desktop=%220%22; passport_fe_beating_status=true; __ac_nonce=06498422c003640d1ae2b; __ac_signature=_02B4Z6wo00f017rWk-AAAIDDOtRpopXa6DO69pdAAIo2dOQEw76.ZbxhpnLM.8MAkPWzYKSpdTlUDviaUMkLZvmA00m0gAaK8VG..-MexxPmGBn2HB.u.wT3BgNNrUk7m5JNcoCet4b-DskTcf; tt_scid=rWXGuuW2-KQMuxpIxTQ7BWB78gfPmIynbtve0mwMLqqBdnhSEQoNRrFSCr3HEKOi0e1f; msToken=G2JTwUoTosLHFACdt1O8ivS7t3Kps8C0FjHmhzlJ4DNNvSEL2nYrvCngD9_OfMi-Ot1RsJ7M4YV9Eo4E_YTUf2ynksdE8jIEUyBVJ0ujxcSjpGjRdJgakA==; msToken=8y-4YgQz1d0cUHxCWJjs8uvg5oGQT0gOhlM6QII3lfbVPnTjwGdbZzrodKAsoLU1gujXb8Ykzr2zSvOfFNkfpaWJ_EJbOWHFqrH0Mx8INFCfx1OYJTK3PnQEGzBoROo=',
            'accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language':
            'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'max-age=0',
            'sec-ch-ua':
            '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.ua,
        }
        response = self.s.get(url=url, headers=headers)
        response = parse.unquote(response.text)
        if self.name == None:
            name = re.findall(r'"nickname":"(.*?)",', response, re.S)[0]
        else:
            name = self.name
        try:
            data = json.loads(
                re.findall(
                    r'<script id="RENDER_DATA" type="application/json">(.*?)</script>',
                    response, re.S)[0])
            stream_url = data['app']['initialState']['roomStore']['roomInfo'][
                'room']['stream_url']
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
            logger.info('抖音直播间 - {} - {} | 暂未开播'.format(
                name,
                url.rsplit('/', 1)[1]))

    def phone(self, url):
        resp = self.s.get(url=url)
        data = resp.url.split('?')[0].split('user')
        if len(data) != 2:
            logger.info('抖音直播间 - {} | 链接已失效'.format(url.rsplit('/', 1)[1]))
            sys.exit()
        if len(data) == 2:
            link = 'https://www.douyin.com/user' + data[1]
            headers = {
                'accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language':
                'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'cookie':
                'douyin.com; webcast_local_quality=null; passport_csrf_token=e1afb9ce99fa7ea626d23c40a180b2f6; passport_csrf_token_default=e1afb9ce99fa7ea626d23c40a180b2f6; s_v_web_id=verify_li8z85qz_am2dyk8B_5mP6_4wFv_8nSP_AHL6mtJ1jjQq; __bd_ticket_guard_local_probe=1685372427205; pwa2=%223%7C0%22; d_ticket=4cd21e3b754e1a41c0d29cea6be14f17d8601; passport_assist_user=Cj1YjhwapK2cp-xkeh29QX1Snqy2nMC4BtXqkWPi2etXdnoRs-Ne85vJkMvhVQzsZBDrqLFTQ2jlLdVZSic2GkgKPBFULU1wZBODcqrcHpvewvbyjehIM5kDZE1D5l0mQqVs9fuY9cwqqE4EGj9GThiYYph_9WfRxgDFP-VC9BCGv7INGImv1lQiAQPOTK8C; n_mh=GT6wTBJ9o6Wqu7VnHmuTt9Ok7MEOH2FanRKJ3PV1f3Q; sso_auth_status=12ddcde3bbb915dd00ed4ea610ac7b7a; sso_auth_status_ss=12ddcde3bbb915dd00ed4ea610ac7b7a; sso_uid_tt=a603e3572c6df0f7bb5dce5056ca8e64; sso_uid_tt_ss=a603e3572c6df0f7bb5dce5056ca8e64; toutiao_sso_user=8ad0db4ea40760bea6da3e1d42d38691; toutiao_sso_user_ss=8ad0db4ea40760bea6da3e1d42d38691; passport_auth_status=56d274100c4267c85627f3eaa7c46eab%2Cb9c2e3d08a268859ead62530a919ba51; passport_auth_status_ss=56d274100c4267c85627f3eaa7c46eab%2Cb9c2e3d08a268859ead62530a919ba51; uid_tt=ca62c1c1071eb97af712d6df012ea53c; uid_tt_ss=ca62c1c1071eb97af712d6df012ea53c; sid_tt=4dba1971e76b056ed10587eb1562e9e3; sessionid=4dba1971e76b056ed10587eb1562e9e3; sessionid_ss=4dba1971e76b056ed10587eb1562e9e3; LOGIN_STATUS=1; store-region=cn-ha; store-region-src=uid; odin_tt=54ee03eeaa6a0a591ce1ffa0eacd48ffdc4d096e5f4d4e1de937b56e4e22b4c8d38bb94afe29d7f3f8abc72548529184a327801411d6d698691afba792c293d9; ttwid=1%7C0y0tGmzVAZ_ajbyNUQjDF79qGoPoUUjPyAXdzeZzc_k%7C1685629323%7Ceec9018aca3dc968bc3a163ece7a4e3690ccfc3eb8b0a6832d7866ec9481c4e2; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNzciI6Ii0tLS0tQkVHSU4gQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbk1JSUJEakNCdFFJQkFEQW5NUXN3Q1FZRFZRUUdFd0pEVGpFWU1CWUdBMVVFQXd3UFltUmZkR2xqYTJWMFgyZDFcclxuWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERBUWNEUWdBRW10Rmh2YVk5QnRabDY0T2hHN3pPNEFRaVxyXG40eUpvQmlBV2phN2l1WjRpWkwzeTd0MGwxbXZoaCtiVm5ocUVhZXdpREd6K3VHR3RscVFGVDhJWW9uSVcvcUFzXHJcbk1Db0dDU3FHU0liM0RRRUpEakVkTUJzd0dRWURWUjBSQkJJd0VJSU9kM2QzTG1SdmRYbHBiaTVqYjIwd0NnWUlcclxuS29aSXpqMEVBd0lEU0FBd1JRSWhBSjhmTWt5c2tRY0s2MGUwdktuWXJGTzdHSVhuZGhnMllEZW80QTYyWmQ2VVxyXG5BaUE5V0lldmc5Q1NSUU5sVUEyYmRxZ3J0aFJBTUdZSmZOdG9iL0lid3gwWmVBPT1cclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9; douyin.com; device_web_cpu_core=4; device_web_memory_size=8; webcast_local_quality=null; publish_badge_show_info=%220%2C0%2C0%2C1687594287181%22; strategyABtestKey=%221687594287.23%22; sid_ucp_sso_v1=1.0.0-KDNiNWU1ZmIwOWM0ZDljNDdhZWFhYTA1NDlmMzA3N2E0NDI3NDA1MzAKHQi16eH4mAMQsMrapAYY7zEgDDD0_bzhBTgCQPEHGgJsZiIgOGFkMGRiNGVhNDA3NjBiZWE2ZGEzZTFkNDJkMzg2OTE; ssid_ucp_sso_v1=1.0.0-KDNiNWU1ZmIwOWM0ZDljNDdhZWFhYTA1NDlmMzA3N2E0NDI3NDA1MzAKHQi16eH4mAMQsMrapAYY7zEgDDD0_bzhBTgCQPEHGgJsZiIgOGFkMGRiNGVhNDA3NjBiZWE2ZGEzZTFkNDJkMzg2OTE; sid_guard=4dba1971e76b056ed10587eb1562e9e3%7C1687594288%7C5184000%7CWed%2C+23-Aug-2023+08%3A11%3A28+GMT; sid_ucp_v1=1.0.0-KGZjYWE3MjAxMTk1ODk4NzQ4YmI5ODQ1YTBmMDRlZTFhNDdhYmM4MWEKFwi16eH4mAMQsMrapAYY7zEgDDgCQPEHGgJscSIgNGRiYTE5NzFlNzZiMDU2ZWQxMDU4N2ViMTU2MmU5ZTM; ssid_ucp_v1=1.0.0-KGZjYWE3MjAxMTk1ODk4NzQ4YmI5ODQ1YTBmMDRlZTFhNDdhYmM4MWEKFwi16eH4mAMQsMrapAYY7zEgDDgCQPEHGgJscSIgNGRiYTE5NzFlNzZiMDU2ZWQxMDU4N2ViMTU2MmU5ZTM; __live_version__=%221.1.1.709%22; live_can_add_dy_2_desktop=%220%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAHUap3JrG49wzgZGqrcdwxWPmuU8fPVxYq3u46HxzQcg%2F1687622400000%2F0%2F0%2F1687596982822%22; download_guide=%223%2F20230624%2F0%22; __ac_nonce=0649707b300d754d9a828; __ac_signature=_02B4Z6wo00f01uIMdpQAAIDCYg6M1RaGnMbiLHIAANwhEYMnk2iKkzBZcBhywZ338QnyDbeFS84jEibxcYv6GAu.lH2wMcu9eaUELZZs8Rp7Acu.RECvflu.dNFl10gn9dxIrsbzk06GxWGub6; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAHUap3JrG49wzgZGqrcdwxWPmuU8fPVxYq3u46HxzQcg%2F1687622400000%2F0%2F0%2F1687620111197%22; home_can_add_dy_2_desktop=%221%22; msToken=Mb6eS-7-qXYRrENf8c5qvUuntdlW5Ivy6LVA-9Tf-ZZIuAEj1Ke-HmuQscu0dOmudbDLdbn3nobypELZ2wUSnMd0U2tlMczYHZn59W6_TgCbMIZBRI9P; tt_scid=Qeme6JA-6y-FCYCObS41oZ032RlksMV.bXGvNaS3oMvC.XsrUmEKRKIkoERBttov5733; msToken=iKh5IS0mzCX5NLKPJ5lmxDnK9KZua8ai0T6tbRzULCuuYL9aabGmi5phkQn5JDpV_0iq9lacOdC1fXajesLowFKbE0lx3izHE87Do4rxi1MuX2ArtXw_TbV9-fp_eN4=; passport_fe_beating_status=false',
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44',
            }
            response = self.s.get(url=link, headers=headers).text
            try:
                uid = re.findall(r'<a href="https://live.douyin.com/(\d+)\?',
                                 response, re.S)[0]
                return uid
            except:
                logger.info('抖音直播间 - {} | 暂未开播'.format(url.rsplit('/', 1)[1]))
                sys.exit()



    def geturl_in_json(self, url):
        headers = {
            'cookie':
            'passport_csrf_token=e1afb9ce99fa7ea626d23c40a180b2f6; passport_csrf_token_default=e1afb9ce99fa7ea626d23c40a180b2f6; xgplayer_user_id=969136724075; s_v_web_id=verify_li8za4se_VqCr8qb3_4sxa_4x6d_BDJH_kx2WZeYFz6Le; pwa2=%223%7C0%22; d_ticket=4cd21e3b754e1a41c0d29cea6be14f17d8601; passport_assist_user=Cj1YjhwapK2cp-xkeh29QX1Snqy2nMC4BtXqkWPi2etXdnoRs-Ne85vJkMvhVQzsZBDrqLFTQ2jlLdVZSic2GkgKPBFULU1wZBODcqrcHpvewvbyjehIM5kDZE1D5l0mQqVs9fuY9cwqqE4EGj9GThiYYph_9WfRxgDFP-VC9BCGv7INGImv1lQiAQPOTK8C; n_mh=GT6wTBJ9o6Wqu7VnHmuTt9Ok7MEOH2FanRKJ3PV1f3Q; sso_auth_status=12ddcde3bbb915dd00ed4ea610ac7b7a; sso_auth_status_ss=12ddcde3bbb915dd00ed4ea610ac7b7a; sso_uid_tt=a603e3572c6df0f7bb5dce5056ca8e64; sso_uid_tt_ss=a603e3572c6df0f7bb5dce5056ca8e64; toutiao_sso_user=8ad0db4ea40760bea6da3e1d42d38691; toutiao_sso_user_ss=8ad0db4ea40760bea6da3e1d42d38691; passport_auth_status=56d274100c4267c85627f3eaa7c46eab%2Cb9c2e3d08a268859ead62530a919ba51; passport_auth_status_ss=56d274100c4267c85627f3eaa7c46eab%2Cb9c2e3d08a268859ead62530a919ba51; uid_tt=ca62c1c1071eb97af712d6df012ea53c; uid_tt_ss=ca62c1c1071eb97af712d6df012ea53c; sid_tt=4dba1971e76b056ed10587eb1562e9e3; sessionid=4dba1971e76b056ed10587eb1562e9e3; sessionid_ss=4dba1971e76b056ed10587eb1562e9e3; LOGIN_STATUS=1; store-region=cn-ha; store-region-src=uid; odin_tt=54ee03eeaa6a0a591ce1ffa0eacd48ffdc4d096e5f4d4e1de937b56e4e22b4c8d38bb94afe29d7f3f8abc72548529184a327801411d6d698691afba792c293d9; ttwid=1%7C0y0tGmzVAZ_ajbyNUQjDF79qGoPoUUjPyAXdzeZzc_k%7C1685629323%7Ceec9018aca3dc968bc3a163ece7a4e3690ccfc3eb8b0a6832d7866ec9481c4e2; publish_badge_show_info=%220%2C0%2C0%2C1687594287181%22; sid_ucp_sso_v1=1.0.0-KDNiNWU1ZmIwOWM0ZDljNDdhZWFhYTA1NDlmMzA3N2E0NDI3NDA1MzAKHQi16eH4mAMQsMrapAYY7zEgDDD0_bzhBTgCQPEHGgJsZiIgOGFkMGRiNGVhNDA3NjBiZWE2ZGEzZTFkNDJkMzg2OTE; ssid_ucp_sso_v1=1.0.0-KDNiNWU1ZmIwOWM0ZDljNDdhZWFhYTA1NDlmMzA3N2E0NDI3NDA1MzAKHQi16eH4mAMQsMrapAYY7zEgDDD0_bzhBTgCQPEHGgJsZiIgOGFkMGRiNGVhNDA3NjBiZWE2ZGEzZTFkNDJkMzg2OTE; sid_guard=4dba1971e76b056ed10587eb1562e9e3%7C1687594288%7C5184000%7CWed%2C+23-Aug-2023+08%3A11%3A28+GMT; sid_ucp_v1=1.0.0-KGZjYWE3MjAxMTk1ODk4NzQ4YmI5ODQ1YTBmMDRlZTFhNDdhYmM4MWEKFwi16eH4mAMQsMrapAYY7zEgDDgCQPEHGgJscSIgNGRiYTE5NzFlNzZiMDU2ZWQxMDU4N2ViMTU2MmU5ZTM; ssid_ucp_v1=1.0.0-KGZjYWE3MjAxMTk1ODk4NzQ4YmI5ODQ1YTBmMDRlZTFhNDdhYmM4MWEKFwi16eH4mAMQsMrapAYY7zEgDDgCQPEHGgJscSIgNGRiYTE5NzFlNzZiMDU2ZWQxMDU4N2ViMTU2MmU5ZTM; __live_version__=%221.1.1.709%22; download_guide=%223%2F20230624%2F1%22; strategyABtestKey=%221687683507.151%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1688288307185%2C%22type%22%3Anull%7D; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAHUap3JrG49wzgZGqrcdwxWPmuU8fPVxYq3u46HxzQcg%2F1687708800000%2F0%2F1687685592747%2F0%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAHUap3JrG49wzgZGqrcdwxWPmuU8fPVxYq3u46HxzQcg%2F1687708800000%2F0%2F1687685594605%2F0%22; device_web_cpu_core=4; device_web_memory_size=8; webcast_local_quality=origin; csrf_session_id=fcd8d1a177fe8a8f26881f50dc03bb58; home_can_add_dy_2_desktop=%221%22; webcast_leading_last_show_time=1687685626215; webcast_leading_total_show_times=1; live_can_add_dy_2_desktop=%220%22; passport_fe_beating_status=true; __ac_nonce=06498422c003640d1ae2b; __ac_signature=_02B4Z6wo00f017rWk-AAAIDDOtRpopXa6DO69pdAAIo2dOQEw76.ZbxhpnLM.8MAkPWzYKSpdTlUDviaUMkLZvmA00m0gAaK8VG..-MexxPmGBn2HB.u.wT3BgNNrUk7m5JNcoCet4b-DskTcf; tt_scid=rWXGuuW2-KQMuxpIxTQ7BWB78gfPmIynbtve0mwMLqqBdnhSEQoNRrFSCr3HEKOi0e1f; msToken=G2JTwUoTosLHFACdt1O8ivS7t3Kps8C0FjHmhzlJ4DNNvSEL2nYrvCngD9_OfMi-Ot1RsJ7M4YV9Eo4E_YTUf2ynksdE8jIEUyBVJ0ujxcSjpGjRdJgakA==; msToken=8y-4YgQz1d0cUHxCWJjs8uvg5oGQT0gOhlM6QII3lfbVPnTjwGdbZzrodKAsoLU1gujXb8Ykzr2zSvOfFNkfpaWJ_EJbOWHFqrH0Mx8INFCfx1OYJTK3PnQEGzBoROo=',
            'user-agent': self.ua,
        }

        room_id = '403359338848'

        json_url = f'https://live.douyin.com/webcast/room/web/enter/?aid=6383&app_name=douyin_web&live_id=1' \
                   f'&device_platform=web&language=zh-CN&enter_from=web_live&cookie_enabled=true&screen_widt' \
                   f'h=1366&screen_height=768&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge' \
                   f'&browser_version=116.0.0.0&web_rid={room_id}&room_id_str=7248777764587817767&enter_sourc' \
                   f'e=&Room-Enter-User-Login-Ab=0&is_need_double_stream=false'
        resp = requests.get(url=json_url, headers=headers)
        # name = resp.json()['data']['data'][0]['owner']['nickname']
        # stream_url = resp.json()['data']['data'][0]['stream_url']
        # print(name)
        # print(stream_url)
